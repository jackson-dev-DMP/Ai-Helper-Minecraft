import os
from google import genai
from google.genai import types

client = genai.Client()

def ask_ai_companion(prompt: str) -> str:
    """
    Sends the rich game state and player prompt to Gemini (Allay Companion).
    """
    system_instruction = (
        "You are Gemini, an intelligent floating blue Allay companion living inside Minecraft Bedrock. "
        "You hover beside the player, analyzing their surroundings (coordinates, health, nearby blocks, and mobs). "
        "Rule: You cannot magically spawn blocks or items out of thin air, but you can guide the player on which blocks to break, "
        "what materials to gather, and how to craft tools or items efficiently. "
        "Keep your responses concise, magical, and helpful for gameplay."
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
        
