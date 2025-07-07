import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional
from simple_salesforce import Salesforce

class SalesforceSimpleAuth:
    def __init__(self):
        self.username = os.environ.get("SALESFORCE_USERNAME")
        self.password = os.environ.get("SALESFORCE_PASSWORD")
        self.security_token = os.environ.get("SALESFORCE_SECURITY_TOKEN")
        self.domain = os.environ.get("SALESFORCE_DOMAIN", "login")  # login or test
        
    def authenticate(self) -> Optional[Salesforce]:
        """
        Authenticate using username/password
        """
        try:
            print("🔐 Authenticating with Salesforce...")
            
            # Use sandbox if specified
            if self.domain == "test":
                sf = Salesforce(
                    username=self.username,
                    password=self.password,
                    security_token=self.security_token,
                    domain='test'
                )
            else:
                sf = Salesforce(
                    username=self.username,
                    password=self.password,
                    security_token=self.security_token
                )
            
            print("✅ Successfully authenticated with Salesforce!")
            print(f"🏢 Instance URL: {sf.base_url}")
            print(f"👤 User ID: {sf.user_id}")
            
            return sf
            
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return None
    
    def test_connection(self) -> bool:
        """
        Test the Salesforce connection
        """
        try:
            sf = self.authenticate()
            if sf:
                # Try a simple query to test the connection
                result = sf.query("SELECT Id, Name FROM User LIMIT 1")
                print(f"✅ Connection test successful! Found {len(result['records'])} user(s)")
                return True
            return False
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False
    
    def save_connection_info(self, sf: Salesforce, filename: str = "salesforce_connection.json"):
        """
        Save connection information for later use
        """
        connection_info = {
            'instance_url': sf.base_url,
            'user_id': sf.user_id,
            'authenticated_at': datetime.now().isoformat(),
            'domain': self.domain
        }
        
        with open(filename, 'w') as f:
            json.dump(connection_info, f, indent=2)
        
        print(f"✅ Connection info saved to {filename}")
    
    def get_salesforce_instance(self) -> Optional[Salesforce]:
        """
        Get an authenticated Salesforce instance
        """
        return self.authenticate() 