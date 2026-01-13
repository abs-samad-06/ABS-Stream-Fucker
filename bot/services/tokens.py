import logging
from datetime import datetime, timedelta
from typing import Optional
from config import Config
from bot.services.security import generate_token, generate_key

logger = logging.getLogger(__name__)

async def create_file_token(db, file_id: str, file_unique_id: str, user_id: int, is_premium: bool) -> dict:
    """Create token and key for file access"""
    try:
        # Generate token and key
        token = generate_token()
        key = generate_key(token, file_id)
        
        # Calculate expiry
        expiry = None
        if not is_premium:
            expiry = datetime.utcnow() + timedelta(hours=Config.FREE_LINK_EXPIRY_HOURS)
        
        # Create token document
        token_doc = {
            "token": token,
            "key": key,
            "file_id": file_id,
            "file_unique_id": file_unique_id,
            "user_id": user_id,
            "is_premium": is_premium,
            "created_at": datetime.utcnow(),
            "expiry_at": expiry,
            "access_count": 0,
            "last_accessed": None
        }
        
        # Insert into database
        await db.links.insert_one(token_doc)
        
        logger.info(f"✅ Token created for file {file_id[:10]}... by user {user_id}")
        return token_doc
    
    except Exception as e:
        logger.error(f"❌ Token creation failed BC: {e}")
        raise

async def get_token_data(db, token: str) -> Optional[dict]:
    """Get token data from database"""
    try:
        token_data = await db.links.find_one({"token": token})
        
        if not token_data:
            return None
        
        # Check expiry
        if token_data.get("expiry_at"):
            if token_data["expiry_at"] < datetime.utcnow():
                logger.info(f"⏰ Token expired: {token}")
                return None
        
        return token_data
    
    except Exception as e:
        logger.error(f"❌ Token lookup failed: {e}")
        return None

async def increment_access_count(db, token: str):
    """Increment access count for token"""
    try:
        await db.links.update_one(
            {"token": token},
            {
                "$inc": {"access_count": 1},
                "$set": {"last_accessed": datetime.utcnow()}
            }
        )
    except Exception as e:
        logger.error(f"❌ Failed to update access count: {e}")

async def delete_token(db, token: str) -> bool:
    """Delete token from database"""
    try:
        result = await db.links.delete_one({"token": token})
        return result.deleted_count > 0
    except Exception as e:
        logger.error(f"❌ Token deletion failed: {e}")
        return False

async def delete_all_file_tokens(db, file_id: str) -> int:
    """Delete all tokens for a specific file"""
    try:
        result = await db.links.delete_many({"file_id": file_id})
        logger.info(f"🗑 Deleted {result.deleted_count} tokens for file {file_id[:10]}...")
        return result.deleted_count
    except Exception as e:
        logger.error(f"❌ Failed to delete file tokens: {e}")
        return 0
