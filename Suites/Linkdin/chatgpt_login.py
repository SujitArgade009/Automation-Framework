#!/usr/bin/env python3
"""
Secure ChatGPT Login Module
Handles credentials securely using environment variables, encryption, and secure storage.
"""

import os
import sys
import json
import base64
import getpass
from pathlib import Path
from cryptography.fernet import Fernet
import time
from typing import Optional, Dict, Tuple

# Selenium imports moved here for clarity
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class SecureCredentialManager:
    """Secure credential manager for ChatGPT login."""

    def __init__(self, key_file: str = ".chatgpt_key"):
        self.key_file = Path(key_file)
        self.credentials_file = Path(".chatgpt_credentials")
        self.key = self._load_or_generate_key()
        self.cipher_suite = Fernet(self.key)

    def _load_or_generate_key(self) -> bytes:
        """Load existing key or generate a new one."""
        if self.key_file.exists():
            try:
                with open(self.key_file, 'rb') as f:
                    return f.read()
            except Exception as e:
                print(f"Warning: Could not load existing key: {e}")

        # Generate new key
        key = Fernet.generate_key()
        try:
            with open(self.key_file, 'wb') as f:
                f.write(key)
            print(f"✅ Generated new encryption key: {self.key_file}")
        except Exception as e:
            print(f"Warning: Could not save key file: {e}")

        return key

    def _encrypt_credentials(self, credentials: Dict[str, str]) -> str:
        """Encrypt credentials."""
        json_data = json.dumps(credentials)
        encrypted_data = self.cipher_suite.encrypt(json_data.encode())
        return base64.b64encode(encrypted_data).decode()

    def _decrypt_credentials(self, encrypted_data: str) -> Dict[str, str]:
        """Decrypt credentials."""
        encrypted_bytes = base64.b64decode(encrypted_data.encode())
        decrypted_data = self.cipher_suite.decrypt(encrypted_bytes)
        return json.loads(decrypted_data.decode())

    def save_credentials(self, email: str, password: str) -> bool:
        """Save credentials securely."""
        try:
            credentials = {
                'email': email,
                'password': password,
                'timestamp': time.time()
            }

            encrypted_credentials = self._encrypt_credentials(credentials)

            with open(self.credentials_file, 'w') as f:
                f.write(encrypted_credentials)

            print(f"✅ Credentials saved securely to {self.credentials_file}")
            return True

        except Exception as e:
            print(f"❌ Failed to save credentials: {e}")
            return False

    def load_credentials(self) -> Optional[Dict[str, str]]:
        """Load credentials securely."""
        if not self.credentials_file.exists():
            return None

        try:
            with open(self.credentials_file, 'r') as f:
                encrypted_data = f.read().strip()

            credentials = self._decrypt_credentials(encrypted_data)
            print(f"✅ Loaded credentials for: {credentials['email']}")
            return credentials

        except Exception as e:
            print(f"❌ Failed to load credentials: {e}")
            return None

    def clear_credentials(self) -> bool:
        """Clear saved credentials."""
        try:
            if self.credentials_file.exists():
                self.credentials_file.unlink()
                print("✅ Credentials cleared")
            return True
        except Exception as e:
            print(f"❌ Failed to clear credentials: {e}")
            return False


class ChatGPTLogin:
    """ChatGPT login handler with secure credential management."""

    def __init__(self):
        self.credential_manager = SecureCredentialManager()
        self.driver = None

    def get_credentials(self) -> Tuple[str, str]:
        """
        Get credentials from environment variables, secure storage, or user input.
        Priority: Environment Variables > Secure Storage > User Input
        """
        # Try environment variables first
        email = os.getenv('CHATGPT_EMAIL')
        password = os.getenv('CHATGPT_PASSWORD')

        if email and password:
            print("✅ Using credentials from environment variables")
            return email, password

        # Try secure storage
        credentials = self.credential_manager.load_credentials()
        if credentials:
            print("✅ Using credentials from secure storage")
            return credentials['email'], credentials['password']

        # Get from user input
        print("🔐 Please enter your ChatGPT credentials:")
        email = input("Email: ").strip()
        password = getpass.getpass("Password: ").strip()

        # Ask if user wants to save credentials
        save_choice = input("Save credentials securely? (y/N): ").strip().lower()
        if save_choice in ['y', 'yes']:
            self.credential_manager.save_credentials(email, password)

        return email, password

    def login_to_chatgpt(self, driver, email: str, password: str) -> bool:
        """
        Login to ChatGPT using provided credentials.
        """
        try:
            print("🔐 Logging into ChatGPT...")

            # Navigate to ChatGPT login page (adjust URL if needed)
            driver.get("https://auth.openai.com/login")

            wait = WebDriverWait(driver, 20)

            # Wait for email input field by name or placeholder
            email_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
            email_input.clear()
            email_input.send_keys(email)

            # Click Continue
            continue_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            continue_button.click()

            # Wait for password input
            password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_input.clear()
            password_input.send_keys(password)

            # Click Continue again
            continue_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            continue_button.click()

            # Wait for navigation or error message
            wait.until(lambda d: "chat.openai.com/c" in d.current_url 
                                or "incorrect" in d.page_source.lower() 
                                or "error" in d.page_source.lower())

            if "chat.openai.com/c" in driver.current_url:
                print("✅ Successfully logged into ChatGPT!")
                return True
            else:
                print("❌ Login failed. Please check your credentials.")
                return False

        except Exception as e:
            print(f"❌ Error during login process: {e}")
            return False

    def setup_driver(self):
        """Setup Chrome WebDriver with proper configuration."""
        print("Setting up Chrome WebDriver...")

        options = webdriver.ChromeOptions()

        # Chrome options for automation
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")

        # Remove automation flags
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)

            # Remove webdriver property to avoid detection
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.maximize_window()

            print("Chrome WebDriver setup successful!")
            return self.driver

        except Exception as e:
            print(f"Error setting up Chrome driver: {e}")
            raise

    def run_login_test(self) -> bool:
        """Run the complete login test."""
        try:
            # Setup driver
            driver = self.setup_driver()

            # Get credentials
            email, password = self.get_credentials()

            # Login to ChatGPT
            success = self.login_to_chatgpt(driver, email, password)

            if success:
                print("🎉 Login test completed successfully!")
                # Keep browser open for a while to see the result
                time.sleep(5)

            return success

        except Exception as e:
            print(f"❌ Error during login test: {e}")
            return False

        finally:
            if self.driver:
                print("Closing Chrome WebDriver...")
                self.driver.quit()


def main():
    """Main function to run the ChatGPT login test."""
    print("🚀 Starting ChatGPT Login Test...")

    login_handler = ChatGPTLogin()
    success = login_handler.run_login_test()

    if success:
        print("🎉 Test completed successfully!")
        sys.exit(0)
    else:
        print("💥 Test failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
