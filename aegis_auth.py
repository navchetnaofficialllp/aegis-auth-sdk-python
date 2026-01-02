"""
Aegis Auth Python SDK
Official Python SDK for Aegis Authentication System

Aegis Auth is a unified identity management system providing memory-safe 
Rust-based authentication. Consolidation of disparate identity providers 
into a single canonical source.

Aegis Auth by Navchetna Technologies.
Securing the future of decentralized identity.
© 2026 Standard Core v3.
"""

import requests
import json
import time
from typing import Dict, Any, Optional, List, Callable
from urllib.parse import urljoin
import threading


class AegisAuthError(Exception):
    """Base exception for Aegis Auth SDK"""
    pass


class AegisAuth:
    """
    Aegis Authentication SDK for Python
    
    Provides comprehensive authentication methods including:
    - Email/password authentication
    - WebAuthn/Passkeys
    - Multi-factor authentication (MFA)
    - Password reset functionality
    - Token management with auto-refresh
    """
    
    def __init__(self, api_key: str, base_url: str = None):
        """
        Initialize Aegis Auth SDK
        
        Args:
            api_key (str): Your Aegis API key
            base_url (str, optional): Custom Aegis instance URL
        """
        if not api_key:
            raise AegisAuthError("API key is required")
            
        self.api_key = api_key
        self.base_url = base_url or "https://05card1j5b.execute-api.ap-south-1.amazonaws.com/prod"
        self.access_token = None
        self.refresh_token = None
        self.user = None
        self.token_expiry = None
        self.session = requests.Session()
        self._refresh_timer = None
        self._event_handlers = {
            'login': [],
            'logout': [],
            'token_refresh': [],
            'error': []
        }
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'X-API-Key': self.api_key
        })
    
    def on(self, event: str, callback: Callable):
        """Register event handler"""
        if event in self._event_handlers:
            self._event_handlers[event].append(callback)
    
    def _emit(self, event: str, data: Any = None):
        """Emit event to registered handlers"""
        if event in self._event_handlers:
            for handler in self._event_handlers[event]:
                try:
                    handler(data)
                except Exception as e:
                    print(f"Event handler error: {e}")
    
    def _request(self, method: str, endpoint: str, data: Dict = None, skip_auth: bool = False) -> Dict[str, Any]:
        """Make HTTP request to Aegis API"""
        url = urljoin(self.base_url, endpoint)
        headers = {}
        
        if self.access_token and not skip_auth:
            headers['Authorization'] = f'Bearer {self.access_token}'
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, headers=headers)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, headers=headers)
            elif method.upper() == 'PATCH':
                response = self.session.patch(url, json=data, headers=headers)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, headers=headers)
            else:
                raise AegisAuthError(f"Unsupported HTTP method: {method}")
            
            if response.status_code >= 400:
                error_data = response.json() if response.content else {}
                error_msg = error_data.get('message', f'HTTP {response.status_code}')
                self._emit('error', {'error': error_msg, 'endpoint': endpoint})
                raise AegisAuthError(error_msg)
            
            return response.json()
            
        except requests.RequestException as e:
            self._emit('error', {'error': str(e), 'endpoint': endpoint})
            raise AegisAuthError(f"Request failed: {str(e)}")
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        Authenticate user with email and password
        
        Args:
            email (str): User email
            password (str): User password
            
        Returns:
            Dict containing user data and tokens
        """
        try:
            response = self._request('POST', '/auth/login', {
                'email': email,
                'password': password
            }, skip_auth=True)
            
            self._set_tokens(response['data'])
            self._emit('login', self.user)
            return response['data']
            
        except Exception as e:
            raise AegisAuthError(f"Login failed: {str(e)}")
    
    def register(self, email: str, password: str, first_name: str = None, last_name: str = None) -> Dict[str, Any]:
        """
        Register new user
        
        Args:
            email (str): User email
            password (str): User password
            first_name (str, optional): User first name
            last_name (str, optional): User last name
            
        Returns:
            Dict containing registration response
        """
        data = {
            'email': email,
            'password': password
        }
        
        if first_name:
            data['first_name'] = first_name
        if last_name:
            data['last_name'] = last_name
        
        try:
            response = self._request('POST', '/auth/register', data, skip_auth=True)
            return response['data']
        except Exception as e:
            raise AegisAuthError(f"Registration failed: {str(e)}")
    
    def logout(self):
        """Logout user and clear tokens"""
        try:
            if self.access_token:
                self._request('POST', '/auth/logout')
        except Exception as e:
            print(f"Logout request failed: {e}")
        finally:
            self._clear_tokens()
            self._emit('logout')
    
    def refresh_access_token(self) -> Dict[str, Any]:
        """
        Refresh access token using refresh token
        
        Returns:
            Dict containing new tokens
        """
        if not self.refresh_token:
            raise AegisAuthError("No refresh token available")
        
        try:
            response = self._request('POST', '/auth/refresh', {
                'refresh_token': self.refresh_token
            }, skip_auth=True)
            
            self._set_tokens(response['data'])
            self._emit('token_refresh', self.user)
            return response['data']
            
        except Exception as e:
            self._clear_tokens()
            raise AegisAuthError(f"Token refresh failed: {str(e)}")
    
    def forgot_password(self, email: str) -> Dict[str, Any]:
        """
        Request password reset
        
        Args:
            email (str): User email
            
        Returns:
            Dict containing response
        """
        try:
            response = self._request('POST', '/auth/forgot-password', {
                'email': email
            }, skip_auth=True)
            return response['data']
        except Exception as e:
            raise AegisAuthError(f"Password reset request failed: {str(e)}")
    
    def reset_password(self, token: str, new_password: str) -> Dict[str, Any]:
        """
        Reset password with token
        
        Args:
            token (str): Reset token
            new_password (str): New password
            
        Returns:
            Dict containing response
        """
        try:
            response = self._request('POST', '/auth/reset-password', {
                'token': token,
                'new_password': new_password
            }, skip_auth=True)
            return response['data']
        except Exception as e:
            raise AegisAuthError(f"Password reset failed: {str(e)}")
    
    def get_profile(self) -> Dict[str, Any]:
        """
        Get user profile
        
        Returns:
            Dict containing user profile
        """
        try:
            response = self._request('GET', '/auth/profile')
            return response['data']
        except Exception as e:
            raise AegisAuthError(f"Failed to get profile: {str(e)}")
    
    def update_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update user profile
        
        Args:
            profile_data (Dict): Profile data to update
            
        Returns:
            Dict containing updated profile
        """
        try:
            response = self._request('PATCH', '/auth/profile', profile_data)
            return response['data']
        except Exception as e:
            raise AegisAuthError(f"Profile update failed: {str(e)}")
    
    def enable_mfa(self) -> Dict[str, Any]:
        """
        Enable multi-factor authentication
        
        Returns:
            Dict containing MFA setup data (QR code, secret, backup codes)
        """
        try:
            response = self._request('POST', '/auth/mfa/enable')
            return response['data']
        except Exception as e:
            raise AegisAuthError(f"MFA enable failed: {str(e)}")
    
    def verify_mfa(self, code: str) -> Dict[str, Any]:
        """
        Verify MFA code
        
        Args:
            code (str): MFA code
            
        Returns:
            Dict containing verification response
        """
        try:
            response = self._request('POST', '/auth/mfa/verify', {'code': code})
            return response['data']
        except Exception as e:
            raise AegisAuthError(f"MFA verification failed: {str(e)}")
    
    def disable_mfa(self, code: str) -> Dict[str, Any]:
        """
        Disable multi-factor authentication
        
        Args:
            code (str): MFA code
            
        Returns:
            Dict containing response
        """
        try:
            response = self._request('POST', '/auth/mfa/disable', {'code': code})
            return response['data']
        except Exception as e:
            raise AegisAuthError(f"MFA disable failed: {str(e)}")
    
    def _set_tokens(self, auth_data: Dict[str, Any]):
        """Set authentication tokens and user data"""
        self.access_token = auth_data.get('access_token')
        self.refresh_token = auth_data.get('refresh_token')
        self.user = auth_data.get('user')
        
        expires_in = auth_data.get('expires_in', 900)  # Default 15 minutes
        self.token_expiry = time.time() + expires_in
        
        self._setup_token_refresh()
    
    def _clear_tokens(self):
        """Clear all authentication data"""
        self.access_token = None
        self.refresh_token = None
        self.user = None
        self.token_expiry = None
        
        if self._refresh_timer:
            self._refresh_timer.cancel()
            self._refresh_timer = None
    
    def _setup_token_refresh(self):
        """Setup automatic token refresh"""
        if self._refresh_timer:
            self._refresh_timer.cancel()
        
        if self.token_expiry:
            # Refresh 1 minute before expiry
            refresh_time = max(0, self.token_expiry - time.time() - 60)
            if refresh_time > 0:
                self._refresh_timer = threading.Timer(refresh_time, self._auto_refresh)
                self._refresh_timer.start()
    
    def _auto_refresh(self):
        """Automatically refresh token"""
        try:
            self.refresh_access_token()
        except Exception as e:
            self._emit('error', {'error': str(e), 'type': 'token_refresh'})
    
    def is_authenticated(self) -> bool:
        """
        Check if user is authenticated
        
        Returns:
            bool: True if authenticated, False otherwise
        """
        return bool(
            self.access_token and 
            self.token_expiry and 
            time.time() < self.token_expiry
        )
    
    def get_user(self) -> Optional[Dict[str, Any]]:
        """
        Get current user data
        
        Returns:
            Dict containing user data or None
        """
        return self.user
    
    def get_access_token(self) -> Optional[str]:
        """
        Get current access token
        
        Returns:
            str: Access token or None
        """
        return self.access_token


# Convenience function
def create_client(api_key: str, base_url: str = None) -> AegisAuth:
    """
    Create Aegis Auth client
    
    Args:
        api_key (str): Your Aegis API key
        base_url (str, optional): Custom Aegis instance URL
        
    Returns:
        AegisAuth: Configured client instance
    """
    return AegisAuth(api_key, base_url)


__version__ = "1.0.0"
__all__ = ["AegisAuth", "AegisAuthError", "create_client"]