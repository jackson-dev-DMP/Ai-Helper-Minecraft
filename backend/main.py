from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from ai_logic import ask_ai_companion

app = FastAPI(title="Minecraft AI Companion Backend")

# Define the structured data coming from Minecraft
class EnvironmentData(BaseModel):
    position: Optional[Dict[str, int]] = None
    health: Optional[int] = None
    nearby_blocks: Optional[List[str]] = []
    nearby_mobs: Optional[List[str]] = []
    inventory: Optional[List[str]] = []

class MinecraftEvent(BaseModel):
    session_code: str  # Keeps worlds separated securely!
    player_name: str
    action: str        # e.g., "chat_command" or "world_snapshot"
    message: str
    environment: Optional[EnvironmentData] = None

@app.get("/")
def read_root():
    return {"status": "AI Companion backend is online and ready!"}

@app.post("/api/companion/interact")
def interact_with_ai(event: MinecraftEvent):
    """
    Receives world telemetry and player chat from Minecraft,
    bundles it into a smart context, and asks Gemini.
    """
    try:
        # Build a rich context string for Gemini based on what the AI "sees"
        env_summary = ""
        if event.environment:
            pos = event.environment.position
            pos_str = f"X: {pos.get('x')}, Y: {pos.get('y')}, Z: {pos.get('z')}" if pos else "Unknown"
            env_summary = (
                f"\n[World Telemetry - Session: {event.session_code}]"
                f"\n- Player Position: {pos_str}"
                f"\n- Health: {event.environment.health}"
                f"\n- Nearby Blocks: {', '.join(event.environment.nearby_blocks) or 'None visible'}"
                f"\n- Nearby Mobs/Threats: {', '.join(event.environment.nearby_mobs) or 'None'}"
                f"\n- Inventory: {', '.join(event.environment.inventory) or 'Empty'}"
            )

        prompt = f"{env_summary}\n\nPlayer [{event.player_name}] says/requests: '{event.message}'"
        
        # Get response from Gemini
        ai_response = ask_ai_companion(prompt)
        
        return {
            "status": "success",
            "session_code": event.session_code,
            "ai_response": ai_response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
