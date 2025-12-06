"""
Command Queue System for Discord -> Free Fire Bot Communication
Uses file-based queue for inter-process communication
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
import tempfile

# Use system temp directory (works on both Windows and Linux)
QUEUE_DIR = Path(tempfile.gettempdir()) / "ff_bot_queue"
COMMANDS_DIR = QUEUE_DIR / "commands"
RESPONSES_DIR = QUEUE_DIR / "responses"

QUEUE_DIR.mkdir(exist_ok=True)
COMMANDS_DIR.mkdir(exist_ok=True)
RESPONSES_DIR.mkdir(exist_ok=True)

class CommandQueue:
    def __init__(self):
        pass
        
    def add_command(self, command_data):
        """Add a command to the file-based queue"""
        command_id = f"{datetime.now().timestamp()}"
        command_data['id'] = command_id
        command_data['timestamp'] = datetime.now().isoformat()
        
        cmd_file = COMMANDS_DIR / f"{command_id}.json"
        with open(cmd_file, 'w') as f:
            json.dump(command_data, f)
        
        return command_id
    
    def get_command(self):
        """Get next command from file-based queue"""
        try:
            files = sorted(COMMANDS_DIR.glob("*.json"))
            if files:
                cmd_file = files[0]
                with open(cmd_file, 'r') as f:
                    command_data = json.load(f)
                cmd_file.unlink()
                return command_data
        except Exception as e:
            print(f"[QUEUE] Error reading command: {e}")
        return None
    
    def add_response(self, command_id, response):
        """Store response for a command in file"""
        if not command_id:
            return
            
        response_data = {
            'response': response,
            'timestamp': datetime.now().isoformat()
        }
        
        resp_file = RESPONSES_DIR / f"{command_id}.json"
        with open(resp_file, 'w') as f:
            json.dump(response_data, f)
    
    def get_response(self, command_id):
        """Get response for a command from file"""
        resp_file = RESPONSES_DIR / f"{command_id}.json"
        if resp_file.exists():
            with open(resp_file, 'r') as f:
                return json.load(f)
        return None
    
    def clear_old_responses(self, max_age_seconds=300):
        """Clear responses older than max_age_seconds"""
        current_time = time.time()
        
        for resp_file in RESPONSES_DIR.glob("*.json"):
            try:
                file_age = current_time - resp_file.stat().st_mtime
                if file_age > max_age_seconds:
                    resp_file.unlink()
            except Exception:
                pass

command_queue = CommandQueue()
