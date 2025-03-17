
import os
import requests
from dotenv import load_dotenv

class TTSConverter:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        self.base_url = 'https://api.elevenlabs.io/v1'
        
        # Verify API key and get available voices
        print("Verifying API key and getting voices...")
        voices_url = f'{self.base_url}/voices'
        response = requests.get(voices_url, headers={'xi-api-key': self.api_key})
        if response.status_code != 200:
            print(f"API Key validation failed. Status: {response.status_code}")
            print(f"Response: {response.text}")
            raise Exception("Invalid ElevenLabs API key")
        
        self.voices = {
            'br': "kd1lRcSdRGIfyKxQKjmH",  # Brazilian Portuguese
            'pt': "VR6AewLTigWG4xSOukaG"    # European Portuguese
        }
        print(f"Available voices: BR and PT")

    def synthesize_speech(self, text, variant='br'):
        try:
            print(f"Attempting TTS conversion with text: {text}")
            print(f"Using API key: {self.api_key[:5]}... and variant: {variant}")
            
            headers = {
                'xi-api-key': self.api_key,
                'Content-Type': 'application/json'
            }
            
            voice_id = self.voices.get(variant, self.voices['br'])
            
            payload = {
                'text': text,
                'model_id': 'eleven_multilingual_v2',
                'voice_settings': {
                    'stability': 0.5,
                    'similarity_boost': 0.75,
                    'style': 0.0,
                    'use_speaker_boost': True
                }
            }
            
            print("Sending request to ElevenLabs API...")
            tts_url = f"{self.base_url}/text-to-speech/{voice_id}"
            print(f"Request URL: {tts_url}")
            
            response = requests.post(
                tts_url,
                json=payload,
                headers=headers
            )
            
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {response.headers}")

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
