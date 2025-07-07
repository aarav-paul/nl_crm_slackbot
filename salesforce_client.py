import requests
import json
from typing import Dict, Optional, List
from salesforce_oauth import SalesforceOAuth

class SalesforceClient:
    def __init__(self):
        self.oauth = SalesforceOAuth()
        self.credentials = self.oauth.get_valid_credentials()
        
        if not self.credentials:
            raise Exception("No valid Salesforce credentials found. Please run OAuth setup first.")
        
        self.access_token = self.credentials['access_token']
        self.instance_url = self.credentials['instance_url']
        
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def find_lead_by_name(self, name: str) -> Optional[Dict]:
        """
        Find a lead by name using SOQL query
        Returns the lead record if found, None otherwise
        """
        try:
            # Sanitize the name to prevent SOQL injection
            sanitized_name = name.replace("'", "\\'")
            
            query = f"SELECT Id, Name, Status, Email FROM Lead WHERE Name = '{sanitized_name}' LIMIT 1"
            url = f"{self.instance_url}/services/data/v59.0/query/?q={query}"
            
            print(f"🔍 Querying Salesforce: {query}")
            
            response = requests.get(url, headers=self.headers)
            
            if response.status_code != 200:
                print(f"❌ Salesforce query failed: {response.status_code}")
                print(f"❌ Response: {response.text}")
                return None
            
            data = response.json()
            print(f"📊 Query result: {json.dumps(data, indent=2)}")
            
            if data.get("records") and len(data["records"]) > 0:
                lead = data["records"][0]
                print(f"✅ Found lead: {lead['Name']} (ID: {lead['Id']})")
                return lead
            else:
                print(f"❌ No lead found with name: {name}")
                return None
                
        except Exception as e:
            print(f"❌ Error querying lead: {str(e)}")
            return None
    
    def update_lead_status(self, lead_id: str, new_status: str) -> Dict:
        """
        Update a lead's status
        Returns success status and message
        """
        try:
            url = f"{self.instance_url}/services/data/v59.0/sobjects/Lead/{lead_id}"
            payload = {"Status": new_status}
            
            print(f"🔄 Updating lead {lead_id} to status: {new_status}")
            print(f"📤 Payload: {json.dumps(payload, indent=2)}")
            
            response = requests.patch(url, headers=self.headers, json=payload)
            
            print(f"📥 Response status: {response.status_code}")
            if response.text:
                print(f"📥 Response body: {response.text}")
            
            if response.status_code == 204:
                print("✅ Lead status updated successfully")
                return {
                    "success": True,
                    "message": f"Successfully updated lead status to '{new_status}'"
                }
            else:
                print(f"❌ Lead update failed: {response.status_code}")
                error_message = f"Salesforce API error: {response.status_code}"
                if response.text:
                    try:
                        error_data = response.json()
                        if "message" in error_data:
                            error_message = f"Salesforce error: {error_data['message']}"
                    except:
                        error_message = f"Salesforce API error: {response.text}"
                
                return {
                    "success": False,
                    "message": error_message
                }
                
        except Exception as e:
            print(f"❌ Error updating lead: {str(e)}")
            return {
                "success": False,
                "message": f"Network error: {str(e)}"
            }
    
    def create_lead(self, fields: Dict) -> Dict:
        """
        Create a new lead in Salesforce
        Returns success status and message
        """
        try:
            # Map fields to Salesforce Lead object structure
            salesforce_fields = {}
            
            # Handle Name field - split into FirstName and LastName
            if 'Name' in fields:
                name_parts = fields['Name'].split(' ', 1)
                if len(name_parts) > 1:
                    salesforce_fields['FirstName'] = name_parts[0]
                    salesforce_fields['LastName'] = name_parts[1]
                else:
                    salesforce_fields['LastName'] = fields['Name']
            
            # Map other common fields
            field_mapping = {
                'Email': 'Email',
                'Status': 'Status',
                'Company': 'Company',
                'Phone': 'Phone',
                'Title': 'Title',
                'Description': 'Description'
            }
            
            for field, value in fields.items():
                if field in field_mapping:
                    salesforce_fields[field_mapping[field]] = value
                elif field not in ['Name']:  # Skip Name as we handled it above
                    salesforce_fields[field] = value
            
            # Ensure LastName is present (required field)
            if 'LastName' not in salesforce_fields:
                return {
                    "success": False,
                    "message": "❌ Error: Last Name is required for lead creation"
                }
            
            # Ensure Company is present (Salesforce requirement)
            if 'Company' not in salesforce_fields:
                # Use LastName as default company if no company specified
                salesforce_fields['Company'] = salesforce_fields.get('LastName', 'Unknown Company')
                print(f"📝 Using default company: {salesforce_fields['Company']}")
            
            url = f"{self.instance_url}/services/data/v59.0/sobjects/Lead"
            
            print(f"🆕 Creating new lead with fields: {json.dumps(salesforce_fields, indent=2)}")
            
            response = requests.post(url, headers=self.headers, json=salesforce_fields)
            
            print(f"📥 Response status: {response.status_code}")
            if response.text:
                print(f"📥 Response body: {response.text}")
            
            if response.status_code == 201:
                data = response.json()
                lead_id = data.get('id')
                print(f"✅ Lead created successfully with ID: {lead_id}")
                return {
                    "success": True,
                    "message": f"Successfully created new lead with ID: {lead_id}",
                    "lead_id": lead_id
                }
            else:
                print(f"❌ Lead creation failed: {response.status_code}")
                error_message = f"Salesforce API error: {response.status_code}"
                if response.text:
                    try:
                        error_data = response.json()
                        if isinstance(error_data, list) and len(error_data) > 0:
                            error_info = error_data[0]
                            if "message" in error_info:
                                error_message = f"Salesforce error: {error_info['message']}"
                                if "fields" in error_info:
                                    error_message += f" (Fields: {', '.join(error_info['fields'])})"
                        elif isinstance(error_data, dict) and "message" in error_data:
                            error_message = f"Salesforce error: {error_data['message']}"
                    except:
                        error_message = f"Salesforce API error: {response.text}"
                
                return {
                    "success": False,
                    "message": error_message
                }
                
        except Exception as e:
            print(f"❌ Error creating lead: {str(e)}")
            return {
                "success": False,
                "message": f"Network error: {str(e)}"
            }
    
    def delete_lead(self, lead_id: str) -> Dict:
        """
        Delete a lead from Salesforce
        Returns success status and message
        """
        try:
            url = f"{self.instance_url}/services/data/v59.0/sobjects/Lead/{lead_id}"
            
            print(f"🗑️ Deleting lead with ID: {lead_id}")
            
            response = requests.delete(url, headers=self.headers)
            
            print(f"📥 Response status: {response.status_code}")
            if response.text:
                print(f"📥 Response body: {response.text}")
            
            if response.status_code == 204:
                print("✅ Lead deleted successfully")
                return {
                    "success": True,
                    "message": f"Successfully deleted lead with ID: {lead_id}"
                }
            else:
                print(f"❌ Lead deletion failed: {response.status_code}")
                error_message = f"Salesforce API error: {response.status_code}"
                if response.text:
                    try:
                        error_data = response.json()
                        if "message" in error_data:
                            error_message = f"Salesforce error: {error_data['message']}"
                    except:
                        error_message = f"Salesforce API error: {response.text}"
                
                return {
                    "success": False,
                    "message": error_message
                }
                
        except Exception as e:
            print(f"❌ Error deleting lead: {str(e)}")
            return {
                "success": False,
                "message": f"Network error: {str(e)}"
            }
    
    def execute_lead_operation(self, parsed_command: Dict) -> Dict:
        """
        Execute any lead operation (create, update, delete) from parsed AI output
        Returns detailed result for Slack response
        """
        try:
            action = parsed_command.get('action', '').lower()
            
            if action == 'create':
                return self.execute_lead_create(parsed_command)
            elif action == 'update':
                return self.execute_lead_update(parsed_command)
            elif action == 'delete':
                return self.execute_lead_delete(parsed_command)
            else:
                return {
                    "success": False,
                    "message": f"❌ Unsupported action: {action}. Supported actions: create, update, delete"
                }
                
        except Exception as e:
            print(f"❌ Error executing lead operation: {str(e)}")
            return {
                "success": False,
                "message": f"❌ Unexpected error: {str(e)}"
            }
    
    def execute_lead_create(self, parsed_command: Dict) -> Dict:
        """
        Execute a lead create command from parsed AI output
        Returns detailed result for Slack response
        """
        try:
            fields = parsed_command.get("fields", {})
            
            if not fields:
                return {
                    "success": False,
                    "message": "❌ Error: No fields specified for lead creation"
                }
            
            # Check for required fields
            if not fields.get('Name'):
                return {
                    "success": False,
                    "message": "❌ Error: Lead Name is required for creation"
                }
            
            print(f"🎯 Executing lead creation: {fields.get('Name')}")
            
            # Create the lead
            create_result = self.create_lead(fields)
            
            if create_result["success"]:
                return {
                    "success": True,
                    "message": f"✅ Successfully created new lead *{fields.get('Name')}* in Salesforce",
                    "lead_details": {
                        "id": create_result["lead_id"],
                        "name": fields.get('Name'),
                        "fields": fields
                    }
                }
            else:
                return {
                    "success": False,
                    "message": f"❌ Failed to create lead '{fields.get('Name')}': {create_result['message']}"
                }
                
        except Exception as e:
            print(f"❌ Error executing lead creation: {str(e)}")
            return {
                "success": False,
                "message": f"❌ Unexpected error: {str(e)}"
            }
    
    def execute_lead_delete(self, parsed_command: Dict) -> Dict:
        """
        Execute a lead delete command from parsed AI output
        Returns detailed result for Slack response
        """
        try:
            filters = parsed_command.get("filters", {})
            
            # Normalize keys to lowercase for robust access
            filters_lower = {k.lower(): v for k, v in filters.items()}
            
            lead_name = filters_lower.get("name")
            
            if not lead_name:
                return {
                    "success": False,
                    "message": f"❌ Error: No lead name specified in the command (parsed filters: {filters})"
                }
            
            print(f"🎯 Executing lead deletion: {lead_name}")
            
            # Step 1: Find the lead
            lead = self.find_lead_by_name(lead_name)
            
            if not lead:
                return {
                    "success": False,
                    "message": f"❌ Lead not found: No lead with name '{lead_name}' exists in Salesforce"
                }
            
            # Step 2: Delete the lead
            delete_result = self.delete_lead(lead["Id"])
            
            if delete_result["success"]:
                return {
                    "success": True,
                    "message": f"✅ Successfully deleted lead *{lead_name}* from Salesforce",
                    "lead_details": {
                        "id": lead["Id"],
                        "name": lead["Name"],
                        "status": lead.get("Status", "Unknown")
                    }
                }
            else:
                return {
                    "success": False,
                    "message": f"❌ Failed to delete lead '{lead_name}': {delete_result['message']}"
                }
                
        except Exception as e:
            print(f"❌ Error executing lead deletion: {str(e)}")
            return {
                "success": False,
                "message": f"❌ Unexpected error: {str(e)}"
            }

    def execute_lead_update(self, parsed_command: Dict) -> Dict:
        """
        Execute a lead update command from parsed AI output
        Returns detailed result for Slack response
        """
        try:
            # Extract data from parsed command
            filters = parsed_command.get("filters", {})
            fields = parsed_command.get("fields", {})

            # Normalize keys to lowercase for robust access
            filters_lower = {k.lower(): v for k, v in filters.items()}
            fields_lower = {k.lower(): v for k, v in fields.items()}

            lead_name = filters_lower.get("name")
            new_status = fields_lower.get("status")

            if not lead_name:
                return {
                    "success": False,
                    "message": "❌ Error: No lead name specified in the command (parsed filters: %s)" % filters
                }

            if not new_status:
                return {
                    "success": False,
                    "message": "❌ Error: No status specified in the command (parsed fields: %s)" % fields
                }

            print(f"🎯 Executing lead update: {lead_name} → {new_status}")

            # Step 1: Find the lead
            lead = self.find_lead_by_name(lead_name)

            if not lead:
                return {
                    "success": False,
                    "message": f"❌ Lead not found: No lead with name '{lead_name}' exists in Salesforce"
                }

            # Step 2: Update the lead
            update_result = self.update_lead_status(lead["Id"], new_status)

            if update_result["success"]:
                return {
                    "success": True,
                    "message": f"✅ Successfully updated *{lead_name}* to status *{new_status}* in Salesforce",
                    "lead_details": {
                        "id": lead["Id"],
                        "name": lead["Name"],
                        "old_status": lead.get("Status", "Unknown"),
                        "new_status": new_status
                    }
                }
            else:
                return {
                    "success": False,
                    "message": f"❌ Failed to update lead '{lead_name}': {update_result['message']}"
                }

        except Exception as e:
            print(f"❌ Error executing lead update: {str(e)}")
            return {
                "success": False,
                "message": f"❌ Unexpected error: {str(e)}"
            } 