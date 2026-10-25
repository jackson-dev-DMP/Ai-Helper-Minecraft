from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from ai_logic import ask_ai_companion

app = FastAPI(title="Minecraft Allay AI Companion Terminal")

class CompanionRequest(BaseModel):
    prompt: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Allay AI Companion // Dashboard</title>
        <style>
            :root {
                --bg-main: #0d1117;
                --bg-panel: #161b22;
                --border-color: #30363d;
                --accent-green: #238636;
                --accent-glow: #55cdfc;
                --text-main: #c9d1d9;
                --text-dim: #8b949e;
            }
            body {
                background-color: var(--bg-main);
                color: var(--text-main);
                font-family: 'Segoe UI', Inter, monospace, sans-serif;
                margin: 0;
                padding: 20px;
                display: flex;
                height: 90vh;
                box-sizing: border-box;
                gap: 15px;
            }
            /* Layout Columns */
            .sidebar-left { width: 25%; background: var(--bg-panel); border: 1px solid var(--border-color); border-radius: 8px; padding: 15px; display: flex; flex-direction: column; overflow-y: auto; }
            .main-console { width: 50%; background: var(--bg-panel); border: 1px solid var(--border-color); border-radius: 8px; padding: 20px; display: flex; flex-direction: column; justify-content: space-between; }
            .sidebar-right { width: 25%; background: var(--bg-panel); border: 1px solid var(--border-color); border-radius: 8px; padding: 15px; display: flex; flex-direction: column; overflow-y: auto; }

            /* Headers & Badges */
            h2, h3 { margin-top: 0; color: #fff; font-size: 1rem; border-bottom: 1px solid var(--border-color); padding-bottom: 8px; }
            .badge { background: #21262d; border: 1px solid var(--border-color); padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; color: var(--accent-glow); }
            
            /* Quest Log / Logs */
            .log-item { display: flex; align-items: center; gap: 8px; font-size: 0.85rem; margin-bottom: 10px; color: var(--text-dim); }
            .log-item.active { color: #fff; font-weight: bold; }
            
            /* Central Console Display */
            .profile-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 10px; }
            .terminal-output { flex-grow: 1; background: #0a0c10; border: 1px solid var(--border-color); border-radius: 6px; padding: 15px; margin: 15px 0; overflow-y: auto; font-family: monospace; white-space: pre-wrap; font-size: 0.95rem; color: #7ee787; }
            
            /* Input Area */
            .input-box { display: flex; gap: 10px; align-items: center; background: #0a0c10; border: 1px solid var(--border-color); border-radius: 6px; padding: 8px 12px; }
            .input-box input { flex-grow: 1; background: transparent; border: none; color: #fff; font-size: 1rem; outline: none; }
            .send-btn { background: var(--accent-green); color: #fff; border: none; width: 36px; height: 36px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; font-weight: bold; }
            .send-btn:hover { background: #2ea043; }
            
            /* Skills panel */
            .skill-card { background: #0a0c10; border: 1px solid var(--border-color); border-radius: 6px; padding: 10px; font-size: 0.85rem; margin-bottom: 10px; }
        </style>
    </head>
    <body>

        <!-- Left Panel: System Status -->
        <div class="sidebar-left">
            <h2>SYSTEM LOG</h2>
            <div class="log-item active">🟢 System Online: Gemini 2.5 Flash</div>
            <div class="log-item">🟢 Web Dashboard Synced</div>
            <div class="log-item">⚪ Minecraft Bedrock Listener</div>
            <div class="log-item">⚪ Context Telemetry Ready</div>
            <hr style="border: 0; border-top: 1px solid var(--border-color); margin: 15px 0;">
            <div style="font-size: 0.8rem; color: var(--text-dim);">
                <b>Status:</b> Autonomous Allay companion linked to Render cloud architecture.
            </div>
        </div>

        <!-- Main Console -->
        <div class="main-console">
            <div>
                <div class="profile-header">
                    <div>
                        <span style="font-size: 1.2rem; font-weight: bold; color: #fff;">Allay Companion</span> 
                        <span class="badge">GEMINI 2.5 FLASH</span>
                    </div>
                    <span style="font-size: 0.85rem; color: var(--text-dim);">API: Connected</span>
                </div>
            </div>

            <!-- Output Window -->
            <div class="terminal-output" id="terminalOutput">System ready. Awaiting prompt input from web terminal or Minecraft world...</div>

            <!-- Input Bar -->
            <div class="input-box">
                <input type="text" id="promptInput" placeholder="Send a message to Allay..." onkeydown="if(event.key === 'Enter') sendToAllay()">
                <button class="send-btn" onclick="sendToAllay()">▲</button>
            </div>
        </div>

        <!-- Right Panel: Skills -->
        <div class="sidebar-right">
            <h2>CAPABILITIES</h2>
            <div class="skill-card">
                <b>⭐ ask_gemini_companion</b>
                <div style="color: var(--text-dim); margin-top: 4px; font-size: 0.8rem;">
                    Processes tactical queries, inventory assistance, and survival guidance for Minecraft Bedrock.
                </div>
            </div>
        </div>

        <script>
            async function sendToAllay() {
                const inputField = document.getElementById('promptInput');
                const outputDiv = document.getElementById('terminalOutput');
                const text = inputField.value.trim();
                if (!text) return;

                outputDiv.innerText += `\\n> ${text}\\n[Allay]: Consulting neural link...`;
                inputField.value = '';

                try {
                    const res = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ prompt: text })
                    });
                    const data = await res.json();
                    outputDiv.innerText += `\\n[Allay]: ${data.reply}\\n`;
                    outputDiv.scrollTop = outputDiv.scrollHeight;
                } catch (err) {
                    outputDiv.innerText += `\\n[ERROR]: Failed to reach cloud backend.\\n`;
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
    
