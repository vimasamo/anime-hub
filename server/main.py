from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from scraper import AnimeFLV

app = FastAPI()
flv = AnimeFLV()

# CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import sys

# API Endpoints
@app.get("/api/search")
async def search(q: str = None, genre: str = None, year: int = None, page: int = 1):
    try:
        return flv.search(query=q, genre=genre, year=year, page=page)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/latest")
async def get_latest():
    try:
        return flv.get_latest_episodes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/on-air")
async def get_on_air():
    try:
        return flv.get_on_air()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/genres")
async def get_genres():
    return flv.get_genres()

@app.get("/api/anime/{slug}")
async def get_anime(slug: str):
    try:
        return flv.get_anime_info(slug)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/episode/{slug}/{num}")
async def get_episode(slug: str, num: int):
    try:
        return {
            "anime": slug,
            "episode": num,
            "servers": flv.get_episode_videos(slug, num)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Determine frontend path (PyInstaller compatibility)
if hasattr(sys, '_MEIPASS'):
    # When running from .exe
    base_dir = sys._MEIPASS
else:
    # When running as script
    base_dir = os.path.dirname(os.path.dirname(__file__))

frontend_path = os.path.join(base_dir, "frontend")

if os.path.exists(frontend_path):
    app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")

    @app.get("/")
    async def read_index():
        return FileResponse(os.path.join(frontend_path, "index.html"))

    # Fallback for other files to be served relatively
    @app.get("/{file_path:path}")
    async def serve_static(file_path: str):
        full_path = os.path.join(frontend_path, file_path)
        if os.path.isfile(full_path):
            return FileResponse(full_path)
        return FileResponse(os.path.join(frontend_path, "index.html"))
else:
    @app.get("/")
    async def read_root():
        return {"status": "Anime Hub API is running", "message": "Frontend not found locally, serving API only."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
