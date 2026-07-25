# Plan of Action & Milestones (POA&M) — superset-cognition-demo

> Maintained by **Sentinel** (via Devin). Every scanner finding on a PR becomes a row here, mapped to
> the 800-53 control it evidences (see `SSP.md`). Status transitions: **Open** → **In Remediation**
> (proxy PR opened) → **Remediated** (proxy PR merged) → **Accepted-Risk** (human waiver). The Sentinel
> dashboard renders the live burn-down + MTTR from these rows.

| ID | Finding | Scanner | Control | Severity | Status | PR | Proxy PR | Opened | Remediation |
|----|---------|---------|---------|----------|--------|----|----------|--------|-------------|
| POAM-0001 | _example: hardcoded fallback secret in config_ | Gitleaks | IA-5 | High | Open | — | — | _seed_ | replace with env-injected secret |
| POAM-0005 | Missing ASF license header in `compliance/scanners/normalize.py` and `run_scans.sh` | License header check | SR-3 | Low | Remediated | #10 | issue #5 | 2026-07-24 | prepended standard ASF Apache-2.0 header to both files (no logic changes) |
| POAM-0006 | Container image runs as root — no `USER` in `demo.live.Dockerfile` | Semgrep (`dockerfile.security.missing-user`) | CM-6 | High | In Remediation | #16 | https://github.com/Soham4001A/superset-cognition-demo/pull/17 | 2026-07-25 | added unprivileged `demo` uid 1001, `COPY --chown`, `USER demo` |
| POAM-0007 | Unpinned base image `python:latest` (DL3007) | Hadolint + Devin Review | CM-6 | Medium | In Remediation | #16 | https://github.com/Soham4001A/superset-cognition-demo/pull/17 | 2026-07-25 | pinned to `python:3.11.13-slim-bookworm` |
| POAM-0008 | apt cache and recommended packages left in image layer (DL3009, DL3015) | Hadolint | CM-6 | Low | In Remediation | #16 | https://github.com/Soham4001A/superset-cognition-demo/pull/17 | 2026-07-25 | `--no-install-recommends` + `rm -rf /var/lib/apt/lists/*` |
| POAM-0009 | Shell-form `CMD` prevents signal handling (DL3025) | Hadolint | CM-6 | Medium | In Remediation | #16 | https://github.com/Soham4001A/superset-cognition-demo/pull/17 | 2026-07-25 | exec-form `CMD ["python", "/app/main.py"]` |
| POAM-0010 | `COPY . /app` can bake local secrets into published image layers | Devin Review | IA-5 | Medium | In Remediation | #16 | https://github.com/Soham4001A/superset-cognition-demo/pull/17 | 2026-07-25 | `.dockerignore` excludes `.env*`, `*.pem`, `*.key`, `*.p12`, `id_rsa*`, `.aws/`, `.npmrc`, credential JSON |
| POAM-0011 | Missing ASF license header in `demo.live.Dockerfile` | Devin Review / RAT | SR-3 | Low | Remediated | #16 | — (direct commit `d62b875`) | 2026-07-25 | prepended standard ASF Apache-2.0 header (no logic change) |
| POAM-0012 | Docs drift: demo image and `SENTINEL_LIVE_DEMO_FLAG` env var undocumented | Docs currency check | CM-2 | Medium | Remediated | #16 | — (direct commit `d62b875`) | 2026-07-25 | documented image + env var in `docs/admin_docs/installation/docker-builds.mdx`; Docusaurus build passes |
| POAM-0013 | Gate evidence gap: Hadolint output dropped by `normalize.py` (66 Dockerfile findings invisible) | Sentinel gate self-check | CM-6 | Medium | In Remediation | #16 | https://github.com/Soham4001A/superset-cognition-demo/pull/17 | 2026-07-25 | `run_scans.sh` now emits hadolint findings as ndjson |
| POAM-0014 | apt package versions unpinned (DL3008) | Hadolint | CM-6 | Low | Open | #16 | — | 2026-07-25 | recommend Accepted-Risk: pinning `curl=<version>` breaks on base-image rebuilds; pin at digest level if required |
| POAM-0015 | `CMD` references `/app/main.py`, which does not exist in the repo — container exits immediately | Sentinel diff review | CM-2 | Low | Open | #16 | — | 2026-07-25 | author to add the entrypoint module or correct the `CMD` target (product logic, not auto-fixed) |
<!-- SENTINEL:POAM-ROWS -->
<!-- Devin appends new POA&M rows directly above this marker, one per finding. -->

## Summary (auto-updated)

| Metric | Value |
|---|---|
| Open | 3 |
| In Remediation | 6 |
| Remediated | 3 |
| Accepted-Risk | 0 |
| Mean time to remediation (MTTR) | — |
