# 🤖 AI-Powered Slack Salesforce Assistant

An intelligent Slack bot that allows enterprise employees to interact with Salesforce using natural language commands. Built with Slack Bolt SDK, OpenAI GPT-4o, and Salesforce REST API.

## ✨ Features

- **Natural Language Processing**: Use plain English to interact with Salesforce
- **Full CRUD Operations**: Create, Read, Update, and Delete Salesforce records
- **Lead Management**: Complete lead lifecycle management
- **Interactive Confirmations**: Simple Execute/Cancel buttons for safe operations
- **Detailed Error Messages**: Comprehensive debugging information
- **Real-time Integration**: Direct Salesforce API integration

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Slack Workspace with admin access
- Salesforce Developer Org
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/aarav-paul/nl_crm_slackbot.git
   cd nl_crm_slackbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your credentials
   ```

4. **Configure Slack App**
   - Create a new Slack app at https://api.slack.com/apps
   - Enable Socket Mode
   - Add bot token scopes: `chat:write`, `commands`
   - Create slash command: `/aiassistant`
   - Install app to workspace

5. **Configure Salesforce**
   - Create Connected App in Salesforce
   - Enable OAuth settings
   - Set redirect URI to `https://example.com`
   - Run OAuth setup: `python setup_oauth.py`

6. **Start the bot**
   ```bash
   python app.py
   ```

## 📋 Environment Variables

Create a `.env` file with the following variables:

```env
# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-key

# Salesforce Configuration
SALESFORCE_CLIENT_ID=your-client-id
SALESFORCE_CLIENT_SECRET=your-client-secret
SALESFORCE_REDIRECT_URI=https://example.com
```

## 🎯 Usage Examples

### Lead Operations

**Create a Lead:**
```
/aiassistant create a new lead for John Doe with email john@example.com and status Open
```

**Update Lead Status:**
```
/aiassistant update John Doe's lead status to Qualified
```

**Delete a Lead:**
```
/aiassistant delete the lead for John Doe
```

### How It Works

1. **Natural Language Input**: User types command in Slack
2. **AI Parsing**: GPT-4o converts to structured JSON
3. **Confirmation**: Bot shows parsed action with Execute/Cancel buttons
4. **Execution**: User confirms and system performs Salesforce operation
5. **Result**: Detailed success/error message with debug information

## 🏗️ Architecture

### Core Components

- **`app.py`**: Main Slack bot application with command handlers
- **`ai_processor.py`**: OpenAI integration for command parsing
- **`salesforce_client.py`**: Salesforce API wrapper with CRUD operations
- **`command_storage.py`**: In-memory storage for command confirmations
- **`salesforce_oauth.py`**: OAuth flow management for Salesforce

### Data Flow

```
Slack Command → AI Parser → Command Storage → Salesforce API → Response
```

## 🔧 Development

### Project Structure

```
nl_crm_slackbot/
├── app.py                 # Main Slack bot
├── ai_processor.py        # OpenAI integration
├── salesforce_client.py   # Salesforce API client
├── command_storage.py     # Command storage
├── salesforce_oauth.py    # OAuth management
├── setup_oauth.py         # OAuth setup script
├── requirements.txt       # Python dependencies
├── env.example           # Environment template
├── README.md             # This file
└── .gitignore           # Git ignore rules
```

### Adding New Features

1. **New Salesforce Objects**: Extend `salesforce_client.py`
2. **New Operations**: Update AI processor prompts
3. **Enhanced UI**: Modify Slack message formatting
4. **Persistence**: Replace in-memory storage with database

## 🛡️ Security

- **OAuth 2.0**: Secure Salesforce authentication
- **Environment Variables**: Sensitive data protection
- **Input Validation**: AI-parsed command validation
- **Error Handling**: Comprehensive error management
- **Audit Trail**: Detailed logging for all operations

## 🚧 Limitations

- **In-Memory Storage**: Commands expire after 5 minutes
- **Lead Objects Only**: Currently supports Lead operations
- **Single User**: No multi-user session management
- **Development Mode**: Uses example.com redirect URI

## 🔮 Roadmap

- [ ] **Multi-Object Support**: Contacts, Accounts, Opportunities
- [ ] **Database Storage**: PostgreSQL for persistent data
- [ ] **Advanced UI**: Rich modals and multi-step workflows
- [ ] **User Management**: Multi-user support with permissions
- [ ] **Analytics**: Usage tracking and reporting
- [ ] **Production Deployment**: Railway/Fly.io deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section below
- Review Salesforce API documentation

## 🔍 Troubleshooting

### Common Issues

**Slack Bot Not Responding:**
- Check bot token and app token
- Verify Socket Mode is enabled
- Check bot is installed to workspace

**Salesforce Authentication Errors:**
- Verify OAuth credentials
- Check redirect URI matches
- Ensure Connected App is properly configured

**AI Parsing Errors:**
- Check OpenAI API key
- Verify API quota and billing
- Review command syntax

**Field Permission Errors:**
- Check Salesforce field-level security
- Verify user profile permissions
- Use supported field names (FirstName, LastName, etc.)

---

**Built with ❤️ for enterprise productivity** 