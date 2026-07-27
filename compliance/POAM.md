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

| POAM-0008 | Unhardened JSON handling in `compliance/scanners/normalize.py` — malformed/empty raw output or missing args crashed the gate | Bandit/Semgrep | SA-11 | Medium | Remediated | #19 | issue #8 | 2026-07-26 | added argv guard + `_get`/`_dicts` guards so a malformed raw file degrades to 'no findings from that scanner' instead of failing the run |
| POAM-0020 | `demo.live.Dockerfile` runs as root — no `USER` instruction, container process is uid 0 | Semgrep (`dockerfile.security.missing-user`) + Devin Review | CM-6 | High | In Remediation | #20 | #22 | 2026-07-27 | added system user `demo` and `USER 1001` as the final user |
| POAM-0021 | `FROM python:latest` — floating, unverified base image breaks reproducibility and supply-chain integrity | Hadolint DL3007 + Devin Review | SR-3 | Medium | In Remediation | #20 | #22 | 2026-07-27 | pinned via `ARG PY_VER=3.11.14-slim-trixie`, matching the root `Dockerfile` convention |
| POAM-0022 | apt install pulls recommended packages and leaves package lists in the image layer | Hadolint DL3015/DL3009 | CM-7 | Low | In Remediation | #20 | #22 | 2026-07-27 | `--no-install-recommends` + `rm -rf /var/lib/apt/lists/*` |
| POAM-0023 | `CMD` in shell form — PID 1 is a shell, signals are not forwarded to the app | Hadolint DL3025 | CM-6 | Low | In Remediation | #20 | #22 | 2026-07-27 | switched to JSON-exec form `CMD ["python", "/app/main.py"]` |
| POAM-0024 | Missing ASF license header on new file `demo.live.Dockerfile` | Devin Review / RAT license check | SR-3 | Low | In Remediation | #20 | #22 | 2026-07-27 | prepended the standard ASF Apache-2.0 header |
| POAM-0025 | `COPY . /app` copies the whole build context; root `.dockerignore` does not exclude `.env`/key material, so secrets present in the context can be baked into image layers | Devin Review | IA-5 / SC-28 | Medium | Open | #20 | — | 2026-07-27 | **Recommendation (human decision):** copy only the demo app directory once it exists rather than the repo root; a global `.dockerignore` exclusion is not safe because `docker/.env` is tracked and consumed by the main image build |
| POAM-0026 | `curl` installed in the demo image but unused by the entrypoint, and its version is unpinned | Hadolint DL3008 + Devin Review (least functionality) | CM-7 | Low | Open | #20 | — | 2026-07-27 | **Recommendation (human decision):** drop `curl` unless it backs a healthcheck; version-pinning it to a distro snapshot would make builds brittle |
| POAM-0027 | Demo image entrypoint targets `/app/main.py`, which does not exist in the repository — the image cannot start as written | Sentinel diff review | CM-2 | Medium | Open | #20 | — | 2026-07-27 | **Author action:** add the demo service entrypoint or point `CMD` at an existing module (product logic, not remediated by Sentinel) |
<!-- SENTINEL:POAM-ROWS -->
<!-- Devin appends new POA&M rows directly above this marker, one per finding. -->

## Summary (auto-updated)

| Metric | Value |
|---|---|
| Open | 4 |
| In Remediation | 5 |
| Remediated | 2 |
| Accepted-Risk | 0 |
| Mean time to remediation (MTTR) | — |
