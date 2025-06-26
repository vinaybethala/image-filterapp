# 🔐 Google OAuth Setup Guide

## Prerequisites
1. A Google account
2. Access to Google Cloud Console

## Step-by-Step Setup

### 1. Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API

### 2. Configure OAuth Consent Screen
1. Go to "APIs & Services" > "OAuth consent screen"
2. Choose "External" user type
3. Fill in the required information:
   - App name: "Image Filter App"
   - User support email: Your email
   - Developer contact information: Your email
4. Add scopes: `openid`, `email`, `profile`
5. Add test users (your email)

### 3. Create OAuth 2.0 Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Choose "Web application"
4. Set authorized redirect URIs:
   - `http://localhost:8501`
   - `http://localhost:8501/`
5. Copy the Client ID and Client Secret

### 4. Update the App Configuration
1. Open `app.py`
2. Replace the placeholder values:
   ```python
   GOOGLE_CLIENT_ID = "your-actual-client-id.apps.googleusercontent.com"
   GOOGLE_CLIENT_SECRET = "your-actual-client-secret"
   ```

### 5. Test the Integration
1. Run your app: `streamlit run app.py`
2. Click "Continue with Google" on the login/signup page
3. Complete the OAuth flow

## Security Notes
- Never commit your client secret to version control
- Use environment variables for production
- Regularly rotate your OAuth credentials

## Troubleshooting
- If you get "redirect_uri_mismatch", check your redirect URIs in Google Console
- If you get "invalid_client", verify your client ID and secret
- Make sure you've added your email as a test user in the OAuth consent screen 