import os
from google import genai
from google.genai import types

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def ask_ai_companion(prompt: str, lobby_code: str = "DEFAULT") -> dict:
    if not api_key:
        return {
            "reply": "Error: GEMINI_API_KEY is not configured on the Render server.",
            "tokens_used": 0
        }

    system_instruction = (
        f"You are Gemini, an intelligent floating blue Allay companion and tactical guide inside Minecraft Bedrock. "
        f"You are currently linked to active lobby code: {lobby_code}. "
        "Speak with a helpful, magical, and supportive tone. Guide the player on crafting recipes and survival strategies."
    )

    try:
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            ),
        )
        
        tokens = 0
        if hasattr(response, 'usage_metadata') and response.usage_metadata:
            tokens = getattr(response.usage_metadata, 'total_token_count', 150)
        else:
            tokens = len(prompt.split()) * 3 + 40

        return {
            "reply": response.text,
            "tokens_used": tokens
        }
    except Exception as e:
        return {
            "reply": f"Neural link error: {str(e)}",
            "tokens_used": 0
        }
        
