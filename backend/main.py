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
    html_part_1 = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Allay AI Companion // Secure Terminal v1.5 (BETA)</title>
    <style>
        :root {
            --bg-main: #0d1117;
            --bg-panel: #161b22;
            --border-color: #30363d;
            --accent-green: #238636;
            --accent-glow: #55cdfc;
            --accent-warning: #d29922;
            --accent-danger: #f85149;
            --accent-dev: #a371f7;
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
        .sidebar-left { width: 28%; background: var(--bg-panel); border: 1px solid var(--border-color); border-radius: 8px; padding: 15px; display: flex; flex-direction: column; overflow-y: auto; gap: 12px; }
        .main-console { width: 44%; background: var(--bg-panel); border: 1px solid var(--border-color); border-radius: 8px; padding: 20px; display: flex; flex-direction: column; justify-content: space-between; }
        .sidebar-right { width: 28%; background: var(--bg-panel); border: 1px solid var(--border-color); border-radius: 8px; padding: 15px; display: flex; flex-direction: column; overflow-y: auto; gap: 12px; }
        
        h2, h3 { margin: 0 0 5px 0; color: #fff; font-size: 0.95rem; border-bottom: 1px solid var(--border-color); padding-bottom: 6px; }
        .badge { background: #21262d; border: 1px solid var(--border-color); padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; color: var(--accent-glow); font-weight: bold; }
        .badge-dev { background: rgba(163, 113, 247, 0.15); border: 1px solid var(--accent-dev); color: var(--accent-dev); }
        
        .control-group { background: #0a0c10; border: 1px solid var(--border-color); border-radius: 6px; padding: 10px; }
        .control-group label { font-size: 0.75rem; color: var(--text-dim); display: block; margin-bottom: 4px; }
        .control-group input, .control-group select { width: 100%; background: #161b22; border: 1px solid var(--border-color); color: #fff; padding: 6px; border-radius: 4px; box-sizing: border-box; font-size: 0.85rem; outline: none; }
        
        .btn { background: var(--accent-green); color: #fff; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-weight: bold; width: 100%; margin-top: 6px; font-size: 0.85rem; transition: background 0.2s; }
        .btn:hover { background: #2ea043; }
        .btn-danger { background: var(--accent-danger); }
        .btn-danger:hover { background: #da3633; }
        .btn-dev { background: var(--accent-dev); }
        .btn-dev:hover { background: #8957e5; }

        .terminal-output { flex-grow: 1; background: #0a0c10; border: 1px solid var(--border-color); border-radius: 6px; padding: 15px; margin: 10px 0; overflow-y: auto; font-family: monospace; white-space: pre-wrap; font-size: 0.9rem; color: #7ee787; }
        .input-box { display: flex; gap: 8px; align-items: center; background: #0a0c10; border: 1px solid var(--border-color); border-radius: 6px; padding: 6px 10px; }
        .input-box input { flex-grow: 1; background: transparent; border: none; color: #fff; font-size: 0.9rem; outline: none; }
        .send-btn { background: var(--accent-green); color: #fff; border: none; width: 32px; height: 32px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0; }
        
        .token-meter-container { background: #0a0c10; border: 1px solid var(--border-color); border-radius: 6px; padding: 10px; }
        .progress-bar-bg { background: #21262d; border-radius: 4px; height: 8px; width: 100%; margin-top: 6px; overflow: hidden; }
        .progress-bar-fill { background: var(--accent-green); height: 100%; width: 0%; transition: width 0.4s ease; }
        
        .lobby-card { background: #161b22; border: 1px solid var(--border-color); padding: 8px; border-radius: 4px; margin-bottom: 6px; font-size: 0.8rem; display: flex; justify-content: space-between; align-items: center; transition: all 0.2s ease; }
        .lobby-card-dev { background: rgba(163, 113, 247, 0.15); border: 1px solid var(--accent-dev); }
        .request-card { background: rgba(210, 153, 34, 0.1); border: 1px solid var(--accent-warning); padding: 8px; border-radius: 4px; margin-bottom: 6px; font-size: 0.8rem; }
        .player-item { background: #161b22; border: 1px solid var(--border-color); padding: 5px 8px; border-radius: 4px; margin-bottom: 4px; font-size: 0.8rem; display: flex; justify-content: space-between; align-items: center; }
        .player-item-dev { border: 1px solid var(--accent-dev); color: var(--accent-dev); font-weight: bold; }
    </style>
</head>
<body>
    <div class="sidebar-left">
        <h2>USER & SECURITY v1.5</h2>
        <div class="control-group">
            <label>Minecraft Gamertag:</label>
            <input type="text" id="gamertagInput" value="" placeholder="Enter your gamertag..." oninput="checkDeveloperStatus()">
            <div id="devPasswordContainer" style="margin-top: 6px; display: none;">
                <label>Developer Password:</label>
                <input type="password" id="devPasswordInput" placeholder="Enter secure password..." oninput="checkDeveloperStatus()">
            </div>
            <div id="devBadgeContainer" style="margin-top: 6px;"></div>
        </div>

        <div class="control-group">
            <label>Custom Gemini API Key (Optional):</label>
            <input type="password" id="customApiKey" placeholder="Leave blank to use server key">
        </div>

        <h2>ACTIVE LOBBIES</h2>
        <div class="control-group">
            <label>Start / Host New Lobby:</label>
            <input type="text" id="newLobbyCode" placeholder="e.g. SurvivalRoom">
            <button class="btn" onclick="startNewLobby()">Start Lobby</button>
        </div>
        <div id="activeLobbiesList" style="max-height: 140px; overflow-y: auto;">
            <div class="lobby-card">
                <span><b>Default-Lobby</b></span>
                <div style="display: flex; gap: 4px;">
                    <button class="btn" style="width: auto; padding: 2px 6px; margin:0;" onclick="joinLobby('Default-Lobby')">Join</button>
                    <button class="btn btn-danger" style="width: auto; padding: 2px 6px; margin:0; display:none;" id="del-Default-Lobby" onclick="deleteLobby('Default-Lobby')">Delete</button>
                </div>
            </div>
        </div>
    </div>
"""

    html_part_2 = """
    <div class="main-console">
        <div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 8px;">
                <div>
                    <span style="font-size: 1.1rem; font-weight: bold; color: #fff;">Allay Companion v1.5 (BETA)</span> 
                    <span class="badge" id="activeLobbyBadge">LOBBY: Default-Lobby</span>
                </div>
                <div id="headerStatusBadge"></div>
            </div>
        </div>
        <div class="terminal-output" id="terminalOutput">[00:00:01] System v1.5 (BETA) ready. Enter your gamertag to begin chatting in Default-Lobby!</div>
        <div class="input-box">
            <input type="text" id="promptInput" placeholder="Send a message to Allay..." onkeydown="if(event.key === 'Enter') sendToAllay()">
            <button class="send-btn" onclick="sendToAllay()">▲</button>
        </div>
    </div>

    <div class="sidebar-right">
        <h2>PLAYERS IN LOBBY</h2>
        <div id="playersListContainer" style="max-height: 120px; overflow-y: auto; margin-bottom: 10px;">
            <div class="player-item"><span>No active players</span></div>
        </div>

        <h2>TOKEN ECONOMY</h2>
        <div class="token-meter-container">
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem;">
                <span>Session Tokens:</span>
                <span id="tokenCountText">0 / 5,000</span>
            </div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" id="tokenProgressBar"></div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 6px;">
                <span style="font-size: 0.75rem; color: var(--text-dim);" id="tokenStatusMsg">🟢 Optimal Bandwidth</span>
                <button class="btn" style="width: auto; margin:0; padding:2px 6px; font-size:0.7rem;" onclick="resetTokens()">Reset</button>
            </div>
        </div>

        <h2>INCOMING REQUESTS</h2>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-size: 0.75rem; color: var(--text-dim);">Queue Control:</span>
            <button class="btn btn-danger" style="width: auto; padding: 2px 6px; margin:0; font-size:0.75rem;" onclick="cancelAllRequests()">Cancel All</button>
        </div>
        <div id="minecraftRequestsContainer" style="font-size: 0.8rem; color: var(--text-dim); max-height: 160px; overflow-y: auto;">
            <div class="request-card">
                <div><b>Friend:</b> TEST</div>
                <div>Wants to join lobby & spawn Guest Allay.</div>
                <div style="display: flex; gap: 5px; margin-top: 5px;">
                    <button class="btn" style="margin:0; padding:2px 6px;" onclick="approveRequest(this, true)">Accept</button>
                    <button class="btn btn-danger" style="margin:0; padding:2px 6px;" onclick="approveRequest(this, false)">Deny</button>
                </div>
            </div>
        </div>
    </div>
"""

    html_part_3 = """
    <script>
        let sessionTokens = 0;
        const maxTokenQuota = 5000;
        let activeLobbies = ["Default-Lobby"];
        let lobbyPlayers = {};
        let isDevAuthenticated = false;

        window.onload = function() {
            checkDeveloperStatus();
        };

        function getTimeString() {
            const now = new Date();
            return now.toTimeString().split(' ')[0];
        }

        function checkDeveloperStatus() {
            const gt = document.getElementById('gamertagInput').value.trim().toLowerCase();
            const pass = document.getElementById('devPasswordInput').value.trim();
            const badgeContainer = document.getElementById('devBadgeContainer');
            const headerStatus = document.getElementById('headerStatusBadge');
            const passContainer = document.getElementById('devPasswordContainer');

            if (gt === 'jackson22510') {
                passContainer.style.display = 'block';
                if (pass === 'Jackson140715') {
                    isDevAuthenticated = true;
                    badgeContainer.innerHTML = '<span class="badge badge-dev">🚀 DEVELOPER LOBBY (ADMIN)</span>';
                    headerStatus.innerHTML = '<span class="badge badge-dev">ROOT ADMIN</span>';
                } else {
                    isDevAuthenticated = false;
                    badgeContainer.innerHTML = '<span style="font-size: 0.75rem; color: var(--accent-warning);">⚠️ Enter Dev Password</span>';
                    headerStatus.innerHTML = '<span class="badge">PENDING AUTH</span>';
                }
            } else {
                isDevAuthenticated = false;
                passContainer.style.display = 'none';
                badgeContainer.innerHTML = '<span style="font-size: 0.75rem; color: var(--text-dim);">Standard User Mode</span>';
                headerStatus.innerHTML = '<span class="badge">GUEST MODE</span>';
            }

            const currentLobby = document.getElementById('activeLobbyBadge').innerText.replace("LOBBY: ", "");
            const activeGt = document.getElementById('gamertagInput').value.trim();
            if (activeGt && isDevAuthenticated) {
                if (!lobbyPlayers[currentLobby]) lobbyPlayers[currentLobby] = [];
                if (!lobbyPlayers[currentLobby].includes(activeGt)) lobbyPlayers[currentLobby].push(activeGt);
            }

            updateLobbiesUI();
            updatePlayersUI();
        }

        function startNewLobby() {
            const codeInput = document.getElementById('newLobbyCode');
            const code = codeInput.value.trim();
            if (!code) return;

            if (!activeLobbies.includes(code)) {
                activeLobbies.push(code);
                updateLobbiesUI();
            }
            joinLobby(code);
            codeInput.value = '';
            document.getElementById('terminalOutput').innerText += "\\n[" + getTimeString() + "]: Created & joined lobby '" + code + "'!";
        }

        function joinLobby(code) {
            document.getElementById('activeLobbyBadge').innerText = "LOBBY: " + code;
            document.getElementById('terminalOutput').innerText += "\\n[" + getTimeString() + "]: Switched active session to lobby '" + code + "'.";
            
            const gt = document.getElementById('gamertagInput').value.trim();
            if (gt) {
                if (!lobbyPlayers[code]) lobbyPlayers[code] = [];
                if (!lobbyPlayers[code].includes(gt)) lobbyPlayers[code].push(gt);
            }
            updateLobbiesUI();
            updatePlayersUI();
        }

        function deleteLobby(code) {
            if (!isDevAuthenticated) {
                alert("Access Denied: Only Dev Admin can delete lobbies!");
                return;
            }
            activeLobbies = activeLobbies.filter(l => l !== code);
            if (activeLobbies.length === 0) activeLobbies.push("Default-Lobby");
            delete lobbyPlayers[code];
            updateLobbiesUI();
            updatePlayersUI();
            document.getElementById('terminalOutput').innerText += "\\n[" + getTimeString() + "]: Lobby '" + code + "' permanently deleted by Developer!";
        }

        function cancelAllRequests() {
            const container = document.getElementById('minecraftRequestsContainer');
            container.innerHTML = '<div style="font-size:0.75rem; color:var(--text-dim); text-align:center; padding:10px;">All incoming requests cancelled.</div>';
            document.getElementById('terminalOutput').innerText += "\\n[" + getTimeString() + "]: Incoming request queue cleared.";
        }

        function updateLobbiesUI() {
            const listDiv = document.getElementById('activeLobbiesList');
            listDiv.innerHTML = '';
            activeLobbies.forEach(code => {
                const playersInRoom = lobbyPlayers[code] || [];
                const hasDevInLobby = playersInRoom.some(p => p.toLowerCase() === 'jackson22510') && isDevAuthenticated;
                
                const devCardClass = hasDevInLobby ? 'lobby-card lobby-card-dev' : 'lobby-card';
                const devLabel = hasDevInLobby ? '<br><span style="font-size:0.68rem; color:var(--accent-dev); font-weight:bold;">👾 A Dev is in the lobby</span>' : '';
                const deleteBtnHtml = isDevAuthenticated ? '<button class="btn btn-danger" style="width: auto; padding: 2px 6px; margin:0;" onclick="deleteLobby(\\'' + code + '\\')">Delete</button>' : '';

                listDiv.innerHTML += '<div class="' + devCardClass + '"><div><span><b>' + code + '</b></span>' + devLabel + '</div><div style="display: flex; gap: 4px;"><button class="btn" style="width: auto; padding: 2px 6px; margin:0;" onclick="joinLobby(\\'' + code + '\\')">Join</button>' + deleteBtnHtml + '</div></div>';
            });
        }

        function updatePlayersUI() {
            const currentLobby = document.getElementById('activeLobbyBadge').innerText.replace("LOBBY: ", "");
            const container = document.getElementById('playersListContainer');
            const players = lobbyPlayers[currentLobby] || [];

            if (players.length === 0) {
                container.innerHTML = '<div class="player-item"><span style="color:var(--text-dim);">No players in this lobby</span></div>';
                return;
            }

            container.innerHTML = '';
            players.forEach(p => {
                const isDevPlayer = (p.toLowerCase() === 'jackson22510') && isDevAuthenticated;
                if (isDevPlayer) {
                    container.innerHTML += '<div class="player-item player-item-dev"><span>🚀 ' + p + ' (DEV)</span></div>';
                } else {
                    container.innerHTML += '<div class="player-item"><span>🟢 ' + p + '</span></div>';
                }
            });
        }

        function approveRequest(btnElement, accepted) {
            const card = btnElement.closest('.request-card');
            if (accepted) {
                card.innerHTML = '<b style="color:var(--accent-green);">✔ Accepted in MC & Web. Guest Allay deployed!</b>';
            } else {
                card.innerHTML = '<b style="color:var(--accent-danger);">✖ Request Denied.</b>';
            }
        }

        async function sendToAllay() {
            const inputField = document.getElementById('promptInput');
            const outputDiv = document.getElementById('terminalOutput');
            const lobbyBadge = document.getElementById('activeLobbyBadge');
            const gtInput = document.getElementById('gamertagInput');
            const passInput = document.getElementById('devPasswordInput');
            const apiKeyInput = document.getElementById('customApiKey');

            const text = inputField.value.trim();
            const currentLobby = lobbyBadge.innerText.replace("LOBBY: ", "");
            const gamertag = gtInput.value.trim();
            const devPassword = passInput.value.trim();
            const customApiKey = apiKeyInput.value.trim();

            if (!gamertag) {
                alert("Please enter your Minecraft Gamertag before chatting!");
                gtInput.focus();
                return;
            }

            if (!text) return;

            if (!lobbyPlayers[currentLobby]) lobbyPlayers[currentLobby] = [];
            if (!lobbyPlayers[currentLobby].includes(gamertag)) {
                lobbyPlayers[currentLobby].push(gamertag);
                updateLobbiesUI();
                updatePlayersUI();
            }

            if (sessionTokens >= maxTokenQuota) {
                outputDiv.innerText += "\\n[" + getTimeString() + "]: [WARNING]: Token quota exhausted! Please reset.\\n";
                return;
            }

            outputDiv.innerText += "\\n> [" + getTimeString() + "] [" + gamertag + "@" + currentLobby + "] " + text + "\\n[Allay]: Querying Gemini...";
            inputField.value = '';
            outputDiv.scrollTop = outputDiv.scrollHeight;

            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        prompt: text, 
                        lobby_code: currentLobby,
                        custom_api_key: customApiKey,
                        gamertag: gamertag,
                        dev_password: d
