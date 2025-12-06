#!/usr/bin/env python3
"""
Delta Bot Auto Start Script - Complete Solution
One command to install, configure and run everything
"""

import subprocess
import sys
import os
import time
import signal
import json
from threading import Thread
from pathlib import Path

CONFIG_FILE = "bot_config.json"
REQUIREMENTS_FILE = "requirements.txt"
VENV_DIR = "venv"
PYTHON_EXEC = "python3"
PORT = 5000

# Essential packages for bot
ESSENTIAL_PACKAGES = [
    'aiohttp', 'flask', 'flask-cors', 'psutil', 'pycryptodome',
    'python-telegram-bot', 'requests', 'httpx', 'cfonts', 'protobuf'
]

def load_config():
    """Load or create configuration"""
    config = {
        "venv_path": os.path.join(os.path.dirname(__file__), VENV_DIR),
        "python_path": PYTHON_EXEC,
        "auto_restart": True,
        "restart_delay": 10,
        "log_file": "bot_combined.log",
        "web_port": PORT,
        "web_host": "0.0.0.0",
        "install_deps": True
    }
    
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                loaded = json.load(f)
                config.update(loaded)
        except:
            pass
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
    
    return config

def run_command(cmd, timeout=60, capture_output=True):
    """Run shell command"""
    try:
        if capture_output:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True,
                timeout=timeout, executable='/bin/bash'
            )
            return result.returncode, result.stdout, result.stderr
        else:
            result = subprocess.run(
                cmd, shell=True, timeout=timeout,
                executable='/bin/bash'
            )
            return result.returncode, "", ""
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

def check_system_deps():
    """Check and install system dependencies"""
    print("🔧 Checking system dependencies...")
    
    deps = ["python3-venv", "python3-pip", "git", "screen"]
    for dep in deps:
        code, out, err = run_command(f"dpkg -l | grep -i {dep}")
        if code != 0:
            print(f"📦 Installing {dep}...")
            run_command(f"sudo apt install -y {dep}", timeout=120)

def setup_virtualenv(config):
    """Setup Python virtual environment"""
    venv_path = config["venv_path"]
    
    if os.path.exists(venv_path):
        print(f"✅ Virtual environment found at {venv_path}")
        return True
    
    print(f"📦 Creating virtual environment at {venv_path}...")
    code, out, err = run_command(f"{PYTHON_EXEC} -m venv {venv_path}")
    
    if code != 0:
        print(f"❌ Failed to create venv: {err}")
        return False
    
    print("✅ Virtual environment created successfully")
    return True

def install_packages(config):
    """Install Python packages"""
    venv_path = config["venv_path"]
    pip_path = os.path.join(venv_path, "bin", "pip")
    python_path = os.path.join(venv_path, "bin", "python")
    
    # Upgrade pip first
    print("🔄 Upgrading pip...")
    run_command(f"{pip_path} install --upgrade pip")
    
    # Install from requirements.txt if exists
    if os.path.exists(REQUIREMENTS_FILE):
        print("📦 Installing from requirements.txt...")
        code, out, err = run_command(
            f"{pip_path} install -r {REQUIREMENTS_FILE}",
            timeout=300
        )
        
        if code == 0:
            print("✅ Packages installed from requirements.txt")
            return True
        else:
            print(f"⚠️ Failed to install from requirements: {err[:200]}")
    
    # Install essential packages individually
    print("📦 Installing essential packages...")
    for package in ESSENTIAL_PACKAGES:
        print(f"  Installing {package}...")
        code, out, err = run_command(f"{pip_path} install {package}", timeout=60)
        if code != 0:
            print(f"  ⚠️ Failed to install {package}: {err[:100]}")
    
    # Verify installations
    print("🔍 Verifying installations...")
    code, out, err = run_command(
        f"{python_path} -c \"import aiohttp, flask, psutil, Crypto, telegram; print('✅ Core packages OK')\""
    )
    
    if code == 0:
        print("✅ All essential packages installed")
        return True
    else:
        print("❌ Some packages failed to install")
        return False

def create_startup_scripts(config):
    """Create startup scripts"""
    scripts = {
        "start_bot.sh": f"""#!/bin/bash
cd "{os.path.dirname(__file__)}"
source "{config['venv_path']}/bin/activate"
python3 start.py
""",
        
        "start_screen.sh": f"""#!/bin/bash
cd "{os.path.dirname(__file__)}"
screen -dmS deltabot bash -c 'source "{config['venv_path']}/bin/activate" && python3 start.py'
echo "Bot started in screen session. Attach with: screen -r deltabot"
""",
        
        "start_nohup.sh": f"""#!/bin/bash
cd "{os.path.dirname(__file__)}"
source "{config['venv_path']}/bin/activate"
nohup python3 start.py > {config['log_file']} 2>&1 &
echo "Bot started with nohup. PID: $!"
echo "Logs: tail -f {config['log_file']}"
""",
        
        "stop_bot.sh": f"""#!/bin/bash
pkill -f "start.py"
pkill -f "python.*start"
screen -S deltabot -X quit 2>/dev/null
echo "Bot stopped"
""",
        
        "restart_bot.sh": f"""#!/bin/bash
cd "{os.path.dirname(__file__)}"
./stop_bot.sh
sleep 2
./start_nohup.sh
""",
        
        "status.sh": f"""#!/bin/bash
echo "=== Bot Status ==="
ps aux | grep -E "(start.py|python.*bot)" | grep -v grep
echo ""
echo "=== Screen Sessions ==="
screen -ls | grep deltabot
echo ""
echo "=== Recent Logs ==="
tail -20 {config['log_file']} 2>/dev/null || echo "No log file found"
""",
        
        "auto_restart.sh": f"""#!/bin/bash
cd "{os.path.dirname(__file__)}"
while true; do
    ./start_nohup.sh
    sleep 10
    while pgrep -f "start.py" > /dev/null; do
        sleep 5
    done
    echo "[$(date)] Bot crashed. Restarting in 5 seconds..."
    sleep 5
done
"""
    }
    
    for filename, content in scripts.items():
        with open(filename, 'w') as f:
            f.write(content)
        run_command(f"chmod +x {filename}")
        print(f"✅ Created {filename}")
    
    print("\n📋 Available scripts:")
    for script in scripts.keys():
        print(f"  ./{script}")

def create_systemd_service(config):
    """Create systemd service file"""
    service_content = f"""[Unit]
Description=Delta Bot Service
After=network.target

[Service]
Type=simple
User={os.getlogin()}
WorkingDirectory={os.path.dirname(__file__)}
ExecStart=/bin/bash -c 'source {config['venv_path']}/bin/activate && exec python3 {os.path.join(os.path.dirname(__file__), 'start.py')}'
Restart=always
RestartSec=10
StandardOutput=append:{config['log_file']}
StandardError=append:{config['log_file']}

[Install]
WantedBy=multi-user.target
"""
    
    service_file = "/etc/systemd/system/deltabot.service"
    
    print(f"🔧 Creating systemd service...")
    try:
        with open("deltabot.service", "w") as f:
            f.write(service_content)
        
        print("ℹ️ To install systemd service:")
        print(f"  sudo cp deltabot.service {service_file}")
        print("  sudo systemctl daemon-reload")
        print("  sudo systemctl enable deltabot")
        print("  sudo systemctl start deltabot")
        
    except Exception as e:
        print(f"⚠️ Could not create service file: {e}")

def run_bot(config, mode="direct"):
    """Run the bot in specified mode"""
    venv_python = os.path.join(config["venv_path"], "bin", "python")
    script_path = os.path.join(os.path.dirname(__file__), "start.py")
    
    modes = {
        "direct": f"source {config['venv_path']}/bin/activate && python3 {script_path}",
        "screen": f"screen -dmS deltabot bash -c 'source {config['venv_path']}/bin/activate && python3 {script_path}'",
        "nohup": f"source {config['venv_path']}/bin/activate && nohup python3 {script_path} > {config['log_file']} 2>&1 &",
        "pm2": f"pm2 start {script_path} --name deltabot --interpreter={venv_python}"
    }
    
    if mode not in modes:
        print(f"❌ Unknown mode: {mode}")
        return False
    
    print(f"🚀 Starting bot in {mode} mode...")
    code, out, err = run_command(modes[mode], capture_output=False)
    
    if code == 0 or mode == "nohup":
        print(f"✅ Bot started successfully!")
        
        if mode == "screen":
            print("   Attach to screen: screen -r deltabot")
        elif mode == "nohup":
            print(f"   Logs: tail -f {config['log_file']}")
            run_command(f"sleep 2 && tail -20 {config['log_file']}")
        elif mode == "pm2":
            print("   PM2 status: pm2 status")
        
        return True
    else:
        print(f"❌ Failed to start bot: {err}")
        return False

def display_instructions():
    """Display usage instructions"""
    print("\n" + "="*60)
    print("DELTA BOT - INSTALLATION COMPLETE")
    print("="*60)
    print("\n📋 QUICK START COMMANDS:")
    print("  ./start_bot.sh      - Start bot in current terminal")
    print("  ./start_screen.sh   - Start in screen session")
    print("  ./start_nohup.sh    - Start in background (recommended)")
    print("  ./stop_bot.sh       - Stop the bot")
    print("  ./restart_bot.sh    - Restart the bot")
    print("  ./status.sh         - Check bot status")
    print("  ./auto_restart.sh   - Auto-restart on crash")
    
    print("\n🌐 WEB PANEL:")
    print(f"  http://YOUR_VPS_IP:{PORT}")
    print(f"  http://localhost:{PORT} (if accessing locally)")
    
    print("\n📊 MONITORING:")
    print("  tail -f bot_combined.log     - View live logs")
    print("  ps aux | grep python         - Check running processes")
    print("  screen -r deltabot           - Attach to screen session")
    
    print("\n🔧 CONFIGURATION:")
    print(f"  Edit {CONFIG_FILE} to change settings")
    print("  Edit bot_config.json for bot-specific settings")
    
    print("\n⚠️  TROUBLESHOOTING:")
    print("  If bot doesn't start, check: ./status.sh")
    print("  View errors: tail -100 bot_combined.log | grep -i error")
    print("  Reinstall: Delete 'venv' folder and run this script again")
    print("="*60)

def main():
    """Main function"""
    print("="*60)
    print("DELTA BOT - AUTO SETUP & CONFIGURATION")
    print("="*60)
    
    # Step 1: Load config
    config = load_config()
    
    # Step 2: System dependencies
    check_system_deps()
    
    # Step 3: Setup virtual environment
    if not setup_virtualenv(config):
        sys.exit(1)
    
    # Step 4: Install packages
    if config.get("install_deps", True):
        if not install_packages(config):
            print("⚠️ Some packages failed to install. Continuing anyway...")
    
    # Step 5: Create startup scripts
    create_startup_scripts(config)
    
    # Step 6: Create systemd service (optional)
    create_systemd_service(config)
    
    # Step 7: Start the bot
    print("\n" + "="*60)
    print("STARTING THE BOT")
    print("="*60)
    
    start_mode = "nohup"  # Change to "direct", "screen", or "pm2"
    run_bot(config, mode=start_mode)
    
    # Step 8: Display instructions
    display_instructions()
    
    # Step 9: Keep script running if in direct mode
    if start_mode == "direct":
        try:
            print("\n📱 Bot is running. Press Ctrl+C to stop.")
            signal.pause()
        except KeyboardInterrupt:
            print("\n🛑 Stopping bot...")
            run_command("./stop_bot.sh")

if __name__ == '__main__':
    main()