
import requests
import hashlib
import time
import uuid
import json

class KeyAuth:
    def __init__(self, app_name, owner_id, app_secret, api_version="1.0"):
        self.app_name = app_name
        self.owner_id = owner_id
        self.app_secret = app_secret
        self.api_version = api_version
        self.session_id = None
        # Use correct API endpoint - 1.2 is the stable version
        self.base_url = "https://keyauth.win/api/1.2/"
        
        print(f"[KeyAuth] Initialized with:")
        print(f"  App Name: {self.app_name}")
        print(f"  Owner ID: {self.owner_id} (length: {len(self.owner_id)})")
        print(f"  API Version: {self.api_version}")
        print(f"  Base URL: {self.base_url}")
        
    def init(self):
        """Initialize KeyAuth session"""
        try:
            # Validate owner ID length
            if len(self.owner_id) != 10:
                return False, f"OwnerID should be 10 characters long (currently {len(self.owner_id)}). Get it from https://keyauth.cc/app/"
            
            # Correct initialization parameters for KeyAuth API 1.2
            # Note: enckey is NOT sent during init - it's used for local encryption only
            init_data = {
                "type": "init",
                "ver": self.api_version,
                "name": self.app_name,
                "ownerid": self.owner_id
            }
            
            print(f"[KeyAuth] Initializing session...")
            print(f"[KeyAuth] Request data: {init_data}")
            
            response = requests.post(self.base_url, data=init_data, timeout=10)
            
            print(f"[KeyAuth] Response status: {response.status_code}")
            
            # Try to parse JSON response
            try:
                data = response.json()
                print(f"[KeyAuth] Response JSON: {data}")
            except ValueError:
                print(f"[KeyAuth] Response text: {response.text}")
                return False, f"Invalid JSON response from KeyAuth API"
            
            if data.get("success"):
                self.session_id = data.get("sessionid")
                print(f"[KeyAuth] ✅ Session initialized successfully!")
                print(f"[KeyAuth] Session ID: {self.session_id}")
                return True, "Session initialized"
            else:
                error_msg = data.get("message", "Failed to initialize session")
                print(f"[KeyAuth] ❌ Init failed: {error_msg}")
                return False, error_msg
                
        except requests.exceptions.RequestException as e:
            print(f"[KeyAuth] ❌ Network error: {str(e)}")
            return False, f"Network error: {str(e)}"
        except Exception as e:
            print(f"[KeyAuth] ❌ Unexpected error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False, f"Initialization error: {str(e)}"
    
    def login(self, username, password, hwid=None):
        """Login with username and password"""
        if not self.session_id:
            init_success, init_msg = self.init()
            if not init_success:
                return False, f"Init failed: {init_msg}"
        
        try:
            if not hwid:
                hwid = str(uuid.uuid4())
            
            login_data = {
                "type": "login",
                "username": username,
                "pass": password,
                "hwid": hwid,
                "sessionid": self.session_id,
                "name": self.app_name,
                "ownerid": self.owner_id
            }
            
            response = requests.post(self.base_url, data=login_data, timeout=10)
            data = response.json()
            
            if data.get("success"):
                info = data.get("info", {})
                subscriptions = info.get("subscriptions", [])
                
                user_info = {
                    "username": info.get("username", username),
                    "subscription": subscriptions[0].get("subscription") if subscriptions else "None",
                    "expiry": subscriptions[0].get("expiry") if subscriptions else "N/A"
                }
                return True, user_info
            else:
                return False, data.get("message", "Login failed - Invalid credentials or account not found")
        except requests.exceptions.RequestException as e:
            return False, f"Network error: {str(e)}"
        except Exception as e:
            return False, f"Login error: {str(e)}"
    
    def register(self, username, password, license_key, hwid=None):
        """Register new user with license key"""
        if not self.session_id:
            init_success, init_msg = self.init()
            if not init_success:
                return False, f"Init failed: {init_msg}"
        
        try:
            if not hwid:
                hwid = str(uuid.uuid4())
            
            register_data = {
                "type": "register",
                "username": username,
                "pass": password,
                "key": license_key,
                "hwid": hwid,
                "sessionid": self.session_id,
                "name": self.app_name,
                "ownerid": self.owner_id
            }
            
            response = requests.post(self.base_url, data=register_data, timeout=10)
            data = response.json()
            
            if data.get("success"):
                return True, "Registration successful! You can now login."
            else:
                return False, data.get("message", "Registration failed - License may be invalid or already used")
        except requests.exceptions.RequestException as e:
            return False, f"Network error: {str(e)}"
        except Exception as e:
            return False, f"Registration error: {str(e)}"
    
    def license(self, license_key, hwid=None):
        """Validate license key"""
        if not self.session_id:
            init_success, init_msg = self.init()
            if not init_success:
                return False, f"Init failed: {init_msg}"
        
        try:
            if not hwid:
                hwid = str(uuid.uuid4())
            
            license_data = {
                "type": "license",
                "key": license_key,
                "hwid": hwid,
                "sessionid": self.session_id,
                "name": self.app_name,
                "ownerid": self.owner_id
            }
            
            response = requests.post(self.base_url, data=license_data, timeout=10)
            data = response.json()
            
            if data.get("success"):
                info = data.get("info", {})
                subscriptions = info.get("subscriptions", [])
                
                user_info = {
                    "username": info.get("username", "LicenseUser"),
                    "subscription": subscriptions[0].get("subscription") if subscriptions else "None",
                    "expiry": subscriptions[0].get("expiry") if subscriptions else "N/A"
                }
                return True, user_info
            else:
                return False, data.get("message", "License validation failed - Key may be invalid or expired")
        except requests.exceptions.RequestException as e:
            return False, f"Network error: {str(e)}"
        except Exception as e:
            return False, f"License error: {str(e)}"
