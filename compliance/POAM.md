# Plan of Action & Milestones (POA&M) — superset-cognition-demo

> Maintained by **Sentinel** (via Devin). Every scanner finding on a PR becomes a row here, mapped to
> the 800-53 control it evidences (see `SSP.md`). Status transitions: **Open** → **In Remediation**
> (proxy PR opened) → **Remediated** (proxy PR merged) → **Accepted-Risk** (human waiver). The Sentinel
> dashboard renders the live burn-down + MTTR from these rows.

| ID | Finding | Scanner | Control | Severity | Status | PR | Proxy PR | Opened | Remediation |
|----|---------|---------|---------|----------|--------|----|----------|--------|-------------|
| POAM-0001 | _example: hardcoded fallback secret in config_ | Gitleaks | IA-5 | High | Open | — | — | _seed_ | replace with env-injected secret |
| POAM-0002 | `demo.Dockerfile` container runs as root (no `USER` instruction) | Semgrep | CM-6 | High | In Remediation | #3 | [#4](https://github.com/Soham4001A/superset-cognition-demo/pull/4) | 2026-07-24 | add non-root `USER demo` as the final user |
| POAM-0003 | `demo.Dockerfile` base image unpinned (`python:latest`) | Hadolint DL3007 | CM-6 / SR-4 | Medium | In Remediation | #3 | [#4](https://github.com/Soham4001A/superset-cognition-demo/pull/4) | 2026-07-24 | pin to `python:3.11.14-slim-trixie` (matches repo `PY_VER`) |
| POAM-0004 | `demo.Dockerfile` installs apt packages without version pin | Hadolint DL3008 | CM-6 | Medium | In Remediation | #3 | [#4](https://github.com/Soham4001A/superset-cognition-demo/pull/4) | 2026-07-24 | pin `curl` to an explicit version range |
| POAM-0005 | `demo.Dockerfile` apt install without `--no-install-recommends` | Hadolint DL3015 | CM-7 | Low | In Remediation | #3 | [#4](https://github.com/Soham4001A/superset-cognition-demo/pull/4) | 2026-07-24 | add `--no-install-recommends` (least functionality) |
| POAM-0006 | `demo.Dockerfile` leaves apt lists in the image layer | Hadolint DL3009 | CM-6 | Low | In Remediation | #3 | [#4](https://github.com/Soham4001A/superset-cognition-demo/pull/4) | 2026-07-24 | `rm -rf /var/lib/apt/lists/*` in the same layer |
| POAM-0007 | `demo.Dockerfile` `CMD` uses shell form, not JSON exec form | Hadolint DL3025 | CM-6 | Low | In Remediation | #3 | [#4](https://github.com/Soham4001A/superset-cognition-demo/pull/4) | 2026-07-24 | convert `CMD` to JSON array form |
| POAM-0008 | `SENTINEL_DEMO_COMPLIANCE_BANNER` config flag shipped undocumented (docs drift) | docs-currency build | CM-2 / CM-3, SA-5 | Medium | Remediated | #3 | — | 2026-07-24 | documented in `docs/admin_docs/configuration/configuring-superset.mdx` |
| POAM-0009 | Scan harness silently drops all Hadolint findings (concatenated JSON arrays unparsable) | Sentinel normalize.py | CA-7 / RA-5 | Medium | In Remediation | #3 | [#4](https://github.com/Soham4001A/superset-cognition-demo/pull/4) | 2026-07-24 | parse concatenated JSON arrays in `normalize.py` |
| POAM-0010 | Pre-existing backlog: 94 Gitleaks secret matches repo-wide (largely test fixtures / docs samples) | Gitleaks | IA-5 | High | Open | #3 | — | 2026-07-24 | out of PR scope — triage with a baseline/allowlist, then rotate any live credential |
| POAM-0011 | Pre-existing backlog: 54 high-severity Semgrep findings repo-wide (raw SQL via `text()`/`execute`, `subprocess(shell=True)`) | Semgrep | SA-11 | High | Open | #3 | — | 2026-07-24 | out of PR scope — triage against `SECURITY.md` trust boundaries; file per-module remediations |
| POAM-0012 | Pre-existing backlog: 17 high-severity Bandit findings (weak hashes B324, Jinja2 autoescape B701, shell use B602/B605) | Bandit | SA-11 | High | Open | #3 | — | 2026-07-24 | out of PR scope — remediate per module; `HASH_ALGORITHM` already defaults to sha256 |
| POAM-0013 | Pre-existing backlog: 8 high/critical dependency CVEs with fixes available | Trivy | RA-5 / SI-2 | High | Open | #3 | — | 2026-07-24 | out of PR scope — bump affected packages in `requirements/` |
| POAM-0014 | Pre-existing backlog: 27 kube-linter hardening findings in `helm/` | kube-linter | CM-6 | Medium | Open | #3 | — | 2026-07-24 | out of PR scope — add resource limits, drop capabilities, run as non-root |
| POAM-0015 | Pre-existing backlog: 14 dependencies with non-allowlisted licenses | pip-licenses | SR-3 | Medium | Open | #3 | — | 2026-07-24 | out of PR scope — legal review; extend allowlist or replace packages |

<!-- SENTINEL:POAM-ROWS -->
<!-- Devin appends new POA&M rows directly above this marker, one per finding. -->

## Summary (auto-updated)

| Metric | Value |
|---|---|
| Open | 7 |
| In Remediation | 7 |
| Remediated | 1 |
| Accepted-Risk | 0 |
| Mean time to remediation (MTTR) | — |
