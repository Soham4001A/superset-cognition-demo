# Intentional hardening issues for the Sentinel demo (Hadolint should flag these):
#  - unpinned base tag (:latest)  - apt without --no-install-recommends / version pins  - no cleanup
FROM python:latest
RUN apt-get update && apt-get install -y curl
COPY . /app
CMD python /app/superset/sentinel_demo_config.py
