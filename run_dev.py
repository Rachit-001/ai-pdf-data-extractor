#!/usr/bin/env python3
"""
Development server runner
Sets environment to development mode and starts the server
"""

import os
os.environ['FLASK_ENV'] = 'development'

from app import app

if __name__ == '__main__':
    print("🚀 Starting in DEVELOPMENT mode")
    print("   - Debug enabled")
    print("   - Auto-reload on code changes")
    print("   - Detailed logging")
    print("   - Flask development server")
    print()
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
