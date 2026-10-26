import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from ai_logic import ask_ai_companion

app = FastAPI(title="Minecraft Allay AI Companion Lobby Terminal v1.5 (BETA)")

class CompanionRequest(BaseModel):
    prompt: str
    lobby_code: str = "Default-Lobby"
    custom_api_key: str = ""
    gamertag: str = ""
    dev_password: str = ""

@app.get("/", response_class=HTMLResponse)
def read_root():
    # On teste plusieurs chemins possibles pour index.html (selon d'où Render lance le serveur)
    possible_paths = [
        "index.html",
        "backend/index.html",
        os.path.join(os.path.dirname(__file__), "index.html"),
        os.path.join(os.path.dirname(__file__), "../index.html")
    ]
    
    html_content = None
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                html_content = f.read()
            break
            
    if html_content:
        return HTMLResponse(content=html_content)
    
    return HTMLResponse(content="<h3>Error: index.html not found. Place it in the root or backend/ folder!</h3>", status_code=500)

@app.post("/chat")
def chat_with_companion(req: CompanionRequest):
    result = ask_ai_companion(req.prompt, req.lobby_code, req.custom_api_key, req.gamertag, req.dev_password)
    return {
        "reply": result["reply"],
        "tokens_used": result["tokens_used"]
    }
    
