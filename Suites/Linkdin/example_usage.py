#!/usr/bin/env python3
"""
Example usage of the secure ChatGPT login system.
This script demonstrates different ways to handle credentials securely.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

def example_environment_variables():
    """Example using environment variables."""
    print("\n🔐 Example 1: Environment Variables")
    print("=" * 40)
    
    # Set environment variables (in real usage, these would be set externally)
    os.environ['CHATGPT_EMAIL'] = 'test@example.com'
    os.environ['CHATGPT_PASSWORD'] = 'testpassword123'
    
    from chatgpt_login import ChatGPTLogin
    
    login_handler = ChatGPTLogin()
    email, password = login_handler.get_credentials()
    
    print(f"✅ Got credentials from environment variables: {email}")
    print("Note: In production, set these using your system's environment variable mechanism")

def example_secure_storage():
    """Example using secure storage."""
    print("\n🔐 Example 2: Secure Storage")
    print("=" * 40)
    
    from chatgpt_login import SecureCredentialManager
    
    # Create credential manager
    cred_manager = SecureCredentialManager()
    
    # Save credentials securely
    email = "user@example.com"
    password = "securepassword123"
    
    success = cred_manager.save_credentials(email, password)
    if success:
        print(f"✅ Credentials saved securely for: {email}")
    
    # Load credentials
    credentials = cred_manager.load_credentials()
    if credentials:
        print(f"✅ Credentials loaded for: {credentials['email']}")
    
    # Clear credentials (clean up)
    cred_manager.clear_credentials()
    print("✅ Credentials cleared")

def example_interactive_input():
    """Example using interactive input."""
    print("\n🔐 Example 3: Interactive Input")
    print("=" * 40)
    
    from chatgpt_login import ChatGPTLogin
    
    login_handler = ChatGPTLogin()
    
    print("This example would prompt for credentials interactively.")
    print("For demonstration, we'll skip the actual input.")
    
    # In real usage, this would prompt for credentials
    print("✅ Interactive input example (skipped for demo)")

def example_full_login_flow():
    """Example of the full login flow."""
    print("\n🔐 Example 4: Full Login Flow")
    print("=" * 40)
    
    from chatgpt_login import ChatGPTLogin
    
    # Create login handler
    login_handler = ChatGPTLogin()
    
    print("This example demonstrates the complete login flow:")
    print("1. Setup Chrome WebDriver")
    print("2. Get credentials (from env vars, storage, or input)")
    print("3. Navigate to ChatGPT login page")
    print("4. Enter credentials")
    print("5. Handle login success/failure")
    print("6. Clean up resources")
    
    print("\nNote: This would actually perform the login (requires real credentials)")
    print("Run 'python chatgpt_login.py' to test the actual login flow")

def main():
    """Main function to run all examples."""
    print("🚀 ChatGPT Secure Login - Usage Examples")
    print("=" * 50)
    
    try:
        # Run examples
        example_environment_variables()
        example_secure_storage()
        example_interactive_input()
        example_full_login_flow()
        
        print("\n🎉 All examples completed!")
        print("\n📋 Next Steps:")
        print("1. Set up your environment variables:")
        print("   export CHATGPT_EMAIL='your-email@example.com'")
        print("   export CHATGPT_PASSWORD='your-password'")
        print("\n2. Test the secure login:")
        print("   python chatgpt_login.py")
        print("\n3. Run the test suite:")
        print("   python test_secure_login.py")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install required dependencies:")
        print("pip install cryptography selenium webdriver-manager")
    except Exception as e:
        print(f"❌ Example failed: {e}")

if __name__ == "__main__":
    main()
