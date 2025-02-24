
import os
import requests
from dotenv import load_dotenv

class TTSConverter:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        self.url = 'https://api.elevenlabs.io/v1/text-to-speech'
        
        # Verify API key
        voices_url = 'https://api.elevenlabs.io/v1/voices'
        response = requests.get(voices_url, headers={'xi-api-key': self.api_key})
        if response.status_code != 200:
            print(f"API Key validation failed. Status: {response.status_code}")
            print(f"Response: {response.text}")
            raise Exception("Invalid ElevenLabs API key")

    def synthesize_speech(self, text):
        try:
            headers = {
                'xi-api-key': self.api_key,
                'Content-Type': 'application/json'
            }
            
            payload = {
                'text': text,
                'voice_id': '21m00Tcm4TlvDq8ikWAM',  # Default voice ID
                'model_id': 'eleven_multilingual_v1'
            }
            
            response = requests.post(self.url, json=payload, headers=headers)

            if response.status_code == 200:
                return response.content
            else:
                error_details = response.json()
                print(f"ElevenLabs API Error: Status {response.status_code}")
                print(f"Error details: {error_details}")
                print(f"Request URL: {self.url}")
                print(f"Headers: {response.request.headers}")
                print(f"Request body: {response.request.body}")
                return None

        except Exception as e:
            print(f"Failed to synthesize speech: {str(e)}")
            return None
