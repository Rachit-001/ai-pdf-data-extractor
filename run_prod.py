#!/usr/bin/env python3
"""
Production server runner
Sets environment to production mode and starts the server
"""

import os
os.environ['FLASK_ENV'] = 'production'

from app import app

if __name__ == '__main__':
    print("🏭 Starting in PRODUCTION mode")
    print("   - Debug disabled")
    print("   - Waitress WSGI server")
    print("   - Minimal logging")
    print("   - Production optimized")
    print()
    
    port = int(os.environ.get('PORT', 5000))
    
    try:
        from waitress import serve
        print(f"   Server running on http://0.0.0.0:{port}")
        serve(app, host='0.0.0.0', port=port)
    except ImportError:
        print("   ERROR: Waitress not installed!")
        print("   Run: pip install waitress")
        app.run(host='0.0.0.0', port=port, debug=False)
