#!/usr/bin/env python3
"""Fold raw scanner outputs into ONE control-mapped findings.json + summary.md.

Unified finding schema:
  {id, scanner, control, severity(critical|high|medium|low|info), file, line, rule,
   message, fixable}

Exit 2 if any high/critical finding (the merge gate), else 0.
Usage: normalize.py <raw_dir> <out_dir>
"""

import contextlib
import json  # noqa: TID251  # standalone script: superset.utils.json is unavailable
import pathlib
import sys
from typing import Any

RAW = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])

# scanner -> 800-53 control it evidences (mirrors SSP.md)
CONTROL = {
    "semgrep": "SA-11",
    "bandit": "SA-11",
    "gitleaks": "IA-5",
    "trivy": "RA-5",
    "hadolint": "CM-6",
    "kubelinter": "CM-6",
    "licenses": "SR-3",
}
# permissive licenses that pass SR-3; anything else is a finding
LICENSE_ALLOW = {
    "mit",
    "bsd",
    "bsd-2-clause",
    "bsd-3-clause",
    "apache",
    "apache-2.0",
    "apache 2.0",
    "isc",
    "python software foundation license",
    "mpl-2.0",
    "unlicense",
    "0bsd",
    "cc0-1.0",
}


def _load(name: str) -> Any:
    p = RAW / name
    if not p.exists() or p.stat().st_size == 0:
        return None
    text = p.read_text()
    with contextlib.suppress(ValueError):
        return json.loads(text)
    # some tools emit ndjson / several JSON documents concatenated (hadolint runs
    # once per file and appends), so decode the stream document by document
    decoder, idx = json.JSONDecoder(), 0
    out: list[Any] = []
    while idx < len(text):
        while idx < len(text) and text[idx].isspace():
            idx += 1
        if idx >= len(text):
            break
        try:
            doc, idx = decoder.raw_decode(text, idx)
        except ValueError:
            return None
        out.extend(doc) if isinstance(doc, list) else out.append(doc)
    return out or None


def _sev(x: Any, default: str = "medium") -> str:
    m = {
        "critical": "critical",
        "error": "high",
        "high": "high",
        "warning": "medium",
        "medium": "medium",
        "moderate": "medium",
        "low": "low",
        "info": "info",
        "unknown": "low",
        "note": "info",
    }
    return m.get(str(x).lower(), default)


findings: list[dict[str, Any]] = []


def add(  # noqa: PLR0913
    scanner: str,
    severity: str,
    file: Any,
    line: Any,
    rule: Any,
    message: Any,
    fixable: bool = True,
) -> None:
    findings.append(
        {
            "id": f"{scanner.upper()}-{len(findings) + 1:04d}",
            "scanner": scanner,
            "control": CONTROL.get(scanner, "RA-5"),
            "severity": severity,
            "file": file,
            "line": line,
            "rule": rule,
            "message": (message or "")[:300],
            "fixable": fixable,
        }
    )


# ---- Semgrep --------------------------------------------------------------
d = _load("semgrep.json")
for r in (d or {}).get("results", []) if isinstance(d, dict) else []:
    add(
        "semgrep",
        _sev(r.get("extra", {}).get("severity")),
        r.get("path"),
        (r.get("start") or {}).get("line"),
        r.get("check_id"),
        (r.get("extra") or {}).get("message"),
    )

# ---- Bandit ---------------------------------------------------------------
d = _load("bandit.json")
for r in (d or {}).get("results", []) if isinstance(d, dict) else []:
    add(
        "bandit",
        _sev(r.get("issue_severity")),
        r.get("filename"),
        r.get("line_number"),
        r.get("test_id"),
        r.get("issue_text"),
    )

# ---- Gitleaks (secrets — always high) -------------------------------------
d = _load("gitleaks.json")
for r in d or []:
    if isinstance(r, dict):
        add(
            "gitleaks",
            "high",
            r.get("File"),
            r.get("StartLine"),
            r.get("RuleID"),
            r.get("Description"),
            fixable=True,
        )

# ---- Trivy (CVEs) ---------------------------------------------------------
d = _load("trivy.json")
for res in (d or {}).get("Results", []) if isinstance(d, dict) else []:
    for v in res.get("Vulnerabilities") or []:
        add(
            "trivy",
            _sev(v.get("Severity")),
            res.get("Target"),
            None,
            v.get("VulnerabilityID"),
            f"{v.get('PkgName')} {v.get('InstalledVersion')} → "
            f"{v.get('FixedVersion') or 'no fix'}: {v.get('Title', '')}",
            fixable=bool(v.get("FixedVersion")),
        )

# ---- Hadolint -------------------------------------------------------------
d = _load("hadolint.json")
for r in d if isinstance(d, list) else []:
    if isinstance(r, dict):
        add(
            "hadolint",
            _sev(r.get("level")),
            r.get("file"),
            r.get("line"),
            r.get("code"),
            r.get("message"),
        )

# ---- kube-linter ----------------------------------------------------------
d = _load("kubelinter.json")
for r in (d or {}).get("Reports", []) if isinstance(d, dict) else []:
    add(
        "kubelinter",
        "medium",
        ((r.get("Object") or {}).get("Metadata") or {}).get("FilePath"),
        None,
        r.get("Check"),
        (r.get("Diagnostic") or {}).get("Message"),
    )

# ---- Licenses -------------------------------------------------------------
d = _load("licenses.json")
for r in d or []:
    if isinstance(r, dict):
        lic = (r.get("License") or "unknown").lower()
        if not any(a in lic for a in LICENSE_ALLOW):
            add(
                "licenses",
                "medium",
                r.get("Name"),
                None,
                lic,
                f"{r.get('Name')} {r.get('Version')} uses non-allowlisted "
                f"license '{r.get('License')}'",
                fixable=False,
            )

# ---- Aggregate + write ----------------------------------------------------
by_sev: dict[str, int] = {}
by_control: dict[str, int] = {}
for f in findings:
    by_sev[f["severity"]] = by_sev.get(f["severity"], 0) + 1
    by_control[f["control"]] = by_control.get(f["control"], 0) + 1

gating = by_sev.get("critical", 0) + by_sev.get("high", 0)
result = {
    "total": len(findings),
    "by_severity": by_sev,
    "by_control": by_control,
    "gating_high_or_critical": gating,
    "findings": findings,
}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "findings.json").write_text(json.dumps(result, indent=2))

lines = [
    f"# Sentinel compliance scan — {len(findings)} findings",
    "",
    f"**Gating (high/critical): {gating}** — {'❌ BLOCK' if gating else '✅ clear'}",
    "",
    "| severity | count |",
    "|---|---|",
]
for s in ("critical", "high", "medium", "low", "info"):
    if by_sev.get(s):
        lines.append(f"| {s} | {by_sev[s]} |")
lines += ["", "| control | findings |", "|---|---|"]
for c, n in sorted(by_control.items()):
    lines.append(f"| {c} | {n} |")
(OUT / "summary.md").write_text("\n".join(lines) + "\n")

print(
    f"  [normalize] {len(findings)} findings ({gating} gating) -> "
    f"{OUT / 'findings.json'}",
    file=sys.stderr,
)
sys.exit(2 if gating else 0)
