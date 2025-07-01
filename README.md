# AI-Powered Slack Assistant

A Slack bot that integrates with OpenAI GPT-4o to parse natural language commands into structured JSON for Salesforce operations.

## Current Features

- Responds to basic commands: `hello`, `help`, `ping`
- Responds when mentioned with `@bot_name`
- **NEW**: `/aiassistant` slash command with AI processing
- **NEW**: GPT-4o integration for natural language parsing
- **NEW**: Structured JSON output for Salesforce operations
- Uses Socket Mode for easy development

## Complete Setup Instructions

### 1. Create a Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click "Create New App" → "From scratch"
3. Give your app a name (e.g., "AI Assistant") and select your workspace

### 2. Configure Bot Token Scopes

Go to **"OAuth & Permissions"** and add these scopes:
- `chat:write` - Send messages
- `app_mentions:read` - Read mentions
- `channels:history` - Read channel messages
- `groups:history` - Read private channel messages
- `im:history` - Read direct messages
- `mpim:history` - Read group direct messages
- `commands` - Add slash commands

### 3. Enable Socket Mode

1. Go to **"Socket Mode"** in your app settings
2. Enable Socket Mode
3. Create an app-level token (starts with `xapp-`)

### 4. Create Slash Command

1. Go to **"Slash Commands"** in your app settings
2. Click **"Create New Command"**
3. Fill in the details:
   - **Command**: `/aiassistant`
   - **Request URL**: Leave empty (we're using Socket Mode)
   - **Short Description**: "AI-powered assistant for Salesforce operations"
   - **Usage Hint**: "update John Doe's lead status to Qualified"
4. Click **"Save"**

### 5. Install the App

1. Go to **"OAuth & Permissions"**
2. Click **"Install to Workspace"**
3. Copy the Bot User OAuth Token (starts with `xoxb-`)

### 6. Set Up Environment Variables

1. Copy `env.example` to `.env`
2. Fill in your tokens:
   ```
   SLACK_BOT_TOKEN=xoxb-your-bot-token-here
   SLACK_APP_TOKEN=xapp-your-app-token-here
   OPENAI_API_KEY=sk-your-openai-api-key-here
   ```

### 7. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 8. Run the Bot

```bash
python3 app.py
```

## Testing the AI Assistant

Once running, try these AI commands in Slack:

### Natural Language Commands:
- `/aiassistant update John Doe's lead status to Qualified`
- `/aiassistant create a new contact for Jane Smith with email jane@example.com`
- `/aiassistant find all leads with status Open`
- `/aiassistant delete the account for Acme Corporation`

### What You'll See:

**In Slack:**
- Beautiful formatted response with parsed JSON
- Summary of the action (tool, action, object, filters, fields)
- Confirmation that the command was understood

**In Terminal:**
- Detailed logging of the AI processing
- Raw JSON output from GPT-4o
- Success/error status

## AI Processing Examples

### Input: "Update John Doe's lead status to Qualified"
### Output:
```json
{
  "tool": "salesforce",
  "action": "update",
  "object": "Lead",
  "filters": {"name": "John Doe"},
  "fields": {"status": "Qualified"}
}
```

### Input: "Create a new contact for Jane Smith"
### Output:
```json
{
  "tool": "salesforce",
  "action": "create",
  "object": "Contact",
  "filters": {},
  "fields": {"name": "Jane Smith"}
}
```

## Verification Checklist

- ✅ Slack App created at api.slack.com/apps
- ✅ Socket Mode enabled with app token
- ✅ Slash command `/aiassistant` created
- ✅ All required scopes added
- ✅ App installed to workspace
- ✅ Environment variables set (including OpenAI API key)
- ✅ Bot running with slack_bolt
- ✅ OpenAI SDK installed and working
- ✅ AI processing functional
- ✅ JSON output formatted for Slack

## Next Steps

This foundation is ready for:
- **Salesforce API integration** - Execute the parsed commands
- **Confirmation workflows** - Add approval steps before execution
- **Error handling** - Handle API failures gracefully
- **Database storage** - Log operations and user preferences
- **Advanced parsing** - Support more complex queries and operations 