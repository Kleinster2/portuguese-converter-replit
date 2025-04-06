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
        self.portuguese_tutor_prompt = "You are a helpful and friendly Brazilian Portuguese tutor. Help the user by correcting the spelling, syntax and grammar of any Portuguese text in the user input that needs correction. Offer to help going thru topics in grammar, or to transform written Portuguese into highly concise spoken Portuguese. For the last one, use our rules-based code. Always respond in English, even when the user writes in Portuguese."

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
        Use LLM to transform formal Portuguese text to Brazilian Portuguese concise speech.

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
                    {"role": "system", "content": "You are an expert in Brazilian Portuguese, transforming formal text into concise speech Brazilian Portuguese. Apply common speech patterns, contractions, and informal expressions without changing the meaning."},
                    {"role": "user", "content": text}
                ],
                temperature=0.7
            )

            transformed_text = response.choices[0].message.content
            return transformed_text, "Text transformed to concise Brazilian Portuguese speech successfully"

        except Exception as e:
            logger.error(f"Error in transform_to_colloquial: {str(e)}")
            return text, f"Error: {str(e)}"

    def ask_question(self, question):
        """
        Interactive chat with LLM that detects Portuguese text and converts it if needed,
        but always responds in English

        Args:
            question (str): User's input text/question

        Returns:
            tuple: (response_text, has_portuguese, colloquial_version)
        """
        if not self.client:
            return "Sorry, API key not configured.", False, None

        try:
            # First determine if the text contains Portuguese
            detect_response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a language detection assistant. Your only job is to determine if text contains Portuguese. Respond with 'YES' if the text is in Portuguese (even partially), and 'NO' if it's not."},
                    {"role": "user", "content": question}
                ],
                temperature=0.1
            )

            is_portuguese = "YES" in detect_response.choices[0].message.content.upper()

            # Always respond in English
            if is_portuguese:
                # If Portuguese input, respond in English and still provide the conversion
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": self.portuguese_tutor_prompt},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.7
                )

                # Convert the Portuguese text to colloquial form
                colloquial_text, _ = self.transform_to_colloquial(question)

                return response.choices[0].message.content, True, colloquial_text
            else:
                # If not Portuguese, just respond normally in English
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": self.portuguese_tutor_prompt},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.7
                )

                return response.choices[0].message.content, False, None

        except Exception as e:
            logger.error(f"Error in ask_question: {str(e)}")
            return f"Error: {str(e)}", False, None