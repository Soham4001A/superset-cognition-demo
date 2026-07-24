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
"""Demo feature toggle for the Sentinel showcase.

Adds an env-driven flag. NOTE: this option is intentionally NOT documented in docs/ —
Sentinel/Devin should detect the docs drift and add it during its review.
"""

import os

# When true, expose an experimental compliance banner in the UI.
SENTINEL_DEMO_COMPLIANCE_BANNER = (
    os.environ.get("SENTINEL_DEMO_COMPLIANCE_BANNER", "false").lower() == "true"
)
