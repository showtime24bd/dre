import os
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import json
import main
import requests , os , psutil , sys , jwt , pickle , json , binascii , time , urllib3 , base64 , datetime , re , socket , threading , ssl , pytz , aiohttp
from protobuf_decoder.protobuf_decoder import Parser
from xC4 import * ; from xHeaders import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from Pb2 import DEcwHisPErMsG_pb2 , MajoRLoGinrEs_pb2 , PorTs_pb2 , MajoRLoGinrEq_pb2 , sQ_pb2 , Team_msg_pb2
from cfonts import render, say
import asyncio
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from emote_shortcuts import BASE_EMOTES

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration - Delta Rare Exe
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("BOT_TOKEN environment variable not set!")
    print("Error: Please set BOT_TOKEN environment variable")

# Load emotes from JSON file
def load_emotes():
    try:
        with open('emotes.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading emotes: {e}")
        return []

# Global variables
emotes_data = load_emotes()

# Helper functions
def get_emote_by_number(number):
    for emote in emotes_data:
        if emote['Number'] == str(number):
            return emote
    return None

def get_emote_by_id(emote_id):
    for emote in emotes_data:
        if emote['Id'] == str(emote_id):
            return emote
    return None

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when command /start is issued."""
    welcome_text = """
🔥 *FREE FIRE BOT COMMANDS* 🔥

📌 *BASIC TEAM COMMANDS*
/2 [UID] - CREATE 2-PLAYER TEAM
/3 [UID] - CREATE 3-PLAYER TEAM 
/4 [UID] - CREATE 4-PLAYER TEAM
/5 [UID] - CREATE 5-PLAYER TEAM
/6 [UID] - CREATE 6-PLAYER TEAM
/join [CODE] - JOIN SPECIFIC TEAM

💣 *SPAM FUNCTIONS*  
/spam_inv [UID] - SEND MULTIPLE GROUP INVITES
/lag [CODE] - TEAM CODE SPAM

💃 *DANCE COMMANDS*
/c [teamcode] [uid] [number]
/e [teamcode] [uid1] [uid2] ... [emote_id]

🤖 *OTHER COMMANDS*
/help - SHOW THIS HELP MENU
/emotes - LIST ALL AVAILABLE EMOTES
/emote [number] - GET EMOTE INFO BY NUMBER
    """
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message when command /help is issued."""
    help_text = """
🔥 *FREE FIRE BOT COMMANDS* 🔥

📌 *BASIC TEAM COMMANDS*
/2 [UID] - CREATE 2-PLAYER TEAM
/3 [UID] - CREATE 3-PLAYER TEAM 
/4 [UID] - CREATE 4-PLAYER TEAM
/5 [UID] - CREATE 5-PLAYER TEAM
/6 [UID] - CREATE 6-PLAYER TEAM
/join [CODE] - JOIN SPECIFIC TEAM

💣 *SPAM FUNCTIONS*  
/spam_inv [UID] - SEND MULTIPLE GROUP INVITES
/lag [CODE] - TEAM CODE SPAM

💃 *DANCE COMMANDS*
/c [teamcode] [uid] [number] - SEND EMOTE BY NUMBER
/e [teamcode] [uid1] [uid2] ... [emote_id] - SEND EMOTE BY ID

🤖 *OTHER COMMANDS*
/help - SHOW THIS HELP MENU
/emotes - LIST ALL AVAILABLE EMOTES
/emote [number] - GET EMOTE INFO BY NUMBER

⚡ *QUICK START*
1. Use /2 [UID] to create 2-player team
2. Use /c [teamcode] [uid] [1] to send emote 1
3. Use /spam_inv [UID] to spam invites
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def create_team_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create 2-player team."""
    if not context.args:
        await update.message.reply_text("❌ Usage: /2 [UID]")
        return
    
    uid = context.args[0]
    await update.message.reply_text(f"✅ Creating 2-player team for UID: {uid}")

async def create_team_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create 3-player team."""
    if not context.args:
        await update.message.reply_text("❌ Usage: /3 [UID]")
        return
    
    uid = context.args[0]
    await update.message.reply_text(f"✅ Creating 3-player team for UID: {uid}")

async def create_team_4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create 4-player team."""
    if not context.args:
        await update.message.reply_text("❌ Usage: /4 [UID]")
        return
    
    uid = context.args[0]
    await update.message.reply_text(f"✅ Creating 4-player team for UID: {uid}")

async def create_team_5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create 5-player team."""
    if not context.args:
        await update.message.reply_text("❌ Usage: /5 [UID]")
        return
    
    uid = context.args[0]
    await update.message.reply_text(f"✅ Creating 5-player team for UID: {uid}")

async def create_team_6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create 6-player team."""
    if not context.args:
        await update.message.reply_text("❌ Usage: /6 [UID]")
        return
    
    uid = context.args[0]
    await update.message.reply_text(f"✅ Creating 6-player team for UID: {uid}")

async def join_team(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Join specific team."""
    if not context.args:
        await update.message.reply_text("❌ Usage: /join [TEAM_CODE]")
        return
    
    team_code = context.args[0]
    await update.message.reply_text(f"✅ Joining team: {team_code}")

async def spam_invite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send multiple group invites - works in private & groups."""
    if not context.args:
        await update.message.reply_text("❌ Usage: /spam_inv [UID]")
        return
    
    uid = context.args[0]
    # Queue command for main bot
    command_queue.put(("spam_inv", uid))
    await update.message.reply_text(f"🚀 Starting spam invites to UID: {uid}\n⏳ Check main bot console for progress")

async def lag_team(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Team code spam/lag - works in private & groups."""
    if not context.args:
        await update.message.reply_text("❌ Usage: /lag [TEAM_CODE]")
        return
    
    team_code = context.args[0]
    # Queue command for main bot
    command_queue.put(("lag", team_code))
    await update.message.reply_text(f"💥 Starting lag attack on team: {team_code}\n⏳ Check main bot console for progress")

async def dance_command_c(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send emote using number mapping - works in private & groups."""
    if len(context.args) < 3:
        await update.message.reply_text("❌ Usage: /c [teamcode] [uid] [emote_number]")
        return
    
    team_code = context.args[0]
    uid = context.args[1]
    emote_number = context.args[2]
    
    emote = get_emote_by_number(emote_number)
    if not emote:
        await update.message.reply_text(f"❌ Emote number {emote_number} not found!")
        return
    
    # Queue command for main bot
    command_queue.put(("emote", team_code, uid, emote['Id']))
    await update.message.reply_text(
        f"💃 Sending emote to team {team_code}\n"
        f"👤 Target UID: {uid}\n"
        f"🎭 Emote: #{emote_number} (ID: {emote['Id']})"
    )

async def dance_command_e(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send emote using emote ID - works in private & groups."""
    if len(context.args) < 3:
        await update.message.reply_text("❌ Usage: /e [teamcode] [uid1] [uid2] ... [emote_id]")
        return
    
    team_code = context.args[0]
    emote_id = context.args[-1]
    uids = context.args[1:-1]
    
    emote = get_emote_by_id(emote_id)
    if not emote:
        await update.message.reply_text(f"❌ Emote ID {emote_id} not found!")
        return
    
    # Queue command for main bot
    for uid in uids:
        command_queue.put(("emote", team_code, uid, emote_id))
    
    await update.message.reply_text(
        f"💃 Sending emote to team {team_code}\n"
        f"👥 Target UIDs: {', '.join(uids)}\n"
        f"🎭 Emote ID: {emote_id} (Number: {emote['Number']})"
    )

async def list_emotes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all available emotes."""
    # Show first 20 emotes to avoid message too long
    emote_list = []
    for emote in emotes_data[:20]:
        if emote['Number'] != 'no':
            emote_list.append(f"#{emote['Number']}: {emote['Id']}")
    
    emote_text = "🎭 *Available Emotes (1-20):*\n" + "\n".join(emote_list)
    emote_text += "\n\nUse `/emote [number]` to get specific emote info"
    
    await update.message.reply_text(emote_text, parse_mode='Markdown')

async def emote_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get specific emote information."""
    if not context.args:
        await update.message.reply_text("❌ Usage: /emote [emote_number]")
        return
    
    emote_number = context.args[0]
    emote = get_emote_by_number(emote_number)
    
    if not emote:
        await update.message.reply_text(f"❌ Emote #{emote_number} not found!")
        return
    
    await update.message.reply_text(
        f"🎭 *Emote Information:*\n"
        f"🔢 Number: #{emote['Number']}\n"
        f"🆔 ID: {emote['Id']}\n"
        f"💃 Usage: `/c [teamcode] [uid] {emote['Number']}`"
    , parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages."""
    text = update.message.text
    await update.message.reply_text(
        f"🤖 I received your message: {text}\n"
        f"Use /help to see all available commands!"
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors."""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Start the bot."""
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not set! Exiting...")
        return
    
    # Create the Application with drop_pending_updates to handle conflicts
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("2", create_team_2))
    application.add_handler(CommandHandler("3", create_team_3))
    application.add_handler(CommandHandler("4", create_team_4))
    application.add_handler(CommandHandler("5", create_team_5))
    application.add_handler(CommandHandler("6", create_team_6))
    application.add_handler(CommandHandler("join", join_team))
    application.add_handler(CommandHandler("spam_inv", spam_invite))
    application.add_handler(CommandHandler("lag", lag_team))
    application.add_handler(CommandHandler("c", dance_command_c))
    application.add_handler(CommandHandler("e", dance_command_e))
    application.add_handler(CommandHandler("emotes", list_emotes))
    application.add_handler(CommandHandler("emote", emote_info))

    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Add error handler
    application.add_error_handler(error_handler)

    # Start the Bot with drop_pending_updates to avoid conflict with other instances
    print("🤖 Free Fire Bot is running...")
    print("Use /help to see available commands")
    print("Note: If you see 409 Conflict errors, another bot instance is running elsewhere")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()