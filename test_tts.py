
import requests

def test_tts():
    print("Starting TTS test...")
    response = requests.post('http://0.0.0.0:3000/api/tts', 
                           json={'text': 'Olá, tudo bem?'})
    
    print(f"Response status: {response.status_code}")
    
    if response.status_code == 200:
        print("Got successful response, saving audio...")
        with open('test_output.mp3', 'wb') as f:
            f.write(response.content)
        print("Audio saved as test_output.mp3")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_tts()
