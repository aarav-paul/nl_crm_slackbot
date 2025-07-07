from typing import Dict, Optional
import time

class CommandStorage:
    def __init__(self):
        # In-memory storage: {user_id: {command_id: command_data}}
        self.commands = {}
        # Command expiration (5 minutes)
        self.expiration_time = 300  # seconds
    
    def store_command(self, user_id: str, parsed_command: Dict) -> str:
        """
        Store a parsed command for a user
        Returns a unique command ID
        """
        import uuid
        
        command_id = str(uuid.uuid4())
        
        if user_id not in self.commands:
            self.commands[user_id] = {}
        
        # Store command with timestamp
        self.commands[user_id][command_id] = {
            "command": parsed_command,
            "timestamp": time.time(),
            "executed": False
        }
        
        print(f"💾 Stored command for user {user_id}: {command_id}")
        print(f"📝 Command data: {parsed_command}")
        
        return command_id
    
    def get_command(self, user_id: str, command_id: str) -> Optional[Dict]:
        """
        Retrieve a stored command
        Returns None if not found or expired
        """
        if user_id not in self.commands:
            return None
        
        if command_id not in self.commands[user_id]:
            return None
        
        command_data = self.commands[user_id][command_id]
        
        # Check if expired
        if time.time() - command_data["timestamp"] > self.expiration_time:
            print(f"⏰ Command {command_id} expired for user {user_id}")
            del self.commands[user_id][command_id]
            return None
        
        print(f"📖 Retrieved command {command_id} for user {user_id}")
        return command_data["command"]
    
    def mark_executed(self, user_id: str, command_id: str):
        """
        Mark a command as executed
        """
        if user_id in self.commands and command_id in self.commands[user_id]:
            self.commands[user_id][command_id]["executed"] = True
            print(f"✅ Marked command {command_id} as executed for user {user_id}")
    
    def cleanup_expired(self):
        """
        Clean up expired commands
        """
        current_time = time.time()
        expired_count = 0
        
        for user_id in list(self.commands.keys()):
            for command_id in list(self.commands[user_id].keys()):
                command_data = self.commands[user_id][command_id]
                if current_time - command_data["timestamp"] > self.expiration_time:
                    del self.commands[user_id][command_id]
                    expired_count += 1
            
            # Remove empty user entries
            if not self.commands[user_id]:
                del self.commands[user_id]
        
        if expired_count > 0:
            print(f"🧹 Cleaned up {expired_count} expired commands")

# Global instance
command_storage = CommandStorage() 