import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from ai_processor import AIProcessor

# Load environment variables
load_dotenv()

# Initialize the Slack app and AI processor
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
ai_processor = AIProcessor()

@app.message("hello")
def handle_hello_message(message, say):
    """Respond to 'hello' messages"""
    say(f"Hello <@{message['user']}>! 👋")

@app.message("help")
def handle_help_message(message, say):
    """Respond to 'help' messages"""
    help_text = """
🤖 *AI Assistant Bot Help*

Available commands:
• `hello` - Get a friendly greeting
• `help` - Show this help message
• `ping` - Test if the bot is responsive
• `/aiassistant` - Use the AI assistant (slash command)

*AI Commands Examples:*
• `/aiassistant update John Doe's lead status to Qualified`
• `/aiassistant create a new contact for Jane Smith`
• `/aiassistant find all leads with status Open`

More features coming soon!
    """
    say(help_text)

@app.message("ping")
def handle_ping_message(message, say):
    """Respond to 'ping' messages"""
    say("pong! 🏓")

@app.event("app_mention")
def handle_app_mention(event, say):
    """Respond when the bot is mentioned"""
    say(f"Hi <@{event['user']}>! You mentioned me. I'm your AI assistant. Type 'help' to see what I can do!")

@app.command("/aiassistant")
def handle_ai_assistant_command(ack, command, say):
    """Handle /aiassistant slash command with AI processing"""
    # Acknowledge the command request
    ack()
    
    # Print the input to console for debugging
    print(f"🔍 Slash Command Input:")
    print(f"   User: {command['user_name']} ({command['user_id']})")
    print(f"   Channel: {command['channel_name']} ({command['channel_id']})")
    print(f"   Text: '{command['text']}'")
    print(f"   Command: {command['command']}")
    print(f"   Response URL: {command.get('response_url', 'N/A')}")
    print("-" * 50)
    
    # Process the command with AI
    if command['text'].strip():
        print(f"🤖 Processing with AI: '{command['text']}'")
        
        # Parse the command using AI
        result = ai_processor.parse_command(command['text'])
        
        # Print the AI result to console
        print(f"🤖 AI Result:")
        print(f"   Success: {result['success']}")
        if result['success']:
            print(f"   Parsed Command: {result['parsed_command']}")
        else:
            print(f"   Error: {result['error']}")
        print("-" * 50)
        
        # Format and send the response
        response_message = ai_processor.format_confirmation_message(result)
        say(response_message)
        
    else:
        say("🤖 *AI Assistant*\n\nPlease provide a command after `/aiassistant`. For example:\n`/aiassistant update John Doe's lead status to Qualified`")

if __name__ == "__main__":
    # Start the app using Socket Mode
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    print("🤖 Bot is starting...")
    print("🤖 AI Processor initialized...")
    handler.start() 