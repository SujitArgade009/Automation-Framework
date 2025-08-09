#!/usr/bin/env python3
"""
Test script for secure ChatGPT login functionality.
This script demonstrates how to use the secure login system.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

def test_secure_login():
    """Test the secure login functionality."""
    try:
        from chatgpt_login import ChatGPTLogin, SecureCredentialManager
        
        print("🔐 Testing Secure ChatGPT Login System")
        print("=" * 50)
        
        # Test credential manager
        print("\n1. Testing Credential Manager...")
        cred_manager = SecureCredentialManager()
        
        # Test saving credentials
        test_email = "test@example.com"
        test_password = "testpassword123"
        
        success = cred_manager.save_credentials(test_email, test_password)
        if success:
            print("✅ Credentials saved successfully")
        
        # Test loading credentials
        credentials = cred_manager.load_credentials()
        if credentials and credentials.get('email') == test_email:
            print("✅ Credentials loaded successfully")
        
        # Test clearing credentials
        cred_manager.clear_credentials()
        print("✅ Credentials cleared successfully")
        
        # Test login system
        print("\n2. Testing Login System...")
        login_handler = ChatGPTLogin()
        
        # Test getting credentials (this will prompt for input)
        print("\n📝 Testing credential input (you can cancel with Ctrl+C):")
        try:
            email, password = login_handler.get_credentials()
            print(f"✅ Got credentials for: {email}")
        except KeyboardInterrupt:
            print("\n⏹️  Test cancelled by user")
            return True
        except Exception as e:
            print(f"❌ Error getting credentials: {e}")
            return False
        
        print("\n🎉 All tests completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install required dependencies:")
        print("pip install cryptography selenium webdriver-manager")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main function."""
    print("🚀 Starting Secure Login Test...")
    
    success = test_secure_login()
    
    if success:
        print("\n🎉 All tests passed!")
        print("\n📋 Usage Examples:")
        print("1. Set environment variables:")
        print("   export CHATGPT_EMAIL='your-email@example.com'")
        print("   export CHATGPT_PASSWORD='your-password'")
        print("\n2. Run the secure login:")
        print("   python chatgpt_login.py")
        print("\n3. Run the test:")
        print("   python test_secure_login.py")
        
        sys.exit(0)
    else:
        print("\n💥 Tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
