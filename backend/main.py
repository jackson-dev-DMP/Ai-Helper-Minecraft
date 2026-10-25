from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from ai_logic import ask_ai_companion

app = FastAPI(title="Minecraft Allay AI Companion Terminal")

class CompanionRequest(BaseModel):
    prompt: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Allay AI Companion // Token Economy Dashboard</title>
    <style>
        :root {
            --bg-main: #0d1117;
            --bg-panel: #161b22;
            --border-color: #30363d;
            --accent-green: #238636;
            --accent-glow: #55cdfc;
            --accent-warning: #d29922;
            --accent-danger: #f85149;
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
        .sidebar-left { width: 25%; background: var(--bg-panel); border: 1px solid var(--border-color); border-radius: 8px; padding: 15px; display: flex; flex-direction: column; overflow-y: auto; }
        .main-console { width: 50%; background: var(--bg-panel); border: 1px solid var(--border-color); border-radius: 8px; padding: 20px; display: flex; flex-direction: column; justify-content: space-between; }
        .sidebar-right { width: 25%; background: var(--bg-panel); border: 1px solid var(--border-color); border-radius: 8px; padding: 15px; display: flex; flex-direction: column; overflow-y: auto; }
        h2, h3 { margin-top: 0; color: #fff; font-size: 1rem; border-bottom: 1px solid var(--border-color); padding-bottom: 8px; }
        .badge { background: #21262d; border: 1px solid var(--border-color); padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; color: var(--accent-glow); }
        .log-item { display: flex; align-items: center; gap: 8px; font-size: 0.85rem; margin-bottom: 10px; color: var(--text-dim); }
        .log-item.active { color: #fff; font-weight: bold; }
        .profile-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 10px; }
        .terminal-output { flex-grow: 1; background: #0a0c10; border: 1px solid var(--border-color); border-radius: 6px; padding: 15px; margin: 15px 0; overflow-y: auto; font-family: monospace; white-space: pre-wrap; font-size: 0.95rem; color: #7ee787; }
        .input-box { display: flex; gap: 10px; align-items: center; background: #0a0c10; border: 1px solid var(--border-color); border-radius: 6px; padding: 8px 12px; }
        .input-box input { flex-grow: 1; background: transparent; border: none; color: #fff; font-size: 1rem; outline: none; }
        .send-btn { background: var(--accent-green); color: #fff; border: none; width: 36px; height: 36px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; font-weight: bold; }
        .send-btn:hover { background: #2ea043; }
        .token-meter-container { background: #0a0c10; border: 1px solid var(--border-color); border-radius: 6px; padding: 12px; margin-bottom: 15px; }
        .progress-bar-bg { background: #21262d; border-radius: 4px; height: 10px; width: 100%; margin-top: 8px; overflow: hidden; }
        .progress-bar-fill { background: var(--accent-green); height: 100%; width: 0%; transition: width 0.4s ease, background-color 0.4s ease; }
        .token-status-text { font-size: 0.8rem; margin-top: 6px; color: var(--text-dim); font-weight: bold; }
        .skill-card { background: #0a0c10; border: 1px solid var(--border-color); border-radius: 6px; padding: 10px; font-size: 0.85rem; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="sidebar-left">
        <h2>TOKEN ECONOMY</h2>
        <div class="token-meter-container">
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem;">
                <span>Session Tokens:</span>
                <span id="tokenCountText">0 / 5,000</span>
            </div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" id="tokenProgressBar"></div>
            </div>
            <div class="token-status-text" id="tokenStatusMsg">🟢 Status: Optimal Bandwidth</div>
        </div>
        <h2>SYSTEM LOG</h2>
        <div class="log-item active">🟢 Model: Gemini 3.8 Flash</div>
        <div class="log-item">🟢 Web Dashboard Synced</div>
        <div class="log-item">⚪ Minecraft Bedrock Listener</div>
    </div>

    <div class="main-console">
        <div>
            <div class="profile-header">
                <div>
                    <span style="font-size: 1.2rem; font-weight: bold; color: #fff;">Allay Companion</span> 
                    <span class="badge">GEMINI 3.8 FLASH</span>
                </div>
                <span style="font-size: 0.85rem; color: var(--text-dim);" id="connectionStatus">API: Connected</span>
            </div>
        </div>
        <div class="terminal-output" id="terminalOutput">System ready. Connected to Gemini 3.8 Flash. Type your prompt below or use 'Gemini <message>' in Minecraft!</div>
        <div class="input-box">
            <input type="text" id="promptInput" placeholder="Send a message to Allay..." onkeydown="if(event.key === 'Enter') sendToAllay()">
            <button class="send-btn" onclick="sendToAllay()">▲</button>
        </div>
    </div>

    <div class="sidebar-right">
        <h2>CAPABILITIES</h2>
        <div class="skill-card">
            <b>⭐ gemini_38_tactical_guide</b>
            <div style="color: var(--text-dim); margin-top: 4px; font-size: 0.8rem;">
                Powered by Gemini 3.8 Flash. Low-latency multi-turn guidance optimized for Minecraft survival engineering.
            </div>
        </div>
    </div>

    <script>
        let sessionTokens = 0;
        const maxTokenQuota = 5000;

        async function sendToAllay() {
            const inputField = document.getElementById('promptInput');
            const outputDiv = document.getElementById('terminalOutput');
            const text = inputField.value.trim();
            if (!text) return;

            if (sessionTokens >= maxTokenQuota) {
                outputDiv.innerText += "\\n[WARNING]: Token quota nearly exhausted! High usage detected. Please wait.\\n";
                return;
            }

            outputDiv.innerText += "\\n> " + text + "\\n[Allay]: Querying Gemini 3.8 Flash...";
            inputField.value = '';

            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt: text })
                });
                const data = await res.json();
                
                outputDiv.innerText += "\\n[Allay]: " + data.reply + "\\n";
                outputDiv.scrollTop = outputDiv.scrollHeight;

                if (data.tokens_used) {
                    sessionTokens += data.tokens_used;
                    updateTokenUI();
                }
            } catch (err) {
                outputDiv.innerText += "\\n[ERROR]: Failed to reach cloud backend.\\n";
            }
        }

        function updateTokenUI() {
            const percentage = Math.min(Math.round((sessionTokens / maxTokenQuota) * 100), 100);
            const progressBar = document.getElementById('tokenProgressBar');
            const tokenText = document.getElementById('tokenCountText');
            const statusMsg = document.getElementById('tokenStatusMsg');

            progressBar.style.width = percentage + '%';
            tokenText.innerText = sessionTokens + ' / ' + maxTokenQuota;

            if (percentage >= 85) {
                progressBar.style.backgroundColor = 'var(--accent-danger)';
                statusMsg.style.color = 'var(--accent-danger)';
                statusMsg.innerText = '🔴 HIGH USAGE: Please wait/throttle requests!';
            } else if (percentage >= 60) {
                progressBar.style.backgroundColor = 'var(--accent-warning)';
                statusMsg.style.color = 'var(--accent-warning)';
                statusMsg.innerText = '⚠️ Caution: Token usage rising.';
            } else {
                progressBar.style.backgroundColor = 'var(--accent-green)';
                statusMsg.style.color = 'var(--text-dim)';
                statusMsg.innerText = '🟢 Status: Optimal Bandwidth';
            }
        }
    </script>
</body>
</html>"""
    return HTMLResponse(content=html_content)

@app.post("/chat")
def chat_with_companion(req: CompanionRequest):
    result = ask_ai_companion(req.prompt)
    return {
        "reply": result["reply"],
        "tokens_used": result["tokens_used"]
    }
    
