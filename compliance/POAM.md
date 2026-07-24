<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->

# Plan of Action & Milestones (POA&M) — superset-cognition-demo

> Maintained by **Sentinel** (via Devin). Every scanner finding on a PR becomes a row here, mapped to
> the 800-53 control it evidences (see `SSP.md`). Status transitions: **Open** → **In Remediation**
> (proxy PR opened) → **Remediated** (proxy PR merged) → **Accepted-Risk** (human waiver). The Sentinel
> dashboard renders the live burn-down + MTTR from these rows.

| ID | Finding | Scanner | Control | Severity | Status | PR | Proxy PR | Opened | Remediation |
|----|---------|---------|---------|----------|--------|----|----------|--------|-------------|
| POAM-0001 | _example: hardcoded fallback secret in config_ | Gitleaks | IA-5 | High | Open | — | — | _seed_ | replace with env-injected secret |
| POAM-0005 | Missing ASF license header in `compliance/scanners/normalize.py` and `run_scans.sh` | License header check | SR-3 | Low | Remediated | #10 | issue #5 | 2026-07-24 | prepended standard ASF Apache-2.0 header to both files (no logic changes) |
| POAM-0016 | `demo.live.Dockerfile` runs as root (no `USER` instruction) | Semgrep `dockerfile.security.missing-user` | CM-6 | High | In Remediation | #12 | #15 | 2026-07-24 | add non-root `demo` user, `chown /app`, end on `USER demo` |
| POAM-0017 | `demo.live.Dockerfile` base image unpinned (`python:latest`) | Hadolint DL3007 / Devin Review | CM-6 | High | In Remediation | #12 | #15 | 2026-07-24 | pin `ARG PY_VER=3.11.14-slim-trixie` (matches repo `Dockerfile`) |
| POAM-0018 | `demo.live.Dockerfile` installs apt packages without a version pin | Hadolint DL3008 | CM-6 | Medium | Open | #12 | — | 2026-07-24 | recommend pinning `curl=<version>` once the demo image's base cadence is fixed; exact Debian pins break on base-image rebuilds, left for the author |
| POAM-0019 | `demo.live.Dockerfile` apt install without `--no-install-recommends` | Hadolint DL3015 | CM-7 | Low | In Remediation | #12 | #15 | 2026-07-24 | added `--no-install-recommends` (least functionality) |
| POAM-0020 | `demo.live.Dockerfile` leaves apt lists in the image layer | Hadolint DL3009 / Devin Review | CM-6 | Low | In Remediation | #12 | #15 | 2026-07-24 | `rm -rf /var/lib/apt/lists/*` in the same layer |
| POAM-0021 | `demo.live.Dockerfile` `CMD` uses shell form, not JSON exec form | Hadolint DL3025 | CM-6 | Low | In Remediation | #12 | #15 | 2026-07-24 | converted `CMD` to JSON array form |
| POAM-0022 | Missing ASF license header in `demo.live.Dockerfile` | Devin Review (RAT / repo rule) | SR-3 | Low | Remediated | #12 | — | 2026-07-24 | ASF Apache-2.0 header prepended on `demo/live-review` |
| POAM-0023 | `SENTINEL_LIVE_DEMO_FLAG` and the new demo build file shipped undocumented (docs drift) | docs-currency build | CM-2 / CM-3, SA-5 | Medium | Remediated | #12 | — | 2026-07-24 | documented in `docs/admin_docs/installation/docker-builds.mdx`; Docusaurus build re-run clean |
| POAM-0024 | Scan harness silently dropped **all** Hadolint findings (concatenated per-file JSON arrays unparsable) | Sentinel `normalize.py` | CA-7 / RA-5 | Medium | In Remediation | #12 | #15 | 2026-07-24 | decode concatenated JSON documents and flatten per-file arrays (0 → 66 Hadolint findings ingested) |
| POAM-0030 | Missing ASF license header in `compliance/POAM.md` and `compliance/SSP.md` (RAT `License Check` failing on the base branch) | Apache RAT | SR-3 | Low | Remediated | #12 | — | 2026-07-24 | prepended HTML-comment ASF header to both documents |
| POAM-0025 | Pre-existing backlog: 253 Gitleaks secret matches repo-wide (largely test fixtures / docs samples) | Gitleaks | IA-5 | High | Open | #12 | — | 2026-07-24 | out of PR scope — baseline/allowlist the fixtures, rotate any live credential |
| POAM-0026 | Pre-existing backlog: 54 high-severity Semgrep findings repo-wide (raw SQL via `text()`/`execute`, `subprocess(shell=True)`) | Semgrep | SA-11 | High | Open | #12 | — | 2026-07-24 | out of PR scope — triage against `SECURITY.md` trust boundaries |
| POAM-0027 | Pre-existing backlog: 17 high-severity Bandit findings (weak hashes, Jinja2 autoescape, shell use) | Bandit | SA-11 | High | Open | #12 | — | 2026-07-24 | out of PR scope — remediate per module |
| POAM-0028 | Pre-existing backlog: 10 high-severity dependency CVEs, all with fixed versions available | Trivy | RA-5 / SI-2 | High | Open | #12 | — | 2026-07-24 | out of PR scope — bump affected packages in `requirements/` |
| POAM-0029 | Pre-existing backlog: 14 dependencies with non-allowlisted licenses | pip-licenses | SR-3 | Medium | Open | #12 | — | 2026-07-24 | out of PR scope — legal review; extend allowlist or replace packages |

<!-- SENTINEL:POAM-ROWS -->
<!-- Devin appends new POA&M rows directly above this marker, one per finding. -->

## Summary (auto-updated)

| Metric | Value |
|---|---|
| Open | 7 |
| In Remediation | 6 |
| Remediated | 4 |
| Accepted-Risk | 0 |
| Mean time to remediation (MTTR) | — |
