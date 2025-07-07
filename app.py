import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from ai_processor import AIProcessor
from salesforce_client import SalesforceClient
from command_storage import command_storage
import json

# Load environment variables
load_dotenv()

# Initialize the Slack app and AI processor
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
ai_processor = AIProcessor()

# Initialize Salesforce client
try:
    salesforce_client = SalesforceClient()
    print("✅ Salesforce client initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize Salesforce client: {e}")
    salesforce_client = None

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
• `/aiassistant create a new lead for Jane Smith with email jane@example.com`
• `/aiassistant update John Doe's lead status to Qualified`
• `/aiassistant delete the lead for Mike Johnson`

*How it works:*
1. Type a natural language command
2. AI parses it into structured format
3. Click "Execute" to run in Salesforce
4. Get detailed results and error messages

*Supported Operations:*
• **Create** - Add new leads to Salesforce
• **Update** - Modify existing lead status
• **Delete** - Remove leads from Salesforce

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
    
    # Check if Salesforce is available
    if not salesforce_client:
        say("❌ *Error: Salesforce connection not available*\n\nPlease check your Salesforce credentials and try again.")
        return
    
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
        
        if result['success']:
            # Check if it's a lead operation command
            parsed_command = result['parsed_command']
            if parsed_command.get('object') == 'Lead' and parsed_command.get('action') in ['create', 'update', 'delete']:
                # Store the command for later execution
                command_id = command_storage.store_command(command['user_id'], parsed_command)
                
                # Create confirmation message with buttons
                action = parsed_command.get('action', 'Unknown')
                object_type = parsed_command.get('object', 'Unknown')
                
                if action == 'create':
                    fields = parsed_command.get('fields', {})
                    lead_name = fields.get('Name', 'Unknown')
                    confirmation_text = f"""
🤖 *AI Assistant - Lead Creation Confirmation*

*Command:* {command['text']}

*Parsed Action:*
• **Object:** {object_type}
• **Action:** Create New Lead
• **Lead Name:** {lead_name}

*Fields to Create:*
{chr(10).join([f"• {k}: {v}" for k, v in fields.items()])}

*What will happen:*
1. Create new lead "{lead_name}" in Salesforce
2. Set all specified fields
3. Return the new lead ID

*Debug Info:*
• Command ID: `{command_id}`
• User: <@{command['user_id']}>
• Timestamp: {command.get('response_url', 'N/A')}

Click *Execute* to proceed or *Cancel* to abort.
                    """
                elif action == 'delete':
                    filters = parsed_command.get('filters', {})
                    filters_lower = {k.lower(): v for k, v in filters.items()}
                    lead_name = filters_lower.get('name', 'Unknown')
                    confirmation_text = f"""
🤖 *AI Assistant - Lead Deletion Confirmation*

*Command:* {command['text']}

*Parsed Action:*
• **Object:** {object_type}
• **Action:** Delete Lead
• **Lead Name:** {lead_name}

*What will happen:*
1. Find lead "{lead_name}" in Salesforce
2. Permanently delete the lead
3. Return confirmation

⚠️ *Warning: This action cannot be undone!*

*Debug Info:*
• Command ID: `{command_id}`
• User: <@{command['user_id']}>
• Timestamp: {command.get('response_url', 'N/A')}

Click *Execute* to proceed or *Cancel* to abort.
                    """
                else:  # update action
                    filters = parsed_command.get('filters', {})
                    fields = parsed_command.get('fields', {})
                    filters_lower = {k.lower(): v for k, v in filters.items()}
                    fields_lower = {k.lower(): v for k, v in fields.items()}
                    lead_name = filters_lower.get('name', 'Unknown')
                    new_status = fields_lower.get('status', 'Unknown')
                    confirmation_text = f"""
🤖 *AI Assistant - Lead Update Confirmation*

*Command:* {command['text']}

*Parsed Action:*
• **Object:** {object_type}
• **Action:** Update Status
• **Lead Name:** {lead_name}
• **New Status:** {new_status}

*What will happen:*
1. Find lead "{lead_name}" in Salesforce
2. Update status to "{new_status}"
3. Return detailed results

*Debug Info:*
• Command ID: `{command_id}`
• User: <@{command['user_id']}>
• Timestamp: {command.get('response_url', 'N/A')}

Click *Execute* to proceed or *Cancel* to abort.
                    """
                
                # Create buttons
                blocks = [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": confirmation_text
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Execute",
                                    "emoji": True
                                },
                                "style": "primary",
                                "value": f"execute_{command_id}",
                                "action_id": "execute_command"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Cancel",
                                    "emoji": True
                                },
                                "style": "danger",
                                "value": f"cancel_{command_id}",
                                "action_id": "cancel_command"
                            }
                        ]
                    }
                ]
                
                say(blocks=blocks)
                
            else:
                # For non-lead operations, show parsed result only
                response_message = ai_processor.format_confirmation_message(result)
                say(response_message)
        else:
            # AI parsing failed
            error_message = f"""
❌ *AI Parsing Error*

*Command:* {command['text']}

*Error Details:*
{result['error']}

*Debug Info:*
• User: <@{command['user_id']}>
• Channel: {command['channel_name']}
• Timestamp: {command.get('response_url', 'N/A')}

*Troubleshooting:*
• Check your command syntax
• Make sure you're asking to update a lead status
• Try rephrasing your request
            """
            say(error_message)
        
    else:
        say("🤖 *AI Assistant*\n\nPlease provide a command after `/aiassistant`. For example:\n`/aiassistant update John Doe's lead status to Qualified`")

@app.action("execute_command")
def handle_execute_command(ack, body, say):
    """Handle execute button click"""
    ack()
    
    user_id = body['user']['id']
    command_id = body['actions'][0]['value'].replace('execute_', '')
    
    print(f"🚀 Executing command {command_id} for user {user_id}")
    print(f"[DEBUG] All stored commands for user {user_id}: {list(command_storage.commands.get(user_id, {}).keys())}")
    
    # Get the stored command
    parsed_command = command_storage.get_command(user_id, command_id)
    
    if not parsed_command:
        print(f"[DEBUG] Command not found. Current storage: {command_storage.commands}")
        say(f"❌ *Error: Command not found or expired*\n\nPlease try your command again.\n\n*Debug Info:*\n• User: <@{user_id}>\n• Command ID: `{command_id}`\n• Stored commands: {list(command_storage.commands.get(user_id, {}).keys())}")
        return
    
    # Execute the command
    try:
        result = salesforce_client.execute_lead_operation(parsed_command)
        
        if result['success']:
            # Mark as executed
            command_storage.mark_executed(user_id, command_id)
            
            success_message = f"""
✅ *Lead Operation Successful*

{result['message']}

*Details:*
"""
            
            # Add operation-specific details
            if 'lead_details' in result:
                details = result['lead_details']
                if 'id' in details:
                    success_message += f"• Lead ID: `{details['id']}`\n"
                if 'name' in details:
                    success_message += f"• Lead Name: {details['name']}\n"
                if 'old_status' in details and 'new_status' in details:
                    success_message += f"• Old Status: {details['old_status']}\n"
                    success_message += f"• New Status: {details['new_status']}\n"
                if 'status' in details:
                    success_message += f"• Status: {details['status']}\n"
                if 'fields' in details:
                    success_message += f"• Fields Created: {', '.join(details['fields'].keys())}\n"
            
            success_message += f"""
*Debug Info:*
• Command ID: `{command_id}`
• User: <@{user_id}>
• Execution Time: {body.get('response_url', 'N/A')}
            """
            
            say(success_message)
            
        else:
            error_message = f"""
❌ *Lead Operation Failed*

{result['message']}

*Debug Info:*
• Command ID: `{command_id}`
• User: <@{user_id}>
• Parsed Command: `{json.dumps(parsed_command, indent=2)}`
• Execution Time: {body.get('response_url', 'N/A')}

*Troubleshooting:*
• Check if the lead exists in Salesforce (for update/delete)
• Verify field values are valid
• Check Salesforce connection and permissions
            """
            
            say(error_message)
            
    except Exception as e:
        error_message = f"""
❌ *Unexpected Error*

*Error:* {str(e)}

*Debug Info:*
• Command ID: `{command_id}`
• User: <@{user_id}>
• Parsed Command: `{json.dumps(parsed_command, indent=2)}`
• Execution Time: {body.get('response_url', 'N/A')}

*Troubleshooting:*
• Check Salesforce credentials
• Verify network connection
• Contact administrator
        """
        
        say(error_message)

@app.action("cancel_command")
def handle_cancel_command(ack, body, say):
    """Handle cancel button click"""
    ack()
    
    user_id = body['user']['id']
    command_id = body['actions'][0]['value'].replace('cancel_', '')
    
    print(f"❌ Cancelled command {command_id} for user {user_id}")
    
    # Clean up the stored command
    command_storage.get_command(user_id, command_id)  # This will mark it as accessed
    
    cancel_message = f"""
❌ *Command Cancelled*

The lead update operation has been cancelled.

*Debug Info:*
• Command ID: `{command_id}`
• User: <@{user_id}>
• Cancellation Time: {body.get('response_url', 'N/A')}

You can try the command again anytime.
    """
    
    say(cancel_message)

if __name__ == "__main__":
    # Start the app using Socket Mode
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    print("🤖 Bot is starting...")
    print("🤖 AI Processor initialized...")
    if salesforce_client:
        print("✅ Salesforce client ready")
    else:
        print("❌ Salesforce client not available")
    handler.start() 