# 🔥 ABS-Stream-Fucker Bot

**Ultimate File to Link Converter with Streaming & Download Support**

Made with 💀 and gaali!

---

## 🎯 Features

- 📤 **File Upload**: Upload any file (video, document, audio, zip, etc.)
- 🔗 **Link Generation**: Secure links with token + key authentication
- 🎬 **HD Streaming**: Browser-based video streaming with seek support
- 📥 **Fast Downloads**: Direct download with resume support
- 🔐 **Security**: HMAC-based key generation with master secret
- 💎 **Premium System**: Free vs Premium users with different features
- ⏰ **Link Expiry**: Automatic expiry for free users (24 hours default)
- 📊 **Admin Panel**: Stats, broadcast, premium management
- 🤖 **Telegram Bot**: Full-featured Telegram interface
- 🌐 **Web Server**: FastAPI-based streaming/download server

---

## 🚀 Deployment

### **Requirements**

- Python 3.11+
- MongoDB Database
- Heroku Account (or any VPS)
- Telegram Bot Token
- Telegram API ID & Hash

### **Environment Variables**

Create these in Heroku Config Vars or `.env` file:

```env
BOT_TOKEN=your_bot_token_here
API_ID=your_api_id
API_HASH=your_api_hash
DATABASE_URL=mongodb+srv://user:pass@cluster.mongodb.net/dbname
OWNER_ID=your_telegram_user_id
MASTER_SECRET=change-this-to-random-secret-key
BOT_USERNAME=ABSStreamFuckerBot
WEB_BASE_URL=https://your-app.herokuapp.com
FREE_LINK_EXPIRY_HOURS=24
FREE_USER_WAIT_TIME=15
Deploy to Heroku
Clone this repository
Create new Heroku app
Add MongoDB addon or use external MongoDB
Set all environment variables in Config Vars
Connect GitHub repo to Heroku
Deploy from main branch
# Or using Heroku CLI
heroku login
heroku create your-app-name
heroku config:set BOT_TOKEN=your_token
heroku config:set API_ID=your_id
# ... set all other vars
git push heroku main
Local Development
# Install dependencies
pip install -r requirements.txt

# Create .env file with variables
cp .env.example .env

# Edit .env with your values
nano .env

# Run bot
python -m bot.main

# Run web server (separate terminal)
python -m uvicorn web.app:app --reload --port 8080
📁 Project Structure
ABS-Stream-Fucker/
├── bot/
│   ├── handlers/          # Command & callback handlers
│   ├── services/          # Business logic
│   └── main.py           # Bot entry point
├── web/
│   ├── templates/        # HTML templates
│   ├── app.py           # FastAPI application
│   ├── stream.py        # File streaming logic
│   ├── middleware.py    # Request verification
│   └── errors.py        # Error pages
├── config.py            # Configuration
├── requirements.txt     # Dependencies
├── Procfile            # Heroku process file
├── runtime.txt         # Python version
└── README.md           # This file
🎮 Bot Commands
User Commands
/start - Start bot & welcome message
/ping - Check bot status
/profile - View your profile & stats
Owner Commands
/stats - Bot statistics
/addpremium user_id days - Add premium to user
/removepremium user_id - Remove premium from user
/broadcast - Broadcast message to all users (reply to message)
🔐 Security Features
Token-Based Authentication: Unique random tokens for each link
HMAC Key Generation: Secure key generation using master secret
Expiry System: Automatic link expiry for free users
Access Verification: Token + key verification on every request
Rate Limiting: Prevent abuse (configurable)
Direct Access Prevention: Cannot access files without valid token+key
💎 Premium Benefits
Feature
Free User
Premium User
Wait Time
15 seconds
Instant ⚡
Link Expiry
24 hours
Never 🔥
Download Speed
Normal
Max Speed 🚀
Support
Basic
Priority 💎
🛠 Tech Stack
Bot: Pyrogram (Telegram MTProto)
Web: FastAPI (async Python web framework)
Database: MongoDB (with motor async driver)
Streaming: Custom Telegram file streaming
Deployment: Heroku (or any VPS)
Scheduler: APScheduler (premium expiry checks)
📊 How It Works
User uploads file → Bot saves to Telegram + MongoDB
Bot generates links → Token + HMAC key created
User shares link → Others can stream/download
Access verification → Token + key verified on each request
File streaming → Direct from Telegram servers
Premium checks → Different experience for free/premium
⚠️ Important Notes
Master Secret: MUST be changed from default in production
Bot Token: Keep secret, never commit to Git
Database: Use MongoDB Atlas or hosted MongoDB
Heroku Dynos: Need 2 dynos (web + worker)
File Size: Telegram limit is 2GB per file
🐛 Troubleshooting
Bot not responding?
Check if worker dyno is running on Heroku
Verify BOT_TOKEN is correct
Check logs: heroku logs --tail
Web server not working?
Check if web dyno is running
Verify WEB_BASE_URL matches your Heroku app URL
Ensure PORT env var is set (Heroku sets automatically)
Links not working?
Verify MASTER_SECRET is same in bot and web
Check if links expired (for free users)
Verify database connection
Streaming issues?
Check if API_ID and API_HASH are correct
Verify file exists in Telegram
Check browser console for errors
📝 License
This project is for educational purposes.
Disclaimer: Use responsibly. Don't upload copyrighted content.
👨‍💻 Developer
Made with 💀 and gaali by ABS
Support: @your_channel
🔥 Gaali Disclaimer
Yes, bot me gaali hai. That's the vibe BC! 😈
But bot professionally kaam karta hai! 💪
Star ⭐ this repo if you like it MC!
---

# 🎉 **ALL FILES COMPLETE! 31/31** 🔥

Bhai **PURA BOT READY HAI!** 💀

## 📋 **Quick Checklist:**

✅ Runtime configuration  
✅ Dependencies  
✅ Heroku deployment files  
✅ Config with validation  
✅ Database services  
✅ Security system (token + key)  
✅ User management  
✅ File handling  
✅ Link generation  
✅ Premium system  
✅ Scheduler  
✅ All bot handlers  
✅ Web streaming server  
✅ Error pages  
✅ HTML templates  
✅ README documentation  
**
