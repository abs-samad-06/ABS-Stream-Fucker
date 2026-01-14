import asyncio
import logging
from pyrogram import Client, idle
from config import Config
from bot.services.database import db_instance
from bot.services.scheduler import start_scheduler, stop_scheduler
from bot.handlers import start, ping, file, profile, admin, callbacks

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Main bot initialization"""
    logger.info("🚀 Starting ABS-Stream-Fucker Bot BC...")
    
    try:
        # Initialize database
        db = await db_instance.connect()
        
        # Create Pyrogram client
        app = Client(
            "abs_stream_fucker",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            sleep_threshold=60,
        )
        
        # Start the client
        await app.start()
        
        # Attach database to app
        app.db = db
        
        logger.info(f"✅ Bot started as @{Config.BOT_USERNAME}")
        
        # Register handlers
        start.register(app)
        ping.register(app)
        file.register(app)
        profile.register(app)
        admin.register(app)
        callbacks.register(app)
        
        logger.info("✅ All handlers registered MC!")
        
        # Start scheduler
        start_scheduler(app)
        
        logger.info("🎉 Bot is fully ready BC! Maa chod denge! 🔥")
        
        # Send startup message to owner
        try:
            await app.send_message(
                Config.OWNER_ID,
                "🚀 **Bot Started Successfully BC!** ✅\n\n"
                "ABS-Stream-Fucker is now online!\n\n"
                "**Status:** ✅ Running\n"
                "**Server:** Heroku\n"
                "**Mode:** Production\n\n"
                "Ready to fuck some files MC! 🔥"
            )
        except Exception as e:
            logger.error(f"Failed to send startup message: {e}")
        
        # Keep the bot running
        await idle()
        
    except KeyboardInterrupt:
        logger.info("⚠️ Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Bot crashed BC: {e}")
        raise
    finally:
        # Cleanup
        logger.info("🛑 Shutting down bot...")
        
        try:
            stop_scheduler()
            await app.stop()
            await db_instance.close()
        except:
            pass
        
        logger.info("👋 Bot stopped successfully")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
