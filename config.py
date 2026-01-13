import os
from typing import List

class Config:
    # Bot Configuration
    BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "")
    API_ID: int = int(os.environ.get("API_ID", "0"))
    API_HASH: str = os.environ.get("API_HASH", "")
    BOT_USERNAME: str = os.environ.get("BOT_USERNAME", "ABSStreamFuckerBot")
    
    # Database
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "")
    DATABASE_NAME: str = "abs_stream_fucker"
    
    # Owner
    OWNER_ID: int = int(os.environ.get("OWNER_ID", "0"))
    
    # Security
    MASTER_SECRET: str = os.environ.get("MASTER_SECRET", "change-this-ultra-secret-key")
    
    # Web Server
    WEB_BASE_URL: str = os.environ.get("WEB_BASE_URL", "https://your-app.herokuapp.com")
    PORT: int = int(os.environ.get("PORT", "8080"))
    
    # Link Expiry (hours)
    FREE_LINK_EXPIRY_HOURS: int = int(os.environ.get("FREE_LINK_EXPIRY_HOURS", "24"))
    
    # Wait Time (seconds)
    FREE_USER_WAIT_TIME: int = int(os.environ.get("FREE_USER_WAIT_TIME", "15"))
    
    # Premium
    PREMIUM_PLANS: dict = {
        "monthly": {"days": 30, "price": "₹99"},
        "yearly": {"days": 365, "price": "₹999"}
    }
    
    @classmethod
    def validate(cls):
        """Validate required environment variables"""
        required = [
            ("BOT_TOKEN", cls.BOT_TOKEN),
            ("API_ID", cls.API_ID),
            ("API_HASH", cls.API_HASH),
            ("DATABASE_URL", cls.DATABASE_URL),
            ("OWNER_ID", cls.OWNER_ID),
            ("MASTER_SECRET", cls.MASTER_SECRET),
        ]
        
        missing = [name for name, value in required if not value or (isinstance(value, int) and value == 0)]
        
        if missing:
            raise ValueError(f"❌ BC missing config: {', '.join(missing)}")
        
        if cls.MASTER_SECRET == "change-this-ultra-secret-key":
            raise ValueError("❌ MASTER_SECRET change kar le chutiye!")
        
        print("✅ Config validated successfully MC!")

# Validate on import
Config.validate()
