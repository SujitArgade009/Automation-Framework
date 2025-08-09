#!/usr/bin/env python3
"""
Install dependencies for ChatGPT test.
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def main():
    """Install all required dependencies."""
    print("Installing dependencies for ChatGPT test...")
    
    # List of required packages
    packages = [
        "selenium==4.15.2",
        "webdriver-manager==4.0.1",
        "pytest==7.4.3"
    ]
    
    success_count = 0
    total_packages = len(packages)
    
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n📊 Installation Summary:")
    print(f"Successfully installed: {success_count}/{total_packages} packages")
    
    if success_count == total_packages:
        print("🎉 All dependencies installed successfully!")
        print("\nYou can now run the test with:")
        print("  python run_chatgpt_test.py")
        print("  or")
        print("  pytest test_chatgpt.py -v")
    else:
        print("⚠️  Some dependencies failed to install. Please check the errors above.")

if __name__ == "__main__":
    main()
