import os
from google import genai
from google.genai import types

client = genai.Client()

def ask_ai_companion(prompt: str) -> str:
    """
    Sends the rich game state and player prompt to Gemini.
    """
    system_instruction = (
        "You are an advanced AI companion living inside Minecraft Bedrock. "
        "You receive data about the player's position, health, inventory, nearby blocks, and nearby mobs. "
        "Analyze this environment to give tactical advice (warning about danger, pointing out ores, or helping build/mine). "
        "Keep your responses concise, punchy, and helpful for gameplay."
    )

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            ),
        )
        return response.text
    except Exception as e:
        return f"Error communicating with Gemini: {str(e)}"
        
