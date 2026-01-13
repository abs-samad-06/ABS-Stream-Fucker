import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

async def save_file(db, file_data: dict) -> dict:
    """Save file metadata to database"""
    try:
        file_doc = {
            "file_id": file_data["file_id"],
            "file_unique_id": file_data["file_unique_id"],
            "file_name": file_data.get("file_name", "Unknown"),
            "file_size": file_data.get("file_size", 0),
            "mime_type": file_data.get("mime_type", "application/octet-stream"),
            "uploader_id": file_data["uploader_id"],
            "upload_time": datetime.utcnow(),
        }
        
        result = await db.files.update_one(
            {"file_unique_id": file_doc["file_unique_id"]},
            {"$set": file_doc},
            upsert=True
        )
        
        if result.upserted_id:
            saved_file = await db.files.find_one({"_id": result.upserted_id})
        else:
            saved_file = await db.files.find_one({"file_unique_id": file_doc["file_unique_id"]})
        
        logger.info(f"✅ File saved: {file_doc['file_name'][:30]}...")
        return saved_file
    
    except Exception as e:
        logger.error(f"❌ File save failed BC: {e}")
        raise

async def get_file_by_id(db, file_id: str) -> Optional[dict]:
    """Get file by Telegram file_id"""
    try:
        return await db.files.find_one({"file_id": file_id})
    except Exception as e:
        logger.error(f"❌ File lookup failed: {e}")
        return None

async def get_file_by_unique_id(db, file_unique_id: str) -> Optional[dict]:
    """Get file by Telegram file_unique_id"""
    try:
        return await db.files.find_one({"file_unique_id": file_unique_id})
    except Exception as e:
        logger.error(f"❌ File lookup failed: {e}")
        return None

async def delete_file(db, file_id: str, user_id: int) -> bool:
    """Delete file and all associated links"""
    try:
        # Get file
        file_doc = await get_file_by_id(db, file_id)
        
        if not file_doc:
            return False
        
        # Check if user owns the file (or is owner)
        from config import Config
        if file_doc["uploader_id"] != user_id and user_id != Config.OWNER_ID:
            logger.warning(f"⚠️ Unauthorized delete attempt by user {user_id}")
            return False
        
        # Delete file
        await db.files.delete_one({"file_id": file_id})
        
        # Delete all associated links
        result = await db.links.delete_many({"file_id": file_id})
        
        logger.info(f"🗑 File deleted: {file_id[:10]}... with {result.deleted_count} links")
        return True
    
    except Exception as e:
        logger.error(f"❌ File deletion failed BC: {e}")
        return False

async def get_user_files(db, user_id: int, limit: int = 10) -> list:
    """Get files uploaded by user"""
    try:
        cursor = db.files.find({"uploader_id": user_id}).sort("upload_time", -1).limit(limit)
        files = await cursor.to_list(length=limit)
        return files
    except Exception as e:
        logger.error(f"❌ Failed to get user files: {e}")
        return []

async def get_last_uploaded_file(db, user_id: int) -> Optional[dict]:
    """Get last uploaded file by user"""
    try:
        return await db.files.find_one(
            {"uploader_id": user_id},
            sort=[("upload_time", -1)]
        )
    except Exception as e:
        logger.error(f"❌ Failed to get last file: {e}")
        return None

async def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"
