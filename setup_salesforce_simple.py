#!/usr/bin/env python3
"""
Salesforce Simple Authentication Setup Script
This script helps you set up username/password authentication with Salesforce.
"""

import os
from dotenv import load_dotenv
from salesforce_simple_auth import SalesforceSimpleAuth

def main():
    load_dotenv()
    
    print("🚀 Salesforce Simple Authentication Setup")
    print("=" * 50)
    
    # Check if environment variables are set
    username = os.environ.get("SALESFORCE_USERNAME")
    password = os.environ.get("SALESFORCE_PASSWORD")
    security_token = os.environ.get("SALESFORCE_SECURITY_TOKEN")
    
    if not username or not password or not security_token:
        print("❌ Missing Salesforce credentials in .env file")
        print("\nPlease add these to your .env file:")
        print("SALESFORCE_USERNAME=your_username_here")
        print("SALESFORCE_PASSWORD=your_password_here")
        print("SALESFORCE_SECURITY_TOKEN=your_security_token_here")
        print("SALESFORCE_DOMAIN=login  # or 'test' for sandbox")
        print()
        print("📝 To get your security token:")
        print("1. Go to Setup → Users → Your User")
        print("2. Click 'Reset My Security Token'")
        print("3. Check your email for the token")
        return
    
    # Initialize Salesforce auth
    sf_auth = SalesforceSimpleAuth()
    
    print("✅ Environment variables loaded")
    print(f"👤 Username: {username}")
    print(f"🔗 Domain: {sf_auth.domain}")
    print()
    
    # Test the connection
    print("🧪 Testing Salesforce connection...")
    if sf_auth.test_connection():
        print()
        print("🎉 Authentication successful!")
        print("✅ You can now use Salesforce API in your bot!")
        
        # Save connection info
        sf = sf_auth.get_salesforce_instance()
        if sf:
            sf_auth.save_connection_info(sf)
        
    else:
        print()
        print("❌ Authentication failed!")
        print("\nTroubleshooting tips:")
        print("- Check your username and password")
        print("- Verify your security token is correct")
        print("- Make sure your user has API access")
        print("- If using sandbox, set SALESFORCE_DOMAIN=test")

if __name__ == "__main__":
    main() 