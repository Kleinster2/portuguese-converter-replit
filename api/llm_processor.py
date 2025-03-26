
import os
import requests
from dotenv import load_dotenv

class LLMProcessor:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            print("Warning: OPENAI_API_KEY not found in environment")
        
    def correct_text(self, text):
        """
        Use LLM to correct typos, syntax, and grammar in the given text.
        
        Args:
            text (str): The input text to correct
            
        Returns:
            str: Corrected text
        """
        if not self.api_key:
            return text, "API key not configured"
            
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that corrects typos, syntax, and grammar issues in Portuguese text. Keep the overall meaning intact. Return only the corrected text without explanations."},
                    {"role": "user", "content": text}
                ],
                "temperature": 0.2
            }
            
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                corrected_text = response.json()["choices"][0]["message"]["content"]
                return corrected_text, "Text corrected successfully"
            else:
                print(f"API Error: {response.status_code}, {response.text}")
                return text, f"Error: {response.status_code}"
                
        except Exception as e:
            print(f"Error in correct_text: {str(e)}")
            return text, f"Error: {str(e)}"
