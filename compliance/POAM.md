# Plan of Action & Milestones (POA&M) — superset-cognition-demo

> Maintained by **Sentinel** (via Devin). Every scanner finding on a PR becomes a row here, mapped to
> the 800-53 control it evidences (see `SSP.md`). Status transitions: **Open** → **In Remediation**
> (proxy PR opened) → **Remediated** (proxy PR merged) → **Accepted-Risk** (human waiver). The Sentinel
> dashboard renders the live burn-down + MTTR from these rows.

| ID | Finding | Scanner | Control | Severity | Status | PR | Proxy PR | Opened | Remediation |
|----|---------|---------|---------|----------|--------|----|----------|--------|-------------|
| POAM-0001 | _example: hardcoded fallback secret in config_ | Gitleaks | IA-5 | High | Open | — | — | _seed_ | replace with env-injected secret |
| POAM-0002 | `missing-user`: last USER in demo.Dockerfile is root | Semgrep | SA-11 | High | In Remediation | #1 | https://github.com/Soham4001A/superset-cognition-demo/pull/2 | 2026-07-24 | added unprivileged `superset` (uid 1000) user; container no longer runs as root |
| POAM-0003 | `DL3007`: base image pinned to `:latest` | Hadolint | CM-6 | Medium | In Remediation | #1 | https://github.com/Soham4001A/superset-cognition-demo/pull/2 | 2026-07-24 | pinned base image to `python:3.11-slim-bookworm` |
| POAM-0004 | `DL3025`: shell-form CMD prevents signal delivery | Hadolint | CM-6 | Medium | In Remediation | #1 | https://github.com/Soham4001A/superset-cognition-demo/pull/2 | 2026-07-24 | converted CMD to exec/JSON form |
| POAM-0005 | `DL3015`: apt-get install without `--no-install-recommends` | Hadolint | CM-7 | Info | In Remediation | #1 | https://github.com/Soham4001A/superset-cognition-demo/pull/2 | 2026-07-24 | added `--no-install-recommends` (least functionality) |
| POAM-0006 | `DL3009`: apt lists retained in image layer | Hadolint | CM-6 | Info | In Remediation | #1 | https://github.com/Soham4001A/superset-cognition-demo/pull/2 | 2026-07-24 | `rm -rf /var/lib/apt/lists/*` after install |
| POAM-0007 | `DL3008`: `curl` installed without a version pin | Hadolint | CM-6 | Medium | Open | #1 | — | 2026-07-24 | NOT auto-fixed: an exact `curl=<version>` pin breaks the build on every Debian security refresh. Recommendation: owner decides between a pinned digest-based base image with a pinned curl version, or an explicit documented waiver |
| POAM-0008 | Hadolint findings silently dropped from findings.json (concatenated per-file JSON not parsed) | Sentinel scan suite | CA-7 | Medium | In Remediation | #1 | https://github.com/Soham4001A/superset-cognition-demo/pull/2 | 2026-07-24 | `normalize.py::_load` now stream-decodes concatenated JSON documents; 66 previously invisible CM-6 findings are now reported |
| POAM-0009 | Repo-wide scan backlog: 173 high findings (94 Gitleaks, 54 Semgrep, 17 Bandit, 8 Trivy) not attributable to PR #1 | Multiple | RA-5 / IA-5 / SA-11 | High | Open | — | — | 2026-07-24 | Pre-existing baseline debt, out of scope for this PR's diff. Recommendation: triage the Gitleaks hits (largely test fixtures/examples) with an allowlist, then burn down Trivy fixable CVEs |

<!-- SENTINEL:POAM-ROWS -->
<!-- Devin appends new POA&M rows directly above this marker, one per finding. -->

## Summary (auto-updated)

| Metric | Value |
|---|---|
| Open | 3 |
| In Remediation | 6 |
| Remediated | 0 |
| Accepted-Risk | 0 |
| Mean time to remediation (MTTR) | — |
