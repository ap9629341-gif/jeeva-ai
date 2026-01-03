from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import (
    HTMLResponse,
    FileResponse,
    StreamingResponse
)
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from ai import stream_ai_reply

# =============================
# APP INIT
# =============================
app = FastAPI(
    title="Jeeva AI",
    description="Jeeva AI Backend with Streaming",
    version="1.0.0"
)

# =============================
# CORS (Browser + Android)
# =============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================
# STATIC FILES
# =============================
app.mount("/static", StaticFiles(directory="static"), name="static")

# =============================
# FRONTEND (MAIN APP)
# =============================
@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse("static/index.html")

@app.get("/app", response_class=HTMLResponse)
def serve_app():
    return FileResponse("static/index.html")

# =============================
# API ROOT / HEALTH
# =============================
@app.get("/api")
def api_root():
    return {
        "status": "Jeeva AI backend live",
        "streaming": "enabled"
    }

@app.get("/health")
def health():
    return {"ok": True}

# =============================
# CHAT REQUEST MODEL
# =============================
class ChatRequest(BaseModel):
    message: str
    language: str = "Hindi"
    role: str = "friend"

# =============================
# STREAMING CHAT ENDPOINT
# =============================
@app.post("/chat")
def chat(req: ChatRequest):
    full_reply = ""
    for chunk in stream_ai_reply(
        message=req.message,
        language=req.language,
        role=req.role,
        user="android_user"
    ):
        full_reply += chunk

    return {"reply": full_reply}



