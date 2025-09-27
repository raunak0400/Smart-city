#!/usr/bin/env python3
"""
Setup script for Smart City Management Platform Backend
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_requirements():
    """Check if required software is installed."""
    print("🔍 Checking requirements...")
    
    requirements = {
        'python': 'python --version',
        'pip': 'pip --version',
        'mongodb': 'mongod --version'
    }
    
    missing = []
    for name, command in requirements.items():
        try:
            subprocess.run(command, shell=True, check=True, capture_output=True)
            print(f"✅ {name} is installed")
        except subprocess.CalledProcessError:
            print(f"❌ {name} is not installed or not in PATH")
            missing.append(name)
    
    if missing:
        print(f"\n⚠️  Missing requirements: {', '.join(missing)}")
        print("Please install the missing software before continuing.")
        return False
    
    return True

def setup_virtual_environment():
    """Set up Python virtual environment."""
    venv_path = Path('venv')
    
    if venv_path.exists():
        print("📁 Virtual environment already exists")
        return True
    
    return run_command('python -m venv venv', 'Creating virtual environment')

def install_dependencies():
    """Install Python dependencies."""
    if os.name == 'nt':  # Windows
        pip_command = 'venv\\Scripts\\pip install -r requirements.txt'
    else:  # Unix/Linux/macOS
        pip_command = 'venv/bin/pip install -r requirements.txt'
    
    return run_command(pip_command, 'Installing Python dependencies')

def setup_environment_file():
    """Set up environment configuration file."""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if env_file.exists():
        print("📁 .env file already exists")
        return True
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from .env.example")
        print("⚠️  Please edit .env file with your configuration")
        return True
    else:
        print("❌ .env.example file not found")
        return False

def setup_directories():
    """Create necessary directories."""
    directories = ['logs', 'uploads', 'temp']
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")
    
    return True

def setup_database():
    """Set up MongoDB database."""
    print("\n🗄️  Setting up MongoDB database...")
    
    # Check if MongoDB is running
    try:
        subprocess.run('mongosh --eval "db.runCommand({ping: 1})"', 
                      shell=True, check=True, capture_output=True)
        print("✅ MongoDB is running")
    except subprocess.CalledProcessError:
        print("❌ MongoDB is not running. Please start MongoDB service.")
        return False
    
    # Initialize database with sample data
    init_script = Path('mongo-init.js')
    if init_script.exists():
        command = f'mongosh smart_city_db {init_script}'
        return run_command(command, 'Initializing database with sample data')
    else:
        print("⚠️  mongo-init.js not found, skipping database initialization")
        return True

def run_tests():
    """Run basic tests to verify setup."""
    print("\n🧪 Running basic tests...")
    
    if os.name == 'nt':  # Windows
        python_command = 'venv\\Scripts\\python'
    else:  # Unix/Linux/macOS
        python_command = 'venv/bin/python'
    
    # Test imports
    test_command = f'{python_command} -c "import flask, pymongo, redis; print(\'All imports successful\')"'
    return run_command(test_command, 'Testing Python imports')

def main():
    """Main setup function."""
    print("🚀 Smart City Management Platform Backend Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('requirements.txt').exists():
        print("❌ requirements.txt not found. Please run this script from the backend directory.")
        sys.exit(1)
    
    steps = [
        ("Checking requirements", check_requirements),
        ("Setting up virtual environment", setup_virtual_environment),
        ("Installing dependencies", install_dependencies),
        ("Setting up environment file", setup_environment_file),
        ("Creating directories", setup_directories),
        ("Setting up database", setup_database),
        ("Running tests", run_tests)
    ]
    
    failed_steps = []
    
    for step_name, step_function in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        if not step_function():
            failed_steps.append(step_name)
            response = input(f"❌ {step_name} failed. Continue anyway? (y/N): ")
            if response.lower() != 'y':
                print("Setup aborted.")
                sys.exit(1)
    
    print("\n" + "="*50)
    if failed_steps:
        print(f"⚠️  Setup completed with warnings. Failed steps: {', '.join(failed_steps)}")
    else:
        print("🎉 Setup completed successfully!")
    
    print("\nNext steps:")
    print("1. Edit .env file with your configuration")
    print("2. Start MongoDB service")
    print("3. Run the application:")
    
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\python run.py")
    else:  # Unix/Linux/macOS
        print("   venv/bin/python run.py")
    
    print("\nFor production deployment:")
    print("   docker-compose up -d")

if __name__ == '__main__':
    main()
