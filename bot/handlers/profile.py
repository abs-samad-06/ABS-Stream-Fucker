import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.services.users import get_user_stats, is_premium

logger = logging.getLogger(__name__)

async def profile_handler(client: Client, message: Message):
    """Handle /profile command"""
    user_id = message.from_user.id
    
    try:
        # Get user stats
        stats = await get_user_stats(client.db, user_id)
        
        if not stats:
            await message.reply_text(
                "❌ **Profile nahi mili BC!**\n\n"
                "Pehle /start kar!"
            )
            return
        
        # Check premium
        premium = stats.get("is_premium", False)
        premium_text = "💎 **Premium MC**" if premium else "🆓 **Free User**"
        
        # Premium expiry
        expiry_text = ""
        if premium and stats.get("premium_expiry"):
            expiry = stats["premium_expiry"]
            expiry_text = f"\n⏰ **Expires:** {expiry.strftime('%d %b %Y, %I:%M %p')}"
        elif premium:
            expiry_text = "\n⚡ **Lifetime Premium BC!** 🔥"
        
        # Join date
        join_date = stats.get("join_date")
        join_text = join_date.strftime('%d %b %Y') if join_date else "Unknown"
        
        # Create profile message
        profile_text = (
            f"👤 **Teri Profile MC:** 🔥\n\n"
            f"**Name:** {stats.get('first_name', 'Unknown')}\n"
            f"**Username:** @{stats.get('username', 'none')}\n"
            f"**User ID:** `{stats['user_id']}`\n\n"
            f"**Status:** {premium_text}{expiry_text}\n"
            f"**Joined:** {join_text}\n\n"
            f"📊 **Statistics:**\n"
            f"• Files Uploaded: {stats.get('total_files', 0)}\n"
            f"• Links Generated: {stats.get('total_links', 0)}\n\n"
        )
        
        if not premium:
            profile_text += (
                "💎 **Premium le le BC!**\n"
                "Benefits:\n"
                "• No wait time\n"
                "• Links never expire\n"
                "• Faster speeds\n"
                "• Priority support\n\n"
                "Contact owner: /start 🚀"
            )
        else:
            profile_text += "✨ **Premium member hai tu! Enjoy kar MC!** 🎉"
        
        # Create buttons
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📁 My Files", callback_data="my_files"),
                InlineKeyboardButton("🔗 My Links", callback_data="my_links")
            ],
            [
                InlineKeyboardButton("💎 Premium Info", callback_data="premium_info")
            ],
            [
                InlineKeyboardButton("❌ Close", callback_data="close")
            ]
        ])
        
        await message.reply_text(profile_text, reply_markup=buttons)
    
    except Exception as e:
        logger.error(f"❌ Profile handler failed BC: {e}")
        await message.reply_text(
            "❌ **Error ho gaya MC!**\n\n"
            "Try again: /profile"
        )

def register(app: Client):
    """Register profile handler"""
    app.add_handler(filters.command("profile") & filters.private, profile_handler)
