# Delta Rare Exe - Free Fire Emote Bot

## Overview
A Free Fire game bot with Telegram integration that sends emotes and manages game interactions. Features include a web-based control panel and shortcut system for easier emote management.

## Project Architecture
- **start.py** - Unified startup script (runs main.py + web_server.py together)
- **app.py** - Telegram Bot interface for commands
- **main.py** - Core Free Fire bot logic with TCP connections and web command queue consumer
- **web_server.py** - Flask web server for web-based emote control (Port 5000)
- **emote_shortcuts.py** - Emote shortcut configurations and mappings
- **command_queue.py** - File-based command queue for web-to-bot communication
- **connection_pool.py** - Connection pool for LAG and SPM accounts
- **keyauth_system.py** - KeyAuth integration for user authentication
- **templates/** - HTML templates (index.html, login.html)
- **Pb2/** - Protocol Buffer generated files
- **xC4.py** - Utility functions (encryption, packet creation)
- **xHeaders.py** - HTTP headers and API functions

## Features
- Telegram bot commands for emotes
- Web-based control panel (Bengali/English)
- Emote shortcuts system (/p, /ak, /scar, etc.)
- Multiple UID support
- Auto-leave squad feature
- Evolution emotes (1-21)
- Dance party feature

## How to Run
**Unified Startup (Recommended):**
```bash
python start.py
```
This will:
1. Check all dependencies
2. Run main.py (Core Free Fire Bot)
3. Run web_server.py (Web Control Panel on port 5000)

**Individual Components:**
- `python main.py` - Core bot only
- `python web_server.py` - Web panel only
- `python app.py` - Telegram bot only

## Suggested Improvements

### 🔴 High Priority
1. **Error Handling Enhancement** - Add try-catch blocks in main.py for network failures
2. **Logging System** - Implement proper file-based logging instead of print statements
3. **Rate Limiting** - Add rate limiting to web endpoints to prevent abuse
4. **Environment Validation** - Check all required secrets (BOT_UID, BOT_PASSWORD, BOT_TOKEN) on startup

### 🟡 Medium Priority
5. **Database Integration** - Store emote usage stats, user sessions in PostgreSQL
6. **API Documentation** - Add OpenAPI/Swagger docs for web endpoints
7. **Health Check Endpoint** - Add /health endpoint for monitoring
8. **Session Management** - Implement Redis for better session handling
9. **Input Validation** - Add stronger validation for UIDs and team codes

### 🟢 Low Priority
10. **Unit Tests** - Add pytest tests for core functions
11. **Docker Support** - Create Dockerfile for containerized deployment
12. **Performance Monitoring** - Add metrics collection for response times
13. **WebSocket Support** - Real-time updates instead of polling
14. **Code Refactoring** - Split main.py (3000+ lines) into smaller modules

## Credits
All development credits: **Delta Rare Exe**

## Recent Changes
- **[Dec 06, 2025]** Added start.py - Unified startup script that:
  - Checks all core dependencies automatically
  - Runs main.py (Core Bot) and web_server.py (Web Panel) simultaneously
  - Provides clean startup logs with status indicators
  - Run with: `python start.py`
- **[Dec 06, 2025]** Documented 14 suggested improvements (categorized by priority)
- Added web-based emote control panel
- Integrated emote shortcuts system from external repository
- Added command queue for web-to-bot communication
- Updated all credits to "Delta Rare Exe"
- **[Nov 26, 2025]** Added 430 emotes from ff-item.netlify.app (pages 1-6)
- **[Nov 26, 2025]** Updated emote_shortcuts.py with 300+ shortcut commands
- **[Nov 26, 2025]** Added new categories: Naruto, Demon Slayer, Premium, Frostfire, Blue Lock, and more
- **[Nov 26, 2025]** Added Group Invite feature in web control panel (4/5/6 player group invite by UID)
- **[Nov 26, 2025]** Redesigned UI with professional 2-tab interface: "Emote Send" and "Group Invite"
- **[Nov 26, 2025]** Added proper error handling and packet validation for group invites (OpEnSq, cHSq, SEnd_InV)
- **[Nov 27, 2025]** Fixed HWID not match issue in login system - now uses persistent browser-based HWID stored in localStorage
- **[Nov 27, 2025]** Made bot account configurable via secrets (BOT_UID and BOT_PASSWORD) instead of hardcoded values
- **[Nov 27, 2025]** Added separate account support for /spm_inv (SPM_INV_UID, SPM_INV_PASSWORD) and /lag (LAG_UID, LAG_PASSWORD) commands - these now use their own accounts and won't interfere with main bot operations
- **[Nov 27, 2025]** Added connection_pool.py for managing LAG and SPM account connections separately
- **[Nov 27, 2025]** Fixed Telegram Bot 409 Conflict issue - removed hardcoded token, using environment variable only
- **[Nov 27, 2025]** Added fallback mechanism - /lag and /spm_inv use pool accounts but fallback to main bot if unavailable
- **[Nov 27, 2025]** Fixed port 5000 conflict issue for Web Control Panel
- **[Nov 27, 2025]** Complete UI Redesign - Emote category section now more responsive and user-friendly:
  - Added horizontal scrolling category tabs for quick filtering
  - Collapsible accordion-style categories with emote count
  - Improved mobile responsiveness with touch-friendly buttons
  - Better visual hierarchy with gradient backgrounds
  - Sticky search bar for easy emote search
  - Improved emote cards with hover effects and selection states
  - Added "All" tab to show all emotes at once
- **[Nov 27, 2025]** Added Admin Password Login - Direct access without KeyAuth:
  - Admin tab in login form for direct password authentication
  - Bypass KeyAuth using environment variable ADMIN_PASSWORD
  - Default password: "admin123" (should be changed via secrets)
  - Set ADMIN_PASSWORD secret for production use
- **[Nov 27, 2025]** Synced ALL 430 Emotes to Website:
  - Organized into 7 categories by ID range
  - Basic Emotes (1-50): 50 emotes
  - Dance & Action (51-100): 50 emotes
  - Weapon & Combat (101-150): 50 emotes
  - Anime & Collab (151-200): 50 emotes
  - Holiday & Event (201-250): 50 emotes
  - Premium (251-300): 50 emotes
  - Extra Rare (301+): 130 emotes
  - All emote images reference: https://cdn.jsdelivr.net/gh/ShahGCreator/icon@main/PNG/
  - User can search/filter across all 430 emotes on website

## Emote Categories
- **Weapon Emotes**: /ak, /m10, /scar, /mp5, /groza, /thompson, /fist, /p90, /m60
- **Basic Emotes**: /hi, /bye, /lol, /clap, /love, /booyah, /king
- **Naruto Emotes**: /rasengan, /jutsu, /ninjarun, /clonejutsu, /fireballjutsu
- **Demon Slayer**: /thunderbreathing, /waterbreathing, /beastbreathing
- **Premium Emotes**: /l100, /max, /lambo, /prismaticflight, /bossenergy
- **Special Emotes**: /toiletman, /naatunaatu, /moonwalk, /flex, /twerk
