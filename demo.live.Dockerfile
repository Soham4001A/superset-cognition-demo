# demo.live.Dockerfile — deliberately flawed for the Sentinel PR-gate demo
FROM python:latest
RUN apt-get update && apt-get install -y curl
ENV SENTINEL_LIVE_DEMO_FLAG=1
COPY . /app
CMD python /app/main.py
