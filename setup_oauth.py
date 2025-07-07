#!/usr/bin/env python3
"""
Simple Salesforce OAuth Setup Script with PKCE
"""

import os
import webbrowser
from dotenv import load_dotenv
from salesforce_oauth import SalesforceOAuth

def main():
    load_dotenv()
    
    print("🚀 Salesforce OAuth Setup (PKCE)")
    print("=" * 50)
    
    # Check environment variables
    client_id = os.environ.get("SALESFORCE_CLIENT_ID")
    client_secret = os.environ.get("SALESFORCE_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("❌ Missing Salesforce credentials in .env file")
        print("\nPlease add these to your .env file:")
        print("SALESFORCE_CLIENT_ID=your_consumer_key_here")
        print("SALESFORCE_CLIENT_SECRET=your_consumer_secret_here")
        print("SALESFORCE_REDIRECT_URI=https://example.com")
        print("SALESFORCE_ENVIRONMENT=production")
        return
    
    # Initialize OAuth
    oauth = SalesforceOAuth()
    
    print("✅ Environment variables loaded")
    print(f"📋 Client ID: {client_id[:10]}...")
    print(f"🔗 Redirect URI: {oauth.redirect_uri}")
    print()
    
    try:
        # Generate authorization URL with PKCE
        auth_url, code_verifier = oauth.get_authorization_url()
        print("🔐 Generated authorization URL with PKCE")
        print()
        print("📝 Next steps:")
        print("1. Click the link below to authorize the app")
        print("2. Log in to your Salesforce account")
        print("3. Allow access to your org")
        print("4. Copy the authorization code from the redirect URL")
        print("5. Paste it when prompted")
        print()
        
        # Ask to open browser
        open_browser = input("🌐 Open authorization URL in browser? (y/n): ").lower().strip()
        if open_browser == 'y':
            webbrowser.open(auth_url)
        
        print(f"\n🔗 Authorization URL:")
        print(auth_url)
        print()
        
        # Get authorization code
        auth_code = input("📋 Enter the authorization code: ").strip()
        
        if not auth_code:
            print("❌ No authorization code provided")
            return
        
        # Exchange code for token with PKCE
        print("🔄 Exchanging authorization code for access token...")
        token_data = oauth.exchange_code_for_token(auth_code, code_verifier)
        
        # Save credentials
        oauth.save_credentials(token_data)
        
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