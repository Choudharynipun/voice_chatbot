import requests
import os
from dotenv import load_dotenv

load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def synthesize_speech(text: str, output_path: str = "response.wav"):
    
    print("Starting Text-to-Speech process.")
    print(f"Input text: {text}")

    if not ELEVENLABS_API_KEY:
        print("Error: ElevenLabs API key not found in .env file.")
        return None

    # API endpoint and headers setup
    url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL"  # Default voice ID
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    # Creating payload with text and voice settings
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    try:
        # Sending POST request to ElevenLabs API
        response = requests.post(url, json=payload, headers=headers)

        # Check if request was successful
        if response.status_code == 200:
            print("TTS audio generation successful.")
            
            # Write audio data to file
            with open(output_path, "wb") as f:
                f.write(response.content)
            
            print(f"Audio has been saved to file: {output_path}")
            return output_path
        else:
            print("TTS API call failed.")
            print(f"Status Code: {response.status_code}")
            print("Response:", response.text)
            return None

    except Exception as e:
        print("An error occurred during TTS generation.")
        print("Error:", e)
        return None
