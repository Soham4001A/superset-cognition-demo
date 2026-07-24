# Demo image for the Sentinel showcase.
FROM python:3.11.14-slim-trixie

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl=8.14.* \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --user-group --create-home --no-log-init --shell /bin/bash demo
COPY --chown=demo:demo . /app

USER demo
CMD ["python", "/app/superset/sentinel_demo_config.py"]
