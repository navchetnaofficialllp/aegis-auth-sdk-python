# Aegis Auth - Python SDK

**Aegis Auth is a unified identity management system providing memory-safe Rust-based authentication. Consolidation of disparate identity providers into a single canonical source.**

*Aegis Auth by Navchetna Technologies.*  
*Securing the future of decentralized identity.*  
*© 2026 Standard Core v3.*

---

Official Python SDK for the Aegis Authentication System. Supports traditional authentication, WebAuthn/Passkeys, MFA, and more.

## Installation

```bash
pip install aegis-auth-navchetna
```

## Quick Start

```python
from aegis_auth import AegisAuth

# Initialize the client
aegis = AegisAuth(api_key="your-api-key-here")

# Login
try:
    response = aegis.login("user@example.com", "password")
    print(f"Logged in: {response['user']['email']}")
except Exception as e:
    print(f"Login failed: {e}")

# Check authentication status
if aegis.is_authenticated():
    print("User is authenticated")
    user = aegis.get_user()
    print(f"Current user: {user['email']}")
```

## Authentication Methods

### Email/Password Authentication

```python
# Login
response = aegis.login("user@example.com", "password")
print(f"Access token: {response['access_token']}")

# Register
response = aegis.register(
    email="user@example.com",
    password="securePassword123",
    first_name="John",
    last_name="Doe"
)
print("Registration successful")

# Logout
aegis.logout()
```

### Password Reset

```python
# Request password reset
aegis.forgot_password("user@example.com")
print("Password reset email sent")

# Reset password with token
aegis.reset_password("reset-token", "newPassword123")
print("Password reset successful")
```

### Multi-Factor Authentication (MFA)

```python
# Enable MFA
mfa_data = aegis.enable_mfa()
print(f"QR Code: {mfa_data['qr_code']}")
print(f"Secret: {mfa_data['secret']}")
print(f"Backup codes: {mfa_data['backup_codes']}")

# Verify MFA code
aegis.verify_mfa("123456")
print("MFA verified")

# Disable MFA
aegis.disable_mfa("123456")
print("MFA disabled")
```

### User Profile Management

```python
# Get profile
profile = aegis.get_profile()
print(f"User profile: {profile}")

# Update profile
updated_profile = aegis.update_profile({
    "first_name": "Jane",
    "last_name": "Smith",
    "phone": "+1234567890"
})
print("Profile updated")
```

## Event Handling

```python
# Register event handlers
def on_login(user):
    print(f"User logged in: {user['email']}")

def on_logout():
    print("User logged out")

def on_error(error_data):
    print(f"Error: {error_data['error']}")

aegis.on('login', on_login)
aegis.on('logout', on_logout)
aegis.on('error', on_error)
```

## Token Management

```python
# Check authentication status
if aegis.is_authenticated():
    print("User is authenticated")

# Get current user
user = aegis.get_user()
if user:
    print(f"Current user: {user['email']}")

# Get access token
token = aegis.get_access_token()
if token:
    print(f"Access token: {token}")

# Manual token refresh
try:
    response = aegis.refresh_access_token()
    print("Token refreshed successfully")
except Exception as e:
    print(f"Token refresh failed: {e}")
```

## Configuration

```python
from aegis_auth import AegisAuth

# Basic configuration
aegis = AegisAuth(api_key="your-api-key")

# Custom base URL
aegis = AegisAuth(
    api_key="your-api-key",
    base_url="https://your-aegis-instance.com"
)

# Using convenience function
from aegis_auth import create_client

aegis = create_client(api_key="your-api-key")
```

## Error Handling

```python
from aegis_auth import AegisAuth, AegisAuthError

aegis = AegisAuth(api_key="your-api-key")

try:
    aegis.login("user@example.com", "wrongpassword")
except AegisAuthError as e:
    if "Invalid credentials" in str(e):
        print("Please check your email and password")
    elif "Network" in str(e):
        print("Please check your internet connection")
    else:
        print(f"Authentication error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Advanced Usage

### Custom Request Headers

```python
# The SDK automatically handles API key and authorization headers
# For custom headers, you can extend the session:

aegis.session.headers.update({
    'Custom-Header': 'value'
})
```

### Automatic Token Refresh

The SDK automatically refreshes tokens 1 minute before expiry. You can listen for refresh events:

```python
def on_token_refresh(user):
    print(f"Token refreshed for user: {user['email']}")

aegis.on('token_refresh', on_token_refresh)
```

## Requirements

- Python 3.7+
- requests >= 2.25.0

## Security Best Practices

1. **Never expose your API key** in client-side code or version control
2. **Use environment variables** to store sensitive configuration
3. **Implement proper error handling** to avoid exposing sensitive information
4. **Use HTTPS** in production environments
5. **Implement logout functionality** to clear tokens when users sign out

## Support

- Documentation: [https://aegis.navchetna.tech](https://aegis.navchetna.tech)
- Issues: [https://github.com/navchetnaofficialllp/aegis-auth-sdk-python/issues](https://github.com/navchetnaofficialllp/aegis-auth-sdk-python/issues)
- Email: hello@navchetna.tech

---

**Aegis Auth by Navchetna Technologies**  
*Securing the future of decentralized identity*  
© 2026 Standard Core v3

## License

MIT License - see LICENSE file for details.