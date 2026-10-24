from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai_logic import ask_ai_companion

app = FastAPI(title="Minecraft AI Companion Backend")

# Define the structure of incoming data from Minecraft
class MinecraftEvent(BaseModel):
    player_name: str
    action: str
    message: str

@app.get("/")
def read_root():
    return {"status": "AI Companion backend is online and ready!"}

@app.post("/api/companion/interact")
def interact_with_ai(event: MinecraftEvent):
    """
    Receives an event/log from Minecraft, feeds it to Gemini, 
    and returns the AI's decision or text response.
    """
    try:
        # Format the log into a clear prompt for Gemini
        prompt = f"Player [{event.player_name}] performed action [{event.action}] with message/context: '{event.message}'"
        
        # Get response from our Gemini module
        ai_response = ask_ai_companion(prompt)
        
        return {
            "status": "success",
            "ai_response": ai_response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
      
