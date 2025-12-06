
import asyncio
import os
import ssl
import aiohttp
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Pb2 import MajoRLoGinrEq_pb2, MajoRLoGinrEs_pb2, PorTs_pb2
from xHeaders import *


async def encrypted_proto_pool(encoded_hex):
    """Encrypt packet using AES CBC"""
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload


async def GeNeRaTeAccEss_pool(uid, password):
    """Generate access token for login"""
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            if response.status != 200:
                return "Failed to get access token"
            data = await response.json()
            open_id = data.get("open_id")
            access_token = data.get("access_token")
            return (open_id, access_token) if open_id and access_token else (None, None)


async def EncRypTMajoRLoGin_pool(open_id, access_token):
    """Encrypt major login packet"""
    from datetime import datetime
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = "1.118.1"
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return await encrypted_proto_pool(string)


async def MajorLogin_pool(payload):
    """Send major login request"""
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/x-www-form-urlencoded",
        'Expect': "100-continue",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB51"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200:
                return await response.read()
            return None


async def DecRypTMajoRLoGin_pool(MajoRLoGinResPonsE):
    """Decrypt major login response"""
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto


async def GetLoginData_pool(base_url, payload, token):
    """Get login data"""
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/x-www-form-urlencoded",
        'Expect': "100-continue",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB51",
        'Authorization': f"Bearer {token}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200:
                return await response.read()
            return None


async def DecRypTLoGinDaTa_pool(LoGinDaTa):
    """Decrypt login data"""
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto


async def xAuThSTarTuP_pool(TarGeT, token, timestamp, key, iv):
    """Generate auth startup packet"""
    from xC4 import DecodE_HeX, EnC_PacKeT
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9:
        headers = '0000000'
    elif uid_length == 8:
        headers = '00000000'
    elif uid_length == 10:
        headers = '000000'
    elif uid_length == 7:
        headers = '000000000'
    else:
        headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"


class BotConnection:
    def __init__(self, uid, password, account_type):
        self.uid = uid
        self.password = password
        self.account_type = account_type
        self.online_writer = None
        self.whisper_writer = None
        self.key = None
        self.iv = None
        self.region = None
        self.connected = False
        self.lock = asyncio.Lock()
        self.last_error = None
    
    async def connect(self):
        """Connect to Free Fire servers"""
        try:
            print(f"[POOL] Connecting {self.account_type} account: {self.uid}")
            
            # Login
            login_result = await GeNeRaTeAccEss_pool(self.uid, self.password)
            if not login_result or login_result == "Failed to get access token":
                self.last_error = "Failed to get access token - Invalid credentials or banned"
                print(f"[POOL] Failed to login {self.account_type}: {self.last_error}")
                return False
            
            open_id, access_token = login_result
            if not open_id or not access_token:
                self.last_error = "No open_id/access_token received"
                print(f"[POOL] Failed to login {self.account_type}: {self.last_error}")
                return False
            
            # Major Login
            PyL = await EncRypTMajoRLoGin_pool(open_id, access_token)
            MajoRLoGinResPonsE = await MajorLogin_pool(PyL)
            if not MajoRLoGinResPonsE:
                self.last_error = "Major Login failed - Account banned or region blocked"
                print(f"[POOL] Failed Major Login for {self.account_type}: {self.last_error}")
                return False
            
            MajoRLoGinauTh = await DecRypTMajoRLoGin_pool(MajoRLoGinResPonsE)
            UrL = MajoRLoGinauTh.url
            self.region = MajoRLoGinauTh.region
            ToKen = MajoRLoGinauTh.token
            TarGeT = MajoRLoGinauTh.account_uid
            self.key = MajoRLoGinauTh.key
            self.iv = MajoRLoGinauTh.iv
            timestamp = MajoRLoGinauTh.timestamp
            
            # Get Login Data
            LoGinDaTa = await GetLoginData_pool(UrL, PyL, ToKen)
            if not LoGinDaTa:
                self.last_error = "Failed to get server ports"
                print(f"[POOL] Failed to get ports for {self.account_type}: {self.last_error}")
                return False
            
            LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa_pool(LoGinDaTa)
            OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
            OnLineiP, OnLineporT = OnLinePorTs.split(":")
            
            # Connect to Online server
            AutHToKen = await xAuThSTarTuP_pool(int(TarGeT), ToKen, int(timestamp), self.key, self.iv)
            reader, writer = await asyncio.open_connection(OnLineiP, int(OnLineporT))
            self.online_writer = writer
            
            bytes_payload = bytes.fromhex(AutHToKen)
            self.online_writer.write(bytes_payload)
            await self.online_writer.drain()
            
            self.connected = True
            print(f"[POOL] ✅ Connected {self.account_type} account: {self.uid}")
            
            # Keep connection alive
            asyncio.create_task(self._keep_alive(reader))
            
            return True
            
        except Exception as e:
            self.last_error = str(e)
            print(f"[POOL] Error connecting {self.account_type}: {e}")
            return False
    
    async def _keep_alive(self, reader):
        """Keep connection alive by reading packets"""
        try:
            while self.connected:
                data = await reader.read(9999)
                if not data:
                    break
                # Don't sleep too long to keep connection active
                await asyncio.sleep(0.05)
        except Exception as e:
            print(f"[POOL] Connection lost for {self.account_type}: {e}")
            self.connected = False
    
    async def send_packet(self, packet):
        """Send packet using this connection - OPTIMIZED FOR SPEED"""
        async with self.lock:
            # Check if we need to reconnect
            if not self.connected or not self.online_writer:
                success = await self.connect()
                if not success:
                    return False
            
            try:
                self.online_writer.write(packet)
                await self.online_writer.drain()
                return True
            except Exception as e:
                # Silent reconnect on error - don't print to avoid spam
                self.connected = False
                # Try one more time
                success = await self.connect()
                if success:
                    try:
                        self.online_writer.write(packet)
                        await self.online_writer.drain()
                        return True
                    except:
                        return False
                return False
    
    async def disconnect(self):
        """Disconnect from server"""
        self.connected = False
        if self.online_writer:
            self.online_writer.close()
            await self.online_writer.wait_closed()


class ConnectionPool:
    def __init__(self):
        self.lag_accounts = []
        self.spm_accounts = []
        self.initialized = False
    
    async def initialize(self):
        """Initialize connection pool with multiple accounts"""
        if self.initialized:
            return
        
        print("[POOL] Initializing connection pool...")
        
        # Get account credentials from environment
        lag_accounts_str = os.environ.get('LAG_ACCOUNTS', '')
        spm_accounts_str = os.environ.get('SPM_ACCOUNTS', '')
        
        # Parse LAG accounts
        if lag_accounts_str:
            for account in lag_accounts_str.split(','):
                if ':' in account:
                    uid, password = account.strip().split(':')
                    bot = BotConnection(uid, password, 'LAG')
                    self.lag_accounts.append(bot)
        
        # Fallback to single LAG account
        if not self.lag_accounts:
            lag_uid = os.environ.get('LAG_UID', '')
            lag_pw = os.environ.get('LAG_PASSWORD', '')
            if lag_uid and lag_pw:
                bot = BotConnection(lag_uid, lag_pw, 'LAG')
                self.lag_accounts.append(bot)
        
        # Parse SPM accounts
        if spm_accounts_str:
            for account in spm_accounts_str.split(','):
                if ':' in account:
                    uid, password = account.strip().split(':')
                    bot = BotConnection(uid, password, 'SPM')
                    self.spm_accounts.append(bot)
        
        # Fallback to single SPM account
        if not self.spm_accounts:
            spm_uid = os.environ.get('SPM_INV_UID', '')
            spm_pw = os.environ.get('SPM_INV_PASSWORD', '')
            if spm_uid and spm_pw:
                bot = BotConnection(spm_uid, spm_pw, 'SPM')
                self.spm_accounts.append(bot)
        
        # Connect all accounts
        tasks = []
        for bot in self.lag_accounts:
            tasks.append(bot.connect())
        for bot in self.spm_accounts:
            tasks.append(bot.connect())
        
        if tasks:
            await asyncio.gather(*tasks)
        
        self.initialized = True
        print(f"[POOL] ✅ Pool initialized - LAG: {len(self.lag_accounts)}, SPM: {len(self.spm_accounts)}")
    
    def get_lag_bot(self):
        """Get available LAG bot from pool"""
        for bot in self.lag_accounts:
            if bot.connected:
                return bot
        return None
    
    def get_spm_bot(self):
        """Get available SPM bot from pool"""
        for bot in self.spm_accounts:
            if bot.connected:
                return bot
        return None
    
    async def shutdown(self):
        """Shutdown all connections"""
        print("[POOL] Shutting down connection pool...")
        tasks = []
        for bot in self.lag_accounts + self.spm_accounts:
            tasks.append(bot.disconnect())
        if tasks:
            await asyncio.gather(*tasks)


# Global connection pool instance
connection_pool = ConnectionPool()
