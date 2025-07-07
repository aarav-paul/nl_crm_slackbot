import json
import os
from openai import OpenAI
from typing import Dict, Any, Optional

class AIProcessor:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
    def parse_command(self, user_input: str) -> Dict[str, Any]:
        """
        Parse natural language command into structured JSON using GPT-4o
        """
        prompt = f"""
You are an AI assistant that converts natural language commands into structured JSON for Salesforce operations.

Parse the following user command and return ONLY a valid JSON object with this structure:

For UPDATE operations:
{{
  "tool": "salesforce",
  "action": "update",
  "object": "Lead|Contact|Account|Opportunity",
  "filters": {{"Name": "value"}},
  "fields": {{"Status": "value", "Email": "value"}}
}}

For CREATE operations:
{{
  "tool": "salesforce",
  "action": "create",
  "object": "Lead|Contact|Account|Opportunity",
  "fields": {{"Name": "value", "Email": "value", "Status": "value"}}
}}

For DELETE operations:
{{
  "tool": "salesforce",
  "action": "delete",
  "object": "Lead|Contact|Account|Opportunity",
  "filters": {{"Name": "value"}}
}}

Examples:
- "update John Doe's lead status to Qualified" → {{"tool": "salesforce", "action": "update", "object": "Lead", "filters": {{"Name": "John Doe"}}, "fields": {{"Status": "Qualified"}}}}
- "create a new lead for Jane Smith with email jane@example.com" → {{"tool": "salesforce", "action": "create", "object": "Lead", "fields": {{"LastName": "Smith", "FirstName": "Jane", "Email": "jane@example.com", "Company": "Smith Corp"}}}}
- "delete the lead for Mike Johnson" → {{"tool": "salesforce", "action": "delete", "object": "Lead", "filters": {{"Name": "Mike Johnson"}}}}

User command: "{user_input}"

Return ONLY the JSON object, no additional text or explanation.
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",  # or "gpt-4o-mini" if you prefer
                messages=[
                    {"role": "system", "content": "You are a command parser that returns only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # Low temperature for consistent parsing
                max_tokens=200
            )
            
            # Extract the JSON from the response
            json_str = response.choices[0].message.content.strip()
            
            # Clean up the response (remove markdown code blocks if present)
            if json_str.startswith("```json"):
                json_str = json_str[7:]
            if json_str.endswith("```"):
                json_str = json_str[:-3]
            
            json_str = json_str.strip()
            
            # Parse the JSON
            parsed_command = json.loads(json_str)
            
            return {
                "success": True,
                "parsed_command": parsed_command,
                "original_input": user_input
            }
            
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Failed to parse JSON: {str(e)}",
                "original_input": user_input,
                "raw_response": response.choices[0].message.content if 'response' in locals() else None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"OpenAI API error: {str(e)}",
                "original_input": user_input
            }
    
    def format_confirmation_message(self, result: Dict[str, Any]) -> str:
        """
        Format the parsed command into a nice Slack message for confirmation
        """
        if not result["success"]:
            return f"❌ *Error parsing command:*\n{result['error']}\n\nPlease try rephrasing your request."
        
        parsed = result["parsed_command"]
        action = parsed.get('action', 'Unknown')
        object_type = parsed.get('object', 'Unknown')
        
        # Create action-specific summaries
        if action == "create":
            fields = parsed.get('fields', {})
            summary = f"Create new {object_type} with {len(fields)} field(s)"
            details = "\n".join([f"• {k}: {v}" for k, v in fields.items()])
        elif action == "delete":
            filters = parsed.get('filters', {})
            summary = f"Delete {object_type} matching {len(filters)} filter(s)"
            details = "\n".join([f"• {k}: {v}" for k, v in filters.items()])
        elif action == "update":
            filters = parsed.get('filters', {})
            fields = parsed.get('fields', {})
            summary = f"Update {object_type} with {len(fields)} field(s)"
            details = f"Filters: {', '.join([f'{k}={v}' for k, v in filters.items()])}\nFields: {', '.join([f'{k}={v}' for k, v in fields.items()])}"
        else:
            summary = f"Unknown action: {action}"
            details = "No details available"
        
        message = f"""
🤖 *AI Command Parsed Successfully!*

*Original Command:*
`{result['original_input']}`

*Parsed Action:*
• **Tool:** {parsed.get('tool', 'Unknown')}
• **Action:** {action}
• **Object:** {object_type}
• **Summary:** {summary}

*Details:*
{details}

*Next Steps:*
This command will be processed by the Salesforce integration.
        """
        
        return message.strip() 