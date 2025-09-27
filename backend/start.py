#!/usr/bin/env python3
"""
Simple startup script for Smart City Management Platform Backend
No Redis required - uses memory storage for rate limiting
"""

import os
import sys
import subprocess
from pathlib import Path

def check_mongodb():
    """Check if MongoDB is running."""
    try:
        import pymongo
        client = pymongo.MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
        client.server_info()
        print("✅ MongoDB is running")
        return True
    except Exception as e:
        print(f"❌ MongoDB is not running: {e}")
        print("Please start MongoDB first:")
        print("  Windows: net start MongoDB")
        print("  Linux/Mac: sudo systemctl start mongod")
        return False

def create_env_file():
    """Create .env file if it doesn't exist."""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists() and env_example.exists():
        # Copy .env.example to .env
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ Created .env file from .env.example")
        return True
    elif env_file.exists():
        print("✅ .env file already exists")
        return True
    else:
        print("❌ .env.example not found")
        return False

def install_dependencies():
    """Install Python dependencies if needed."""
    try:
        import flask
        import pymongo
        print("✅ Dependencies are installed")
        return True
    except ImportError:
        print("📦 Installing dependencies...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False

def main():
    """Main startup function."""
    print("🚀 Starting Smart City Management Platform Backend")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('requirements.txt').exists():
        print("❌ requirements.txt not found. Please run this script from the backend directory.")
        sys.exit(1)
    
    # Pre-startup checks
    checks = [
        ("Installing dependencies", install_dependencies),
        ("Creating environment file", create_env_file),
        ("Checking MongoDB connection", check_mongodb)
    ]
    
    for check_name, check_function in checks:
        print(f"\n🔄 {check_name}...")
        if not check_function():
            print(f"❌ {check_name} failed. Please fix the issue and try again.")
            sys.exit(1)
    
    print("\n" + "="*50)
    print("🎉 All checks passed! Starting the backend server...")
    print("="*50)
    
    # Set environment variables
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    
    # Start the Flask application
    try:
        from run import main as run_main
        run_main()
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server failed to start: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
