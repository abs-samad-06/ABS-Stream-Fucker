import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import Config
from web.middleware import verify_request, handle_error, get_db
from web.stream import stream_file, init_stream_client, cleanup_stream_client
from bot.services.files import get_file_by_id

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events"""
    # Startup
    logger.info("🚀 Starting web server BC...")
    await init_stream_client()
    logger.info("✅ Web server ready! 🔥")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down web server...")
    await cleanup_stream_client()

# Create FastAPI app
app = FastAPI(
    title="ABS-Stream-Fucker",
    description="File to Link Converter with Streaming",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ABS-Stream-Fucker</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                text-align: center;
                max-width: 500px;
            }
            h1 {
                color: #333;
                margin-bottom: 20px;
            }
            .emoji {
                font-size: 60px;
                margin-bottom: 20px;
            }
            p {
                color: #666;
                line-height: 1.6;
            }
            .btn {
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 30px;
                border-radius: 50px;
                text-decoration: none;
                margin-top: 20px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="emoji">🔥</div>
            <h1>ABS-Stream-Fucker</h1>
            <p>Ultimate File to Link Converter BC!</p>
            <p>Made with 💀 and gaali</p>
            <a href="https://t.me/ABSStreamFuckerBot" class="btn">🤖 Start Bot</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.get("/stream/{token}")
async def stream_endpoint(token: str, key: str, request: Request):
    """Stream file endpoint"""
    try:
        # Verify access
        success, token_data, error = await verify_request(request, token, key)
        
        if not success:
            return await handle_error(error)
        
        # Get file
        db = await get_db()
        file_doc = await get_file_by_id(db, token_data["file_id"])
        
        if not file_doc:
            return await handle_error("file_not_found")
        
        # Stream file
        return await stream_file(file_doc["file_id"], request)
    
    except Exception as e:
        logger.error(f"❌ Stream endpoint failed BC: {e}")
        return await handle_error("server_error")

@app.get("/download/{token}")
async def download_endpoint(token: str, key: str, request: Request):
    """Download file endpoint"""
    try:
        # Verify access
        success, token_data, error = await verify_request(request, token, key)
        
        if not success:
            return await handle_error(error)
        
        # Get file
        db = await get_db()
        file_doc = await get_file_by_id(db, token_data["file_id"])
        
        if not file_doc:
            return await handle_error("file_not_found")
        
        # Add download header
        headers = {
            "Content-Disposition": f'attachment; filename="{file_doc["file_name"]}"'
        }
        
        # Stream file with download header
        response = await stream_file(file_doc["file_id"], request)
        
        # Update headers
        for key, value in headers.items():
            response.headers[key] = value
        
        return response
    
    except Exception as e:
        logger.error(f"❌ Download endpoint failed BC: {e}")
        return await handle_error("server_error")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Bot alive hai BC! 🔥",
        "version": "1.0.0"
    }

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Handle 404 errors"""
    return await handle_error("invalid_token")

@app.exception_handler(500)
async def server_error_handler(request: Request, exc: Exception):
    """Handle 500 errors"""
    logger.error(f"Server error: {exc}")
    return await handle_error("server_error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=Config.PORT)
