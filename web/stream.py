import logging
from io import BytesIO
from pyrogram import Client
from pyrogram.errors import FloodWait
from fastapi import Request
from fastapi.responses import StreamingResponse
import asyncio
from config import Config

logger = logging.getLogger(__name__)

# Global Pyrogram client for file streaming
stream_client = None

async def init_stream_client():
    """Initialize Pyrogram client for streaming"""
    global stream_client
    
    if stream_client is None:
        stream_client = Client(
            "web_streamer",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            in_memory=True
        )
        await stream_client.start()
        logger.info("✅ Stream client initialized")
    
    return stream_client

async def stream_file(file_id: str, request: Request):
    """
    Stream file from Telegram with range request support
    """
    try:
        client = await init_stream_client()
        
        # Get file info
        try:
            file_info = await client.get_file(file_id)
        except Exception as e:
            logger.error(f"❌ Failed to get file info: {e}")
            raise
        
        file_size = file_info.file_size
        
        # Parse range header
        range_header = request.headers.get("range")
        
        if range_header:
            # Range request
            range_match = range_header.replace("bytes=", "").split("-")
            start = int(range_match[0]) if range_match[0] else 0
            end = int(range_match[1]) if len(range_match) > 1 and range_match[1] else file_size - 1
        else:
            # Full file
            start = 0
            end = file_size - 1
        
        # Calculate chunk size
        chunk_size = min(1024 * 1024, end - start + 1)  # 1MB chunks
        
        async def file_streamer():
            """Generator for streaming file chunks"""
            try:
                offset = start
                
                while offset <= end:
                    try:
                        # Calculate current chunk size
                        current_chunk_size = min(chunk_size, end - offset + 1)
                        
                        # Download chunk
                        chunk = await client.download(
                            file_id,
                            file_size=file_size,
                            offset=offset,
                            limit=current_chunk_size
                        )
                        
                        if not chunk:
                            break
                        
                        yield chunk
                        offset += len(chunk)
                    
                    except FloodWait as e:
                        logger.warning(f"FloodWait: {e.value} seconds")
                        await asyncio.sleep(e.value)
                    
                    except Exception as e:
                        logger.error(f"❌ Streaming error: {e}")
                        break
            
            except Exception as e:
                logger.error(f"❌ File streamer failed: {e}")
        
        # Determine content type
        content_type = "video/mp4"  # Default
        
        # Build headers
        headers = {
            "Accept-Ranges": "bytes",
            "Content-Length": str(end - start + 1),
            "Content-Type": content_type,
        }
        
        if range_header:
            headers["Content-Range"] = f"bytes {start}-{end}/{file_size}"
            status_code = 206  # Partial Content
        else:
            status_code = 200
        
        return StreamingResponse(
            file_streamer(),
            status_code=status_code,
            headers=headers,
            media_type=content_type
        )
    
    except Exception as e:
        logger.error(f"❌ Stream file failed BC: {e}")
        raise

async def cleanup_stream_client():
    """Cleanup stream client"""
    global stream_client
    
    if stream_client:
        try:
            await stream_client.stop()
            logger.info("🛑 Stream client stopped")
        except:
            pass
