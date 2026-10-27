import os
import base64
import time
import jwt
import requests
from fastapi import FastAPI, Request
from google import genai

app = FastAPI()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
APP_ID = os.environ.get("GITHUB_APP_ID")
PRIVATE_KEY = os.environ.get("GITHUB_PRIVATE_KEY")
REPO = "jackson-dev-DMP/Ai-Helper-Minecraft"

def get_installation_token():
    # Generate JWT for the GitHub App
    payload = {
        "iat": int(time.time()),
        "exp": int(time.time()) + 600,
        "iss": APP_ID
    }
    encoded_jwt = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
    
    headers = {
        "Authorization": f"Bearer {encoded_jwt}",
        "Accept": "application/vnd.github+json"
    }
    
    # Get installation ID
    inst_resp = requests.get(f"https://api.github.com/repos/{REPO}/installation", headers=headers)
    if inst_resp.status_code != 200:
        return None
    installation_id = inst_resp.json()["id"]
    
    # Get access token
    token_resp = requests.post(f"https://api.github.com/app/installations/{installation_id}/access_tokens", headers=headers)
    if token_resp.status_code == 201:
        return token_resp.json()["token"]
    return None

@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    if "comment" in payload and "body" in payload["comment"]:
        comment_body = payload["comment"]["body"].strip()
        if comment_body.startswith("@gemini"):
            user_prompt = comment_body.replace("@gemini", "").strip()
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"Write or modify the code based on this request: {user_prompt}. Return only clean code."
            )
            
            token = get_installation_token()
            if token:
                update_github_file("backend/main.py", response.text, f"Gemini update: {user_prompt}", token)

    return {"status": "ok"}

def update_github_file(file_path, new_content, commit_message, token):
    url = f"https://api.github.com/repos/{REPO}/contents/{file_path}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    
    resp = requests.get(url, headers=headers)
    sha = resp.json().get("sha") if resp.status_code == 200 else None
    
    payload = {
        "message": commit_message,
        "content": base64.b64encode(new_content.encode("utf-8")).decode("utf-8"),
        "branch": "main"
    }
    if sha:
        payload["sha"] = sha
        
    requests.put(url, headers=headers, json=payload)
