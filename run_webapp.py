#!/usr/bin/env python3
"""
BYTEME Web App Launcher
Simple script to run the web application
"""

import os
import sys
import subprocess

def main():
    """Launch the BYTEME web application"""
    
    # Change to webapp directory
    webapp_dir = os.path.join(os.path.dirname(__file__), 'webapp')
    
    if not os.path.exists(webapp_dir):
        print("❌ Error: webapp directory not found!")
        print("Make sure you're running this from the BYTEME project root.")
        return
    
    # Change to webapp directory
    os.chdir(webapp_dir)
    
    print("🚀 Starting BYTEME Web Application...")
    print("📱 Open http://localhost:8080 in your browser")
    print("🔗 API available at http://localhost:8080/api/analyze")
    print("=" * 50)
    
    try:
        # Run the Flask app
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Web app stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting web app: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
