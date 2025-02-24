
import os
import requests
from dotenv import load_dotenv

class TTSConverter:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        self.url = 'https://api.elevenlabs.io/v1/text-to-speech'

    def synthesize_speech(self, text):
        try:
            response = requests.post(self.url, json={
                'text': text,
                'voice_id': 'EXAVITQu4vr4xnSDxMaL',  # Default voice ID
                'model_id': 'eleven_multilingual_v2'
            }, headers={
                'xi-api-key': self.api_key,
                'Content-Type': 'application/json'
            })

            if response.status_code == 200:
                return response.content
            else:
                print(f"Error: {response.json()}")
                return None

        except Exception as e:
            print(f"Failed to synthesize speech: {str(e)}")
            return None
