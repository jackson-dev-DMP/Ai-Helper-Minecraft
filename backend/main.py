from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from ai_logic import ask_ai_companion

app = FastAPI(title="Minecraft AI Companion Backend")

# Enable CORS for dashboard web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for active world sessions
active_sessions: Dict[str, Dict[str, Any]] = {}

class EnvironmentData(BaseModel):
    position: Optional[Dict[str, int]] = None
    health: Optional[int] = None
    nearby_blocks: Optional[List[str]] = []
    nearby_mobs: Optional[List[str]] = []
    inventory: Optional[List[str]] = []

class MinecraftEvent(BaseModel):
    session_code: str
    player_name: str
    action: str
    message: str
    environment: Optional[EnvironmentData] = None

@app.get("/")
def read_root():
    return {"status": "AI Companion backend is online and ready!"}

@app.get("/api/companion/status/{session_code}")
def get_session_status(session_code: str):
    if session_code not in active_sessions:
        return {"status": "no_data", "message": "No activity recorded for this session code yet."}
    return {"status": "active", "data": active_sessions[session_code]}

@app.post("/api/companion/interact")
def interact_with_ai(event: MinecraftEvent):
    try:
        env_summary = ""
        env_dict = {}
        if event.environment:
            env_dict = event.environment.dict()
            pos = env_dict.get('position')
            pos_str = f"X: {pos.get('x')}, Y: {pos.get('y')}, Z: {pos.get('z')}" if pos else "Unknown"
            env_summary = (
                f"\n[World Telemetry - Session: {event.session_code}]"
                f"\n- Player Position: {pos_str}"
                f"\n- Health: {env_dict.get('health')}"
                f"\n- Nearby Blocks: {', '.join(env_dict.get('nearby_blocks', [])) or 'None visible'}"
                f"\n- Nearby Mobs/Threats: {', '.join(env_dict.get('nearby_mobs', [])) or 'None'}"
            )

        prompt = f"{env_summary}\n\nPlayer [{event.player_name}] says/requests: '{event.message}'"
        
        # Get AI response and format with Gemini tag
        raw_ai_response = ask_ai_companion(prompt)
        formatted_ai_response = f"Gemini: {raw_ai_response}"
        
        # Save state to active session memory
        active_sessions[event.session_code] = {
            "player_name": event.player_name,
            "last_message": event.message,
            "ai_response": formatted_ai_response,
            "environment": env_dict,
            "timestamp": "Just now"
        }
        
        return {
            "status": "success",
            "session_code": event.session_code,
            "ai_response": formatted_ai_response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
