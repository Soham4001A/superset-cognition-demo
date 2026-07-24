# Plan of Action & Milestones (POA&M) — superset-cognition-demo

> Maintained by **Sentinel** (via Devin). Every scanner finding on a PR becomes a row here, mapped to
> the 800-53 control it evidences (see `SSP.md`). Status transitions: **Open** → **In Remediation**
> (proxy PR opened) → **Remediated** (proxy PR merged) → **Accepted-Risk** (human waiver). The Sentinel
> dashboard renders the live burn-down + MTTR from these rows.

| ID | Finding | Scanner | Control | Severity | Status | PR | Proxy PR | Opened | Remediation |
|----|---------|---------|---------|----------|--------|----|----------|--------|-------------|
| POAM-0001 | _example: hardcoded fallback secret in config_ | Gitleaks | IA-5 | High | Open | — | — | _seed_ | replace with env-injected secret |
| POAM-0005 | Missing ASF license header in `compliance/scanners/normalize.py` and `run_scans.sh` | License header check | SR-3 | Low | Remediated | #10 | issue #5 | 2026-07-24 | prepended standard ASF Apache-2.0 header to both files (no logic changes) |
| POAM-0007 | Hadolint findings in `dockerize.Dockerfile` (unpinned `alpine:latest`, unpinned apk packages, unquoted var, no `pipefail`) | Hadolint | CM-6/CM-7 | Medium | Remediated | — | issue #7 | 2026-07-24 | pinned base image to `alpine:3.21`, pinned `wget`/`openssl` versions, set `SHELL` with `-o pipefail`, quoted download URL; hadolint 5 findings → 0, image builds and `dockerize -version` works |

<!-- SENTINEL:POAM-ROWS -->
<!-- Devin appends new POA&M rows directly above this marker, one per finding. -->

## Summary (auto-updated)

| Metric | Value |
|---|---|
| Open | 0 |
| In Remediation | 0 |
| Remediated | 0 |
| Accepted-Risk | 0 |
| Mean time to remediation (MTTR) | — |
