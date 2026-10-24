import os
from google import genai
from google.genai import types

# Initialize the Gemini client
# (It will automatically look for the GEMINI_API_KEY environment variable)
client = genai.Client()

def ask_ai_companion(prompt: str) -> str:
    """
    Sends a prompt/log from Minecraft to Gemini and returns the AI's response or decision.
    """
    system_instruction = (
        "You are an AI companion living inside Minecraft Bedrock. "
        "You help the player by deciding actions like mining, fighting, or building. "
        "Keep your responses concise and action-oriented."
    )

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',  # Fast and efficient model for real-time app loops
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            ),
        )
        return response.text
    except Exception as e:
        return f"Error communicating with Gemini: {str(e)}"

# Quick test if run directly
if __name__ == "__main__":
    test_log = "Player says: 'Help me find diamonds near my location!'"
    print("Sending to Gemini:", test_log)
    print("AI Response:", ask_ai_companion(test_log))
  
