#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# demo.live.Dockerfile — live-demo service image for the Sentinel PR-gate demo
ARG PY_VER=3.11.14-slim-trixie
FROM python:${PY_VER}

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

ENV SENTINEL_LIVE_DEMO_FLAG=1

COPY . /app

RUN useradd --system --create-home --shell /usr/sbin/nologin demo \
    && chown -R demo:demo /app
USER demo

CMD ["python", "/app/main.py"]
