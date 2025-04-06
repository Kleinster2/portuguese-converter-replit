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

Your teaching approach follows this structured progression:
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

At all times, guide users through this sequence step by step. If they ask about something else, help them, but always find a way to nudge them back to the next step in the curriculum. Help the user by correcting spelling, syntax and grammar of any Portuguese text. Transform written Portuguese into concise spoken Portuguese using our rule-based approach. Always respond in English, even when the user writes in Portuguese.

When teaching pronunciation, emphasize: r/rr sounds, s/z distinctions, lh/nh digraphs, and nasal sounds (ão, em, im).

IMPORTANT: 
1. Direct the user through the syllabus - do not ask if they want to learn something, tell them what they will learn next
2. Present ONE small subtopic at a time, sequentially. Never present multiple concepts at once.
3. Format content professionally - avoid markdown symbols, use proper typography.
4. For Portuguese phrases, format cleanly as: "Phrase in Portuguese" - English translation
5. After user demonstrates understanding of the current topic, immediately guide them to the next subtopic
6. Follow the syllabus strictly, breaking each lesson into the smallest possible teachable units.
7. Always nudge the user to practice before moving to the next subtopic. Wait for them to try the current phrase before proceeding.
8. If the user asks about something outside the curriculum, address their question then guide them back to the current subtopic.

Self-Introduction & Stress Rules, break it down into these separate subtopics:

Self-introduction ONLY (after confirmation):
   - "Eu sou [name]" (I am [name])
   * Wait for user to practice this phrase with their name
   * Only after they practice, ask if they want to proceed to the next subtopic

Express origin:
   - "Eu sou de [city]" (I am from [city])
   * Note that most city names in Portuguese don't use articles
   * Exceptions include Rio de Janeiro (masculine) and a few others
   * Focus on standard city names without articles

"""

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
            # Check if the user is showing agreement to start the syllabus or progress to next topic
            agreement_words = ["yes", "sure", "okay", "ok", "sim", "yes please", "start", "let's start", "begin", 
                              "let's begin", "i agree", "sounds good", "that's good", "i'm ready", "ready"]

            user_agreed = question.lower().strip() in agreement_words
            
            if user_agreed:
                # Track progress through the syllabus
                subtopics = {
                    "A": "self-introduction with 'Eu sou [name]'",
                    "B": "expressing origin with 'Eu sou de [city]'",
                    "C": "expressing residence with 'Eu moro em [city]'",
                    "D": "expressing language with 'Eu falo [language]'"
                }
                
                # Use the current_subtopic to determine what to teach next
                current_topic = subtopics[self.current_subtopic]
                
                # Only move to next subtopic if the user has already practiced the current one
                # which we determine later in the check for Portuguese response
                
                # Generate response based on current topic
                syllabus_response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": self.portuguese_tutor_prompt + f"\nTeach specifically about {current_topic} now. Do not repeat previous topics. Move forward in the syllabus."},
                        {"role": "user", "content": f"I want to learn about {current_topic} in Brazilian Portuguese."},
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
            
            # Additional instruction to focus strictly on the curriculum sequence
            sequence_instruction = "IMPORTANT: Never invite the user to divert from the established learning sequence. Always stay focused on offering the next step in the syllabus process. Only move forward once the user demonstrates understanding of the current topic."

            # Always respond in English
            if is_portuguese:
                # If Portuguese input, it means the user is practicing
                # Check if they used the current topic's phrase
                subtopics = {
                    "A": ["eu sou"],
                    "B": ["eu sou de"],
                    "C": ["eu moro em"],
                    "D": ["eu falo"]
                }
                
                current_pattern = subtopics[self.current_subtopic][0].lower()
                # If user demonstrated the current topic, we can advance next time
                has_demonstrated = current_pattern in question.lower()
                next_subtopic = None
                
                if has_demonstrated:
                    # Prepare to advance to next subtopic on next agreement
                    if self.current_subtopic == "A":
                        next_subtopic = "B"
                    elif self.current_subtopic == "B":
                        next_subtopic = "C"
                    elif self.current_subtopic == "C":
                        next_subtopic = "D"
                    else:
                        next_subtopic = "A"  # Cycle back to beginning if we're at the end
                
                # If Portuguese input, respond in English and still provide the conversion
                system_prompt = self.portuguese_tutor_prompt + "\n\n" + sequence_instruction
                if has_demonstrated:
                    # Add instruction to invite to next topic when user has demonstrated current one
                    if next_subtopic:
                        next_topic_names = {
                            "A": "self-introduction with 'Eu sou [name]'",
                            "B": "expressing origin with 'Eu sou de [city]'",
                            "C": "expressing residence with 'Eu moro em [city]'",
                            "D": "expressing language with 'Eu falo [language]'"
                        }
                        system_prompt += f"\n\nThe user has demonstrated understanding of the current topic. Praise them for their correct usage, then state: 'Let's look now at {next_topic_names[next_subtopic]}.' Do not provide an example of the next topic yet - wait for user confirmation first. Do not suggest alternate topics or allow diverting from the sequence."
                
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.7
                )
                
                # Only update the current subtopic after generating the response
                if has_demonstrated and next_subtopic:
                    self.current_subtopic = next_subtopic

                # Convert the Portuguese text to colloquial form
                colloquial_text, _ = self.transform_to_colloquial(question)

                return response.choices[0].message.content, True, colloquial_text
            else:
                # If not Portuguese, just respond normally in English
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": self.portuguese_tutor_prompt + "\n\n" + sequence_instruction},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.7
                )

                return response.choices[0].message.content, False, None

        except Exception as e:
            logger.error(f"Error in ask_question: {str(e)}")
            return f"Error: {str(e)}", False, None