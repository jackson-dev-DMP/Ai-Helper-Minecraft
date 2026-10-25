import os
from google import genai
from google.genai import types

# Initialize client safely using environment variable
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def ask_ai_companion(prompt: str) -> str:
    """
    Sends the prompt to Gemini 2.5 Flash with Allay companion persona.
    """
    if not api_key:
        return "Error: GEMINI_API_KEY is not configured on the Render server."

    system_instruction = (
        "You are Gemini, an intelligent floating blue Allay companion and tactical guide inside Minecraft Bedrock. "
        "Your UI codename is Ada. Speak with a helpful, magical, and high-tech tone. "
        "Guide the player on crafting recipes, survival mechanics, and building strategies."
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
        return f"Neural link error: {str(e)}"
        
