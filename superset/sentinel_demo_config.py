"""Demo feature toggle for the Sentinel showcase.

Adds an env-driven flag. NOTE: this option is intentionally NOT documented in docs/ —
Sentinel/Devin should detect the docs drift and add it during its review.
"""
import os

# When true, expose an experimental compliance banner in the UI.
SENTINEL_DEMO_COMPLIANCE_BANNER = os.environ.get("SENTINEL_DEMO_COMPLIANCE_BANNER", "false").lower() == "true"
