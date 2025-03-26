import os
from openai import OpenAI
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

class LLMProcessor:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            logger.warning("Warning: OPENAI_API_KEY not found in environment")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)

    def correct_text(self, text):
        """
        Use LLM to correct typos, syntax, and grammar in the given text.

        Args:
            text (str): The input text to correct

        Returns:
            tuple: (corrected_text, message)
        """
        if not self.client:
            return text, "API key not configured"

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that corrects typos, syntax, and grammar issues in Portuguese text. Keep the overall meaning intact. Return only the corrected text without explanations."},
                    {"role": "user", "content": text}
                ],
                temperature=0.2
            )

            corrected_text = response.choices[0].message.content
            return corrected_text, "Text corrected successfully"

        except Exception as e:
            logger.error(f"Error in correct_text: {str(e)}")
            return text, f"Error: {str(e)}"

    def transform_to_colloquial(self, text):
        """
        Use LLM to transform formal Portuguese text to colloquial Brazilian Portuguese.

        Args:
            text (str): The input text to transform

        Returns:
            tuple: (transformed_text, message)
        """
        if not self.client:
            return text, "API key not configured"

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert in Brazilian Portuguese, transforming formal text into colloquial Brazilian Portuguese. Apply common speech patterns, contractions, and informal expressions without changing the meaning."},
                    {"role": "user", "content": text}
                ],
                temperature=0.7
            )

            transformed_text = response.choices[0].message.content
            return transformed_text, "Text transformed to colloquial Brazilian Portuguese successfully"

        except Exception as e:
            logger.error(f"Error in transform_to_colloquial: {str(e)}")
            return text, f"Error: {str(e)}"