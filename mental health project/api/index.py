"""
Vercel Serverless Entrypoint for Mental Health Monitoring System
This file is the WSGI handler for Vercel - 'app' must be exposed at module level.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path so all imports work
current_dir = Path(__file__).parent        # api/
project_root = current_dir.parent          # project root
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "app"))

# Import the Flask app object - Vercel requires 'app' at module level
from app.app_enhanced import app           # noqa: F401  (Vercel picks this up)

# Vercel automatically uses the 'app' WSGI callable above.
# The lines below are only used when running locally via `python api/index.py`.
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=3000)
