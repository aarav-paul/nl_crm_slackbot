import os
import json
import requests
import secrets
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Dict, Optional
from authlib.integrations.requests_client import OAuth2Session

class SalesforceAuth:
    def __init__(self):
        self.client_id = os.environ.get("SALESFORCE_CLIENT_ID")
        self.client_secret = os.environ.get("SALESFORCE_CLIENT_SECRET")
        self.redirect_uri = os.environ.get("SALESFORCE_REDIRECT_URI", "http://localhost:3000/oauth/callback")
        self.auth_url = "https://login.salesforce.com/services/oauth2/authorize"
        self.token_url = "https://login.salesforce.com/services/oauth2/token"
        
        # For development, use test.salesforce.com instead
        if os.environ.get("SALESFORCE_ENVIRONMENT") == "sandbox":
            self.auth_url = "https://test.salesforce.com/services/oauth2/authorize"
            self.token_url = "https://test.salesforce.com/services/oauth2/token"
    
    def generate_pkce_pair(self):
        """Generate PKCE code verifier and challenge"""
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode('utf-8')).digest()
        ).decode('utf-8').rstrip('=')
        return code_verifier, code_challenge
    
    def get_authorization_url(self) -> tuple:
        """Generate the authorization URL for OAuth flow with PKCE"""
        code_verifier, code_challenge = self.generate_pkce_pair()
        
        oauth = OAuth2Session(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            scope="api refresh_token"
        )
        
        authorization_url, state = oauth.create_authorization_url(
            self.auth_url,
            code_challenge=code_challenge,
            code_challenge_method='S256'
        )
        
        return authorization_url, code_verifier
    
    def exchange_code_for_token(self, authorization_code: str, code_verifier: str) -> Dict:
        """Exchange authorization code for access token with PKCE"""
        data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'code_verifier': code_verifier
        }
        
        response = requests.post(self.token_url, data=data)
        response.raise_for_status()
        
        return response.json()
    
    def refresh_access_token(self, refresh_token: str) -> Dict:
        """Refresh the access token using refresh token"""
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        response = requests.post(self.token_url, data=data)
        response.raise_for_status()
        
        return response.json()
    
    def save_credentials(self, token_data: Dict, filename: str = "salesforce_credentials.json"):
        """Save credentials to a file"""
        credentials = {
            'access_token': token_data['access_token'],
            'refresh_token': token_data.get('refresh_token'),
            'instance_url': token_data['instance_url'],
            'expires_at': datetime.now().timestamp() + token_data.get('expires_in', 7200),
            'token_type': token_data.get('token_type', 'Bearer')
        }
        
        with open(filename, 'w') as f:
            json.dump(credentials, f, indent=2)
        
        print(f"✅ Credentials saved to {filename}")
    
    def load_credentials(self, filename: str = "salesforce_credentials.json") -> Optional[Dict]:
        """Load credentials from file"""
        try:
            with open(filename, 'r') as f:
                credentials = json.load(f)
            
            # Check if token is expired
            if datetime.now().timestamp() > credentials['expires_at']:
                print("🔄 Access token expired, refreshing...")
                if credentials.get('refresh_token'):
                    new_token = self.refresh_access_token(credentials['refresh_token'])
                    credentials.update({
                        'access_token': new_token['access_token'],
                        'expires_at': datetime.now().timestamp() + new_token.get('expires_in', 7200)
                    })
                    self.save_credentials(credentials, filename)
                else:
                    print("❌ No refresh token available")
                    return None
            
            return credentials
            
        except FileNotFoundError:
            print(f"❌ Credentials file {filename} not found")
            return None
        except Exception as e:
            print(f"❌ Error loading credentials: {e}")
            return None
    
    def get_valid_credentials(self) -> Optional[Dict]:
        """Get valid credentials, refreshing if necessary"""
        credentials = self.load_credentials()
        if credentials:
            return credentials
        else:
            print("🔐 No valid credentials found. Please run the OAuth flow.")
            return None 