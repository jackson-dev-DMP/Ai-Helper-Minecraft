from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from ai_logic import ask_ai_companion

app = FastAPI(title="Minecraft Allay AI Companion")

class CompanionRequest(BaseModel):
    prompt: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Minecraft Allay Companion - Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; background: #1a1a1a; color: #fff; text-align: center; padding: 50px; }
            .container { max-width: 600px; margin: auto; background: #2a2a2a; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
            h1 { color: #55cdfc; }
            textarea { width: 100%; height: 100px; background: #333; color: #fff; border: 1px solid #444; border-radius: 6px; padding: 10px; font-size: 16px; margin-bottom: 10px; }
            button { background: #55cdfc; color: #1a1a1a; border: none; padding: 10px 20px; font-size: 16px; font-weight: bold; border-radius: 6px; cursor: pointer; }
            button:hover { background: #3fa9db; }
            #response { margin-top: 20px; background: #1f1f1f; padding: 15px; border-radius: 6px; text-align: left; min-height: 50px; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧚‍♂️ Allay AI Companion</h1>
            <p>Your autonomous Gemini tactical guide for Minecraft Bedrock!</p>
            <textarea id="promptInput" placeholder="Ask your Allay for crafting recipes, survival tips, or coordinate analysis..."></textarea>
            <br>
            <button onclick="askAllay()">Ask Allay</button>
            <h3>Companion Response:</h3>
            <div id="response">Waiting for query...</div>
        </div>

        <script>
            async function askAllay() {
                const prompt = document.getElementById('promptInput').value;
                const responseDiv = document.getElementById('response');
                if (!prompt) return;
                
                responseDiv.innerText = "✨ Allay is thinking...";
                
                try {
                    const res = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ prompt: prompt })
                    });
                    const data = await res.json();
                    responseDiv.innerText = data.reply || "No response received.";
                } catch (err) {
                    responseDiv.innerText = "Error connecting to the cloud backend.";
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/chat")
def chat_with_companion(req: CompanionRequest):
    reply = ask_ai_companion(req.prompt)
    return {"reply": reply}
    
