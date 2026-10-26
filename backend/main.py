import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from ai_logic import ask_ai_companion

app = FastAPI(title="Minecraft Allay AI Companion Lobby Terminal v1.5 (BETA)")

# Global server-side memory for banned gamertags
banned_gamertags = set()

class CompanionRequest(BaseModel):
    prompt: str
    lobby_code: str = "Default-Lobby"
    custom_api_key: str = ""
    gamertag: str = ""
    dev_password: str = ""

class BanRequest(BaseModel):
    gamertag: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    target_names = ["index.html", "Index.html", "INDEX.HTML"]
    search_dirs = [current_dir, os.path.join(current_dir, ".."), "."]
    
    html_content = None
    for d in search_dirs:
        for name in target_names:
            full_path = os.path.join(d, name)
            if os.path.exists(full_path):
                with open(full_path, "r", encoding="utf-8") as f:
                    html_content = f.read()
                break
        if html_content:
            break
            
    if html_content:
        return HTMLResponse(content=html_content)
    
    return HTMLResponse(content="<h3>Error: index.html not found!</h3>", status_code=500)

@app.get("/api/banned")
def get_banned_users():
    return {"banned": list(banned_gamertags)}

@app.post("/api/ban")
def ban_user(req: BanRequest):
    gt = req.gamertag.strip().lower()
    if gt:
        banned_gamertags.add(gt)
    return {"success": True, "banned": list(banned_gamertags)}

@app.post("/api/unban")
def unban_user(req: BanRequest):
    gt = req.gamertag.strip().lower()
    if gt in banned_gamertags:
        banned_gamertags.remove(gt)
    return {"success": True, "banned": list(banned_gamertags)}

@app.post("/chat")
def chat_with_companion(req: CompanionRequest):
    gt_lower = req.gamertag.strip().lower()
    if gt_lower in banned_gamertags:
        raise HTTPException(status_code=403, detail="BANNED: You are banned from this terminal.")
        
    result = ask_ai_companion(req.prompt, req.lobby_code, req.custom_api_key, req.gamertag, req.dev_password)
    return {
        "reply": result["reply"],
        "tokens_used": result["tokens_used"]
    }
    
