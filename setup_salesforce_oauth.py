#!/usr/bin/env python3
"""
Salesforce OAuth Setup Script
This script helps you set up OAuth authentication with Salesforce.
"""

import os
import webbrowser
from dotenv import load_dotenv
from salesforce_auth import SalesforceAuth

def main():
    load_dotenv()
    
    print("🚀 Salesforce OAuth Setup")
    print("=" * 50)
    
    # Check if environment variables are set
    client_id = os.environ.get("SALESFORCE_CLIENT_ID")
    client_secret = os.environ.get("SALESFORCE_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("❌ Missing Salesforce credentials in .env file")
        print("\nPlease add these to your .env file:")
        print("SALESFORCE_CLIENT_ID=your_consumer_key_here")
        print("SALESFORCE_CLIENT_SECRET=your_consumer_secret_here")
        print("SALESFORCE_REDIRECT_URI=https://httpbin.org/get")
        print("SALESFORCE_ENVIRONMENT=production  # or 'sandbox' for test org")
        return
    
    # Initialize Salesforce auth
    sf_auth = SalesforceAuth()
    
    print("✅ Environment variables loaded")
    print(f"📋 Client ID: {client_id[:10]}...")
    print(f"🔗 Redirect URI: {sf_auth.redirect_uri}")
    print()
    
    # Generate authorization URL with PKCE
    try:
        auth_url, code_verifier = sf_auth.get_authorization_url()
        print("🔐 Generated authorization URL with PKCE")
        print()
        print("📝 Next steps:")
        print("1. Click the link below to authorize the app")
        print("2. Log in to your Salesforce account")
        print("3. Allow access to your org")
        print("4. Copy the authorization code from the redirect URL")
        print("5. Paste it when prompted")
        print()
        
        # Ask user if they want to open the browser
        open_browser = input("🌐 Open authorization URL in browser? (y/n): ").lower().strip()
        if open_browser == 'y':
            webbrowser.open(auth_url)
        
        print(f"\n🔗 Authorization URL:")
        print(auth_url)
        print()
        
        # Get authorization code from user
        auth_code = input("📋 Enter the authorization code: ").strip()
        
        if not auth_code:
            print("❌ No authorization code provided")
            return
        
        # Exchange code for token with PKCE
        print("🔄 Exchanging authorization code for access token...")
        token_data = sf_auth.exchange_code_for_token(auth_code, code_verifier)
        
        # Save credentials
        sf_auth.save_credentials(token_data)
        
        print("✅ OAuth setup completed successfully!")
        print(f"🏢 Instance URL: {token_data['instance_url']}")
        print(f"👤 User ID: {token_data.get('id', 'N/A')}")
        print()
        print("🎉 You can now use the Salesforce API in your bot!")
        
    except Exception as e:
        print(f"❌ Error during OAuth setup: {e}")
        print("\nTroubleshooting tips:")
        print("- Make sure your Client ID and Secret are correct")
        print("- Verify the redirect URI matches your Connected App settings")
        print("- Check that your Connected App has the correct OAuth scopes")

if __name__ == "__main__":
    main() 