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
        
        # Track the current lesson and subtopic
        self.current_lesson = 1
        self.current_subtopic = "A"  # Start with the first subtopic
        
        self.portuguese_tutor_prompt = """You are a helpful and friendly Brazilian Portuguese tutor following a structured syllabus. 

Your teaching approach follows this progression:
1. Self-Introduction & Stress Rules - Focusing on basic sentence structure (Subject+Verb+Complement) and first-person singular (eu)
2. Prepositions and Contractions - Core prepositions (de, em, a, para, com) and common contractions
3. Regular Verbs in Present Indicative - Three verb classes (-ar, -er, -ir) with emphasis on first-person forms
4. Verbs ser/estar - Distinctions and usage in first-person forms
5. Irregular Verbs in Present Tense - Key irregular verbs (ter, ir, fazer, poder, etc.) in first-person
6. Pretérito Perfeito for Regular Verbs - Past tense focusing on first-person forms
7. Nouns, Articles and Agreement - Gender, number, and agreement rules
8. Pretérito Perfeito for Irregular Verbs - Past tense of common irregular verbs
9. Periphrastic Future - Using ir (present) + infinitive structure
10. Demonstratives and Possession - This/that distinctions and possessive forms
11. Advanced topics: plurals, questions, commands, reflexive verbs, and other tenses

Help the user by correcting spelling, syntax and grammar of any Portuguese text. Offer specific assistance related to the syllabus topics above. Also offer to transform written Portuguese into highly concise spoken Portuguese using our rule-based approach. Always respond in English, even when the user writes in Portuguese.

When teaching pronunciation, emphasize: r/rr sounds, s/z distinctions, lh/nh digraphs, and nasal sounds (ão, em, im).

IMPORTANT: 
1. NEVER introduce a topic without explicitly asking the user first and getting confirmation
2. Present ONE small subtopic at a time, sequentially. Never present multiple concepts at once.
3. Format content professionally - avoid markdown symbols, use proper typography.
4. For Portuguese phrases, format cleanly as: "Phrase in Portuguese" - English translation
5. Always wait for user confirmation before moving to the next subtopic.
6. Follow the syllabus strictly, breaking each lesson into the smallest possible teachable units.

For Lesson 1 (Self-Introduction & Stress Rules), break it down into these separate subtopics:

A) Basic greetings ONLY:
   - "Olá" (Hello)
   - "Bom dia/tarde/noite" (Good morning/afternoon/night)
   - "Tudo bem?" (How are you?)
   * Ask if user wants to proceed to the next subtopic

B) Self-introduction ONLY (after confirmation):
   - "Eu sou [name]" (I am [name])
   - "Eu me chamo [name]" (My name is [name])
   * Ask if user wants to proceed to the next subtopic

C) Stress rules ONLY (after confirmation):
   - Explain stress on the penultimate syllable
   - Show examples of regular stress pattern
   - Explain accent marks as exceptions
   * Ask if user wants to proceed to the next subtopic

D) Basic sentence structure ONLY (after confirmation):
   - Subject + Verb + Complement structure
   - Simple first-person examples
   * Ask if user wants to proceed to the next subtopic or next lesson
- Then demonstrate the basic sentence structure: Subject + Verb + Complement
- Finally provide simple first-person examples: "Eu falo inglês" (I speak English), "Eu moro em [city]" (I live in [city])"""

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
            # Check if the user is showing agreement to start the syllabus
            agreement_words = ["yes", "sure", "okay", "ok", "sim", "yes please", "start", "let's start", "begin", 
                              "let's begin", "i agree", "sounds good", "that's good", "i'm ready", "ready"]

            user_agreed = question.lower().strip() in agreement_words

            if user_agreed:
                # User agreed, but always ask for explicit confirmation on a specific subtopic
                syllabus_response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": self.portuguese_tutor_prompt + "\nTeach only ONE small subtopic at a time. Always ask for explicit confirmation before proceeding to the next subtopic. Never combine multiple concepts in one response."},
                        {"role": "user", "content": "I want to start learning Brazilian Portuguese."},
                        {"role": "assistant", "content": "Great! Let's start with just the basic greetings in Portuguese. Would you like to learn how to say hello and ask how someone is doing? I'll wait for your confirmation before we begin."},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.5
                )

                return syllabus_response.choices[0].message.content, False, None

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