# 🚀 Deployment Guide

This guide covers deploying the AI-Powered Slack Salesforce Assistant to production environments.

## 📋 Prerequisites

- GitHub repository with your code
- Railway or Fly.io account
- Slack app configured for production
- Salesforce Connected App configured
- OpenAI API key

## 🚂 Railway Deployment

### 1. Connect Repository

1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will automatically detect Python

### 2. Configure Environment Variables

Add these environment variables in Railway dashboard:

```env
SLACK_BOT_TOKEN=xoxb-your-production-bot-token
SLACK_APP_TOKEN=xapp-your-production-app-token
OPENAI_API_KEY=sk-your-openai-key
SALESFORCE_CLIENT_ID=your-client-id
SALESFORCE_CLIENT_SECRET=your-client-secret
SALESFORCE_REDIRECT_URI=https://your-domain.com/callback
```

### 3. Configure Build Settings

Railway will automatically:
- Install Python dependencies from `requirements.txt`
- Run the app using `python app.py`

### 4. Set Up Custom Domain (Optional)

1. Go to your Railway project settings
2. Add a custom domain
3. Update `SALESFORCE_REDIRECT_URI` to use your domain

## 🪰 Fly.io Deployment

### 1. Install Fly CLI

```bash
# macOS
brew install flyctl

# Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# Linux
curl -L https://fly.io/install.sh | sh
```

### 2. Create Fly App

```bash
fly auth login
fly launch
```

### 3. Configure Environment Variables

```bash
fly secrets set SLACK_BOT_TOKEN=xoxb-your-production-bot-token
fly secrets set SLACK_APP_TOKEN=xapp-your-production-app-token
fly secrets set OPENAI_API_KEY=sk-your-openai-key
fly secrets set SALESFORCE_CLIENT_ID=your-client-id
fly secrets set SALESFORCE_CLIENT_SECRET=your-client-secret
fly secrets set SALESFORCE_REDIRECT_URI=https://your-app.fly.dev/callback
```

### 4. Deploy

```bash
fly deploy
```

## 🔧 Production Configuration

### 1. Update Slack App Settings

1. Go to your Slack app settings
2. Update redirect URLs to use your production domain
3. Add production scopes if needed
4. Update app description and icons

### 2. Update Salesforce Connected App

1. Go to Salesforce Setup → App Manager
2. Edit your Connected App
3. Update callback URL to production domain
4. Add production IP addresses to allowed list

### 3. Database Setup (Future)

For production, consider adding a database:

```bash
# PostgreSQL on Railway
railway add postgresql

# Or use external database
DATABASE_URL=postgresql://user:pass@host:port/db
```

## 🔒 Security Considerations

### 1. Environment Variables

- Never commit `.env` files
- Use platform secrets management
- Rotate tokens regularly
- Use least-privilege access

### 2. API Rate Limits

- Monitor OpenAI API usage
- Implement rate limiting
- Set up billing alerts
- Use appropriate API tiers

### 3. Access Control

- Restrict Slack app to specific channels
- Use Salesforce user profiles
- Implement audit logging
- Monitor usage patterns

## 📊 Monitoring

### 1. Application Logs

```bash
# Railway
railway logs

# Fly.io
fly logs
```

### 2. Health Checks

Add a health check endpoint:

```python
@app.route("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
```

### 3. Metrics

Consider adding:
- Request/response times
- Error rates
- User activity
- API usage

## 🔄 CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy to Railway

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Railway
        uses: railway/deploy@v1
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
```

## 🚨 Troubleshooting

### Common Issues

**App Not Starting:**
- Check environment variables
- Verify Python version
- Check dependency installation

**Slack Integration Failing:**
- Verify bot token permissions
- Check app installation
- Test Socket Mode connection

**Salesforce Errors:**
- Verify OAuth credentials
- Check API permissions
- Test with Salesforce Workbench

### Support

- Check application logs
- Review error messages
- Test in development first
- Contact platform support

---

**Ready for production! 🎉** 