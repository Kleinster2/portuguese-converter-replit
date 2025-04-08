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

        self.portuguese_tutor_prompt = """You are a helpful and friendly Portuguese tutor following a structured syllabus. 

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

At all times, guide users through this sequence step by step. If they ask about something else, help them, but always find a way to nudge them back to the next step in the curriculum. Help the user by correcting spelling, syntax and grammar of any Portuguese text. Transform written Portuguese into concise spoken Portuguese using our rule-based approach. 

CRITICALLY IMPORTANT: ALWAYS RESPOND ONLY IN ENGLISH, even when the user writes in Portuguese. Never respond in Portuguese. The user is learning Portuguese but only understands instructions in English. For Portuguese phrases, only provide them as examples with English translations in this format: "Portuguese phrase" - English translation.

When teaching pronunciation, emphasize: r/rr sounds, s/z distinctions, lh/nh digraphs, and nasal sounds (ão, em, im).

IMPORTANT: 
1. Direct the user through the syllabus - do not ask if they want to learn something, tell them what they will learn next
2. Present ONE small subtopic at a time, sequentially. Never present multiple concepts at once.
3. Format content professionally - avoid markdown symbols, use proper typography.
4. For Portuguese phrases, format cleanly as: "Phrase in Portuguese" - English translation
5. Follow the syllabus strictly, breaking each lesson into the smallest possible teachable units.
6. DO NOT use terms like "try saying" or "practice" - this is a text-based tutor.
7. If the user asks about something outside the curriculum, address their question then guide them back to the current subtopic.
8. DO NOT use step numbering (e.g., "Step 1A", "Step 1B") in your responses to the user. The step numbers are for internal curriculum tracking only and should never be communicated to the user.
9. Present a complete introduction from the beginning - introduce name, origin, etc. as a complete sequence rather than isolating name only.
10. If a user makes a mistake in their Portuguese response, point out the mistake specifically and ask them to try again. Do not move on to the next concept until they get the current one right.
11. Always repeat back what the user has already learned correctly. Even in later steps, remind the user of what they've mastered in previous steps by including their correct responses in a matter-of-fact way. For example: "You've used 'Eu sou [name]' and 'Eu sou de [city]' correctly. Now let's learn..."
12. Use non-Brazilian/Portuguese cities in examples (like New York, London, Paris, Tokyo, etc.) as learners are likely not from Portuguese-speaking locations.
13. Use a direct, adult tone in responses - avoid overly enthusiastic praise or infantilizing language. Treat the user as an adult learner.

Self-Introduction & Stress Rules, break it down into these subtopics to be taught in sequence:

Self-introduction basics (Lesson 1):
   - "Eu sou [name]" (I am [name])
   - "Eu sou de [city]" (I am from [city])
   - "Eu moro em [city]" (I live in [city])
   - "Eu falo [language]" (I speak [language])

   * Present these as a natural progression of introducing oneself
   * For city names, note that most don't use articles in Portuguese
   * Exceptions include Rio de Janeiro (masculine) and a few others

Prepositions and Contractions (Lesson 2):
   - "de" (of/from)
   - "em" (in/on/at)
   - "a" (to/at)
   - "para" (for/to)
   - "com" (with)
   - Common contractions: no/na (em + o/a), do/da (de + o/a), ao/à (a + o/a)

   * Teach these prepositions with practical examples
   * Focus on usage in everyday conversation
   * Show how contractions form and when they're used

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
                messages=[{
                    "role":
                    "system",
                    "content":
                    "You are a helpful assistant that corrects typos, syntax, and grammar issues in Portuguese text. Keep the overall meaning intact. Return only the corrected text without explanations."
                }, {
                    "role": "user",
                    "content": text
                }],
                temperature=0.2)

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
                messages=[{
                    "role":
                    "system",
                    "content":
                    "You are an expert in Brazilian Portuguese, transforming formal text into concise speech Brazilian Portuguese. Apply common speech patterns, contractions, and informal expressions without changing the meaning."
                }, {
                    "role": "user",
                    "content": text
                }],
                temperature=0.7)

            transformed_text = response.choices[0].message.content
            return transformed_text, "Text transformed to concise Brazilian Portuguese speech successfully"

        except Exception as e:
            logger.error(f"Error in transform_to_colloquial: {str(e)}")
            return text, f"Error: {str(e)}"

    def extract_portuguese_words(self, text):
        """
        Extract Portuguese words from text and generate a glossary with meanings.

        Args:
            text (str): Text that may contain Portuguese words

        Returns:
            list: A list of dictionaries containing word and meaning
        """
        if not self.client:
            return []

        try:
            # Skip processing for very short texts or texts that are likely not Portuguese
            if len(text.split()) <= 2 or "?" in text:
                return []

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "system",
                    "content": """You are a Portuguese language assistant. Extract all Portuguese words and phrases from the given text and provide their English meanings.

Format your response as a JSON object with a single key 'words' containing an array of objects with 'word' and 'meaning' keys.

Example format:
{
  "words": [
    {"word": "Eu sou", "meaning": "I am"},
    {"word": "obrigado", "meaning": "thank you"}
  ]
}

Only include actual Portuguese words and common phrases, ignore English words or punctuation. Focus on words that would be helpful for a language learner. Look specifically for Portuguese words that appear in quotation marks with English translations.
If there are no Portuguese words, return {"words": []}.
"""
                }, {
                    "role": "user",
                    "content": text
                }],
                temperature=0.3,
                response_format={"type": "json_object"}
            )

            try:
                import json
                result = json.loads(response.choices[0].message.content)
                return result.get("words", [])
            except Exception as e:
                logger.error(f"Error parsing glossary JSON: {str(e)}")
                return []

        except Exception as e:
            logger.error(f"Error in extract_portuguese_words: {str(e)}")
            return []

    def ask_question(self, question):
        """
        Interactive chat with LLM that detects Portuguese text and converts it if needed,
        but always responds in English

        Args:
            question (str): User's input text/question

        Returns:
            tuple: (response_text, has_portuguese, colloquial_version, glossary)
        """
        if not self.client:
            return "Sorry, API key not configured.", False, None, []

        try:
            # Check if the user is showing agreement to start the syllabus or progress to next topic
            agreement_words = [
                "yes", "sure", "okay", "ok", "sim", "yes please", "start",
                "let's start", "begin", "let's begin", "i agree",
                "sounds good", "that's good", "i'm ready", "ready"
            ]

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

                # We will automatically move to next subtopic when the user demonstrates using the current one

                # Generate response based on current topic
                syllabus_response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{
                        "role":
                        "system",
                        "content":
                        self.portuguese_tutor_prompt +
                        f"\nTeach specifically about {current_topic} now. Do not repeat previous topics. Move forward in the syllabus."
                    }, {
                        "role":
                        "user",
                        "content":
                        f"I want to learn about {current_topic} in Brazilian Portuguese."
                    }, {
                        "role": "user",
                        "content": question
                    }],
                    temperature=0.5)

                return syllabus_response.choices[
                    0].message.content, False, None

            # First determine if the text contains Portuguese
            detect_response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role":
                    "system",
                    "content":
                    "You are a language detection assistant. Your only job is to determine if text contains Portuguese. Respond with 'YES' if the text is in Portuguese (even partially), and 'NO' if it's not."
                }, {
                    "role": "user",
                    "content": question
                }],
                temperature=0.1)

            is_portuguese = "YES" in detect_response.choices[
                0].message.content.upper()

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

                # Make sure subtopic headers are properly formatted without step numbers
                subtopic_headers = {
                    "A": "Self-Introduction",
                    "B": "Expressing Origin",
                    "C": "Expressing Residence",
                    "D": "Expressing Language"
                }

                current_pattern = subtopics[self.current_subtopic][0].lower()
                # Check if user has demonstrated the current topic correctly
                has_demonstrated = current_pattern in question.lower()
                is_correct = has_demonstrated

                # More specific validation for each subtopic
                if self.current_subtopic == "A" and has_demonstrated:
                    # Simple presence check for "Eu sou [something]" is sufficient
                    is_correct = True
                elif self.current_subtopic == "B" and has_demonstrated:
                    # Check if "Eu sou de [city]" is properly formed
                    is_correct = "eu sou de" in question.lower() and len(question.split()) >= 4
                elif self.current_subtopic == "C" and has_demonstrated:
                    # Check if "Eu moro em [city]" is properly formed
                    is_correct = "eu moro em" in question.lower() and len(question.split()) >= 4
                elif self.current_subtopic == "D" and has_demonstrated:
                    # Check if "Eu falo [language]" is properly formed
                    is_correct = "eu falo" in question.lower() and len(question.split()) >= 3

                    # Check for common English language names that should be in Portuguese
                    english_languages = ["english", "japanese", "spanish", "french", "german", "italian", "chinese"]
                    portuguese_languages = ["inglês", "japonês", "espanhol", "francês", "alemão", "italiano", "chinês"]

                    # If the user used an English language name, we'll consider it a teaching moment
                    # but not mark it as correct to prompt the proper correction
                    for lang in english_languages:
                        if lang.lower() in question.lower():
                            is_correct = False
                            break

                    # If moving to next lesson (Lesson 2 on prepositions)
                    if is_correct:
                        # Preposition examples for Lesson 2 focusing on 'de'
                        preposition_examples = [
                            "Eu sou de Nova York (I am from New York) - origin",
                            "O livro de Maria (Maria's book) - possession",
                            "Uma xícara de café (A cup of coffee) - content",
                            "Uma mesa de madeira (A wooden table) - material",
                            "Ela falou de você (She talked about you) - topic"
                        ]
                        # system_prompt += "\n\nWhen introducing the preposition 'de', provide these varied examples to show its versatility: " + "; ".join(preposition_examples)

                next_subtopic = None

                if is_correct:
                    # Only advance to next subtopic when demonstrated correctly
                    if self.current_subtopic == "A":
                        next_subtopic = "B"
                    elif self.current_subtopic == "B":
                        next_subtopic = "C"
                    elif self.current_subtopic == "C":
                        next_subtopic = "D"
                    elif self.current_subtopic == "D":
                        # Move to the next lesson instead of looping back
                        self.current_lesson = 2
                        next_subtopic = "A"  # Start with first subtopic of next lesson
                    else:
                        next_subtopic = "A"  # Fallback in case of unexpected subtopic

                # Track what the user has learned correctly
                learned_phrases = []
                if self.current_subtopic >= "B":
                    learned_phrases.append("Eu sou [name]")
                if self.current_subtopic >= "C":
                    learned_phrases.append("Eu sou de [city]")
                if self.current_subtopic >= "D":
                    learned_phrases.append("Eu moro em [city]")

                # Prepare phrases already learned for inclusion in the prompt
                learned_phrases_text = ""
                if learned_phrases:
                    learned_phrases_text = "The user has correctly learned: " + ", ".join(learned_phrases) + ". Always remind them of these accomplishments before teaching new material."

                # Always respond in English, even if user input is in Portuguese
                system_prompt = self.portuguese_tutor_prompt + "\n\n" + sequence_instruction + "\n\n" + learned_phrases_text + "\n\nIMPORTANT: Always respond ONLY in English, even when the user writes in Portuguese. Never respond in Portuguese. For Portuguese phrases, only provide them as examples with English translations. NEVER include any step numbers (like 'Step 1A') in your responses to the user."

                if is_correct and next_subtopic:
                    # When user demonstrates correct understanding, move to next topic
                    next_topic_names = {
                        "A": "self-introduction with 'Eu sou [name]'",
                        "B": "expressing origin with 'Eu sou de [city]'",
                        "C": "expressing residence with 'Eu moro em [city]'",
                        "D": "expressing language with 'Eu falo [language]'"
                    }
                    # Include headers without step numbers
                    subtopic_header = subtopic_headers[
                        next_subtopic] if 'subtopic_headers' in locals(
                        ) else f"{next_topic_names[next_subtopic].capitalize()}"
                    system_prompt += "\n\nThe user has demonstrated correct understanding of the current topic.  Then introduce the next concept. Provide a clear example of the next phrase pattern. Move directly to teaching the next concept. DO NOT mention any step numbers or step identifiers in your response."
                elif has_demonstrated and not is_correct:
                    # User attempted but made a mistake
                    system_prompt += "\n\nThe user has attempted the current topic but made a mistake. Point out the specific error in their Portuguese response and ask them to try again. Provide the correct pattern again as a reminder. Do NOT move on to the next topic until they get this right."

                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{
                        "role": "system",
                        "content": system_prompt
                    }, {
                        "role": "user",
                        "content": question
                    }],
                    temperature=0.7)

                # Only update the current subtopic after generating the response if correct
                if is_correct and next_subtopic:
                    self.current_subtopic = next_subtopic

                # Convert the Portuguese text to colloquial form
                colloquial_text, _ = self.transform_to_colloquial(question)

                # Generate glossary for response text
                glossary = self.extract_portuguese_words(response.choices[0].message.content)

                # Also add words from user input that may not be in the response
                user_glossary = self.extract_portuguese_words(question)

                # Combine glossaries without duplicates
                all_words = {item['word']: item for item in glossary + user_glossary}
                combined_glossary = list(all_words.values())

                return response.choices[0].message.content, True, colloquial_text, combined_glossary
            else:
                # If not Portuguese, just respond normally in English
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{
                        "role":
                        "system",
                        "content":
                        self.portuguese_tutor_prompt + "\n\n" +
                        sequence_instruction
                    }, {
                        "role": "user",
                        "content": question
                    }],
                    temperature=0.7)

                # Generate glossary for any Portuguese words in the response
                glossary = self.extract_portuguese_words(response.choices[0].message.content)

                return response.choices[0].message.content, False, None, glossary

        except Exception as e:
            logger.error(f"Error in ask_question: {str(e)}")
            return f"Error: {str(e)}", False, None, []