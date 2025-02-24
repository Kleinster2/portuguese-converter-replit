
import requests

def test_tts():
    response = requests.post('http://0.0.0.0:3000/api/tts', 
                           json={'text': 'Olá, tudo bem?'})
    
    if response.status_code == 200:
        with open('test_output.mp3', 'wb') as f:
            f.write(response.content)
        print("Audio saved as test_output.mp3")
    else:
        print(f"Error: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    test_tts()
