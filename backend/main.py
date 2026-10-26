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
    # Détermine le chemin dynamique du fichier index.html dans le même dossier
    current_dir = os.path.dirname(os.path.realpath(__file__))
    html_path = os.path.join(current_dir, "index.html")
    
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h3>Error: index.html not found in backend directory.</h3>", status_code=500)

@app.post("/chat")
def chat_with_companion(req: CompanionRequest):
    result = ask_ai_companion(req.prompt, req.lobby_code, req.custom_api_key, req.gamertag, req.dev_password)
    return {
        "reply": result["reply"],
        "tokens_used": result["tokens_used"]
    }
    
