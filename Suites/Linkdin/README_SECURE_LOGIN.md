# 🔐 Secure ChatGPT Login System

This module provides a secure way to handle ChatGPT login credentials with multiple layers of security and encryption.

## 🛡️ Security Features

### 1. **Environment Variables** (Highest Priority)
- Credentials stored as environment variables
- No local file storage
- Most secure for production environments

### 2. **Encrypted Local Storage** (Medium Priority)
- Credentials encrypted using Fernet (AES-256)
- Automatic key generation and management
- Encrypted files stored locally

### 3. **Interactive Input** (Lowest Priority)
- Secure password input using `getpass`
- No password display on screen
- Optional secure storage after input

## 📁 File Structure

```
Suites/Linkdin/
├── chatgpt_login.py          # Main secure login module
├── test_secure_login.py      # Test script for the login system
├── run_chatgpt_test.py       # Simple ChatGPT test runner
├── install_dependencies.py   # Dependency installer
├── .chatgpt_key             # Encryption key (auto-generated)
├── .chatgpt_credentials     # Encrypted credentials (auto-generated)
└── README_SECURE_LOGIN.md   # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd Suites/Linkdin
python install_dependencies.py
```

Or install manually:
```bash
pip install cryptography selenium webdriver-manager pytest
```

### 2. Set Environment Variables (Recommended)

```bash
# Linux/macOS
export CHATGPT_EMAIL="your-email@example.com"
export CHATGPT_PASSWORD="your-password"

# Windows (PowerShell)
$env:CHATGPT_EMAIL="your-email@example.com"
$env:CHATGPT_PASSWORD="your-password"

# Windows (Command Prompt)
set CHATGPT_EMAIL=your-email@example.com
set CHATGPT_PASSWORD=your-password
```

### 3. Run Secure Login

```bash
python chatgpt_login.py
```

## 🔧 Usage Examples

### Example 1: Using Environment Variables

```python
import os
from chatgpt_login import ChatGPTLogin

# Set environment variables
os.environ['CHATGPT_EMAIL'] = 'your-email@example.com'
os.environ['CHATGPT_PASSWORD'] = 'your-password'

# Create login handler
login_handler = ChatGPTLogin()

# Run login test
success = login_handler.run_login_test()
if success:
    print("Login successful!")
else:
    print("Login failed!")
```

### Example 2: Interactive Input

```python
from chatgpt_login import ChatGPTLogin

# Create login handler
login_handler = ChatGPTLogin()

# This will prompt for credentials interactively
email, password = login_handler.get_credentials()

# Use credentials for login
driver = login_handler.setup_driver()
success = login_handler.login_to_chatgpt(driver, email, password)
```

### Example 3: Secure Storage

```python
from chatgpt_login import SecureCredentialManager

# Create credential manager
cred_manager = SecureCredentialManager()

# Save credentials securely
cred_manager.save_credentials("user@example.com", "securepassword123")

# Load credentials later
credentials = cred_manager.load_credentials()
if credentials:
    email = credentials['email']
    password = credentials['password']

# Clear credentials when done
cred_manager.clear_credentials()
```

## 🔐 Security Best Practices

### 1. **Environment Variables** (Production)
- Use environment variables for production deployments
- Never commit credentials to version control
- Rotate passwords regularly

### 2. **Local Storage** (Development)
- Credentials are encrypted with AES-256
- Key files are separate from credential files
- Automatic cleanup available

### 3. **Interactive Input** (Testing)
- Passwords are hidden during input
- Optional secure storage after input
- Clear credentials after use

## 🛠️ API Reference

### SecureCredentialManager

```python
class SecureCredentialManager:
    def __init__(self, key_file: str = ".chatgpt_key")
    def save_credentials(self, email: str, password: str) -> bool
    def load_credentials(self) -> Optional[Dict[str, str]]
    def clear_credentials(self) -> bool
```

### ChatGPTLogin

```python
class ChatGPTLogin:
    def __init__(self)
    def get_credentials(self) -> Tuple[str, str]
    def login_to_chatgpt(self, driver, email: str, password: str) -> bool
    def setup_driver(self)
    def run_login_test(self) -> bool
```

## 🔍 Error Handling

The system includes comprehensive error handling:

1. **Import Errors**: Graceful fallback with helpful messages
2. **Network Errors**: Retry logic and timeout handling
3. **Login Errors**: Detailed error messages and screenshots
4. **Encryption Errors**: Automatic key regeneration
5. **File Errors**: Safe file operations with error recovery

## 🧪 Testing

### Run All Tests

```bash
# Test secure login functionality
python test_secure_login.py

# Test ChatGPT login (requires credentials)
python chatgpt_login.py

# Run pytest tests
pytest test_chatgpt.py -v
```

### Test Individual Components

```bash
# Test credential manager only
python -c "
from chatgpt_login import SecureCredentialManager
cred_manager = SecureCredentialManager()
print('Credential manager test passed!')
"
```

## 🚨 Security Warnings

1. **Never commit credentials** to version control
2. **Use environment variables** in production
3. **Rotate passwords** regularly
4. **Clear credentials** after use in shared environments
5. **Monitor access logs** for suspicious activity

## 🔄 Troubleshooting

### Common Issues

1. **Chrome not launching**
   - Check if Chrome is installed
   - Verify WebDriver compatibility
   - Try updating Chrome and WebDriver

2. **Login failures**
   - Verify credentials are correct
   - Check for 2FA requirements
   - Ensure network connectivity

3. **Encryption errors**
   - Delete `.chatgpt_key` file to regenerate
   - Check file permissions
   - Verify Python cryptography package

### Error Messages

- `"Credentials not found"`: No saved credentials available
- `"Login failed"`: Invalid credentials or network issues
- `"Chrome driver error"`: WebDriver setup issues
- `"Encryption error"`: Key or file corruption

## 📞 Support

For issues or questions:

1. Check the troubleshooting section
2. Review error logs and screenshots
3. Test with different credentials
4. Verify all dependencies are installed

## 🔄 Version History

- **v1.0.0**: Initial release with secure credential management
- **v1.1.0**: Added environment variable support
- **v1.2.0**: Enhanced error handling and logging
- **v1.3.0**: Added comprehensive testing framework

## 📄 License

This module is part of the YouTube Automation project and follows the same licensing terms.
