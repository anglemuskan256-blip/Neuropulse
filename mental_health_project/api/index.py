"""
Vercel WSGI Entry Point for Mental Health Monitoring System
This file serves as the serverless function handler for Vercel
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

# Import the Flask app
from app.app_enhanced import app

# Handle Vercel WSGI requirement
def handler(request):
    return app(request.environ, request.start_response)

# For local testing with `vercel dev`
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3000)
