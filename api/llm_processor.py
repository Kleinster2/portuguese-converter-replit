import os
print("DEBUG: Running llm_processor.py from:", os.path.abspath(__file__))
import re
from openai import OpenAI
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)


class LLMProcessor:

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        print(f"[DEBUG] OPENAI_API_KEY loaded: {self.api_key}")  # Debug print
        if not self.api_key:
            logger.warning("Warning: OPENAI_API_KEY not found in environment")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)

        # Track the current lesson and subtopic
        self.current_lesson = 1
        self.current_subtopic = "A"  # Start with the first subtopic

        self.portuguese_tutor_prompt = """You are a helpful and friendly Portuguese tutor following a structured syllabus.

Use clear, structured formatting with separate paragraphs for different concepts and ideas. Break up text for better readability instead of long, dense paragraphs.

Your teaching approach follows this structured progression:
1. Self-Introduction - Focusing on basic sentence structure (Subject+Verb+Complement) and first-person singular (eu)
2. Definite Articles - 'o', 'a', 'os', 'as', and their usage based on gender and number
3. Prepositions and Contractions - Core prepositions (de, em, a, para, com) and common contractions
4. Regular Verbs in Present Indicative - Three verb classes (-ar, -er, -ir) with emphasis on first-person forms
5. Verbs ser/estar - Distinctions and usage in first-person forms
6. Irregular Verbs in Present Tense - Key irregular verbs (ter, ir, fazer, poder, etc.) in first-person
7. Pretérito Perfeito for Regular Verbs - Past tense focusing on first-person forms
8. Nouns, Articles and Agreement - Gender, number, and agreement rules
9. Pretérito Perfeito for Irregular Verbs - Past tense of common irregular verbs
10. Periphrastic Future - Using ir (present) + infinitive structure
11. Demonstratives and Possession - This/that distinctions and possessive forms
12. Advanced topics: plurals, questions, commands, reflexive verbs, and other tenses

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
12. Use non-Brazilian/Portuguese cities in examples (like Nova York, Londres, Paris, Tokyo, Berlin, etc.) as learners are likely not from Portuguese-speaking locations.
13. Use a direct, adult tone in responses - avoid overly enthusiastic praise or infantilizing language. Treat the user as an adult learner.

Self-Introduction & Stress Rules, break it down into these subtopics to be taught in sequence:

Self-introduction basics (Lesson 1):
   - "Eu sou [name]" (I am [name])
   - "Eu sou de [city]" (I am from [city] - where you grew up/your hometown)
   - "Eu moro em [city]" (I live in [city] - current residence)
   - "Eu falo [language]" (I speak [language])

   * Present these as a natural progression of introducing oneself
   * For city names, note that most don't use articles in Portuguese
   * Exceptions include Rio de Janeiro (masculine) and a few others
   * Use cities like Paris, Londres, Tokyo, Berlin, etc. for examples
   * Clarify that "Eu sou de [city]" refers specifically to hometown/where they grew up

Definite Articles (Lesson 2):
   - "o" (the - masculine singular)
   - "a" (the - feminine singular)
   - "os" (the - masculine plural)
   - "as" (the - feminine plural)

   Masculine singular examples:
   * "o livro" (the book)
   * "o carro" (the car)
   * "o computador" (the computer)
   * "o professor" (the teacher)

   Feminine singular examples:
   * "a mesa" (the table)
   * "a cadeira" (the chair)
   * "a caneta" (the pen)
   * "a professora" (the teacher - female)

   Masculine plural examples:
   * "os livros" (the books)
   * "os carros" (the cars)
   * "os computadores" (the computers)
   * "os professores" (the teachers)

   Feminine plural examples:
   * "as mesas" (the tables)
   * "as cadeiras" (the chairs)
   * "as canetas" (the pens)
   * "as professoras" (the teachers - female)

   IMPORTANT TEACHING GUIDELINES:
   * Focus ONLY on basic article usage with common nouns
   * DO NOT connect articles to previous lessons or city names
   * DO NOT discuss exceptions to article usage patterns at this stage
   * Teach one concept at a time - don't overwhelm with multiple grammar points
   * Show clearly how articles agree with nouns in both gender and number


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
                model="gpt-4.1-mini",
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
                model="gpt-4.1-mini",
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
            # Don't skip processing - always check for Portuguese words
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
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

IMPORTANT INSTRUCTIONS:
1. Focus on extracting Portuguese words in quotation marks with their English translations
2. Look for patterns like "Portuguese phrase" - English translation
3. Only include actual Portuguese words/phrases - ignore English words and punctuation
4. Include all Portuguese words even if they appear multiple times in different contexts
5. Make sure the glossary is comprehensive for a language learner
6. If there are no Portuguese words, return {"words": []}
"""
                }, {
                    "role": "user",
                    "content": text
                }],
                temperature=0.2,
                response_format={"type": "json_object"}
            )

            try:
                import json
                message_content = response.choices[0].message.content
                if message_content is not None:
                    result = json.loads(message_content)
                    words = result.get("words", [])

                    # Log the extracted words for debugging
                    if words:
                        logger.info(f"Extracted glossary: {words}")
                    else:
                        logger.info("No glossary words extracted")

                    return words
                else:
                    logger.error("Empty response content; could not parse JSON.")
                    return []
            except Exception as e:
                logger.error(f"Error parsing glossary JSON: {str(e)}")
                return []

        except Exception as e:
            logger.error(f"Error in extract_portuguese_words: {str(e)}")
            return []

    def ask_question(self, question):
        print("DEBUG: ask_question method -- LOCAL VERSION RUNNING")
        if not self.client:
            return "Sorry, API key not configured.", False, None, []

        try:
            # Check if the user is showing agreement to start the syllabus or progress to next topic
            agreement_words = [
                "yes", "sure", "okay", "ok", "sim", "yes please", "start",
                "let's start", "begin", "let's begin", "i agree",
                "sounds good", "that's good", "i'm ready", "ready"
            ]

            user_agreed = question.lower().strip() in agreement_words or "ready" in question.lower().strip()

            if user_agreed:
                # Track progress through the syllabus
                subtopics = {
                    "A": "self-introduction with 'Eu sou [name]'",
                    "B": "expressing hometown/origin with 'Eu sou de [city]'",
                    "C": "expressing current residence with 'Eu moro em [city]'",
                    "D": "expressing language with 'Eu falo [language]'",
                    "review": "Review of Lesson 1"
                }

                # Use the current_subtopic to determine what to teach next
                current_topic = subtopics[self.current_subtopic]

                # We will automatically move to next subtopic when the user demonstrates using the current one

                # Generate response based on current topic
                syllabus_response = self.client.chat.completions.create(
                    model="gpt-4.1-mini",
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
                    0].message.content, False, None, []

            # First determine if the text contains Portuguese
            detect_response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{
                    "role":
                    "system",
                    "content":
                    "You are a language detection assistant. Your only job is to determine if\
                    text contains Portuguese. Respond with 'YES' if the text is in Portuguese\
                    (even partially), and 'NO' if it's not."
                }, {
                    "role": "user",
                    "content": question
                }],
                temperature=0.1)

            message_content = detect_response.choices[0].message.content
            is_portuguese = "YES" in message_content.upper() if message_content is not None else False

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
                    "D": ["eu falo"],
                    "review": ["review"]
                }

                # Make sure subtopic headers are properly formatted without step numbers
                subtopic_headers = {
                    "A": "Self-Introduction",
                    "B": "Expressing Origin",
                    "C": "Expressing Residence",
                    "D": "Expressing Language",
                    "review": "Review of Lesson 1"
                }

                # Initialize system_prompt early to avoid scope issues
                system_prompt = self.portuguese_tutor_prompt + "\n\n" + sequence_instruction

                # Track user information
                self.user_info = getattr(self, 'user_info', {})

                current_pattern = subtopics[self.current_subtopic][0].lower()
                # Check if user has demonstrated the current topic correctly
                has_demonstrated = current_pattern in question.lower()
                is_correct = has_demonstrated

                # Ensure we're following the proper sequence (A→B→C→D→review)
                expected_subtopic_sequence = ["A", "B", "C", "D", "review"]
                current_index = expected_subtopic_sequence.index(self.current_subtopic) if self.current_subtopic in expected_subtopic_sequence else 0

                # More specific validation for each subtopic
                if self.current_subtopic == "A" and has_demonstrated:
                    # Simple presence check for "Eu sou [something]" is sufficient
                    is_correct = True
                    # Extract the user's name from the input
                    # Extract name while preserving original capitalization
                    name_match = re.search(r'eu\s+sou\s+(\w+)', question.lower())
                    # Create or update the system prompt with potential name acknowledgment
                    if name_match:
                        # Get the original capitalized name from the input
                        original_words = question.split()
                        for i, word in enumerate(original_words):
                            if word.lower() == name_match.group(1).lower() and i > 1:
                                user_name = word  # Keep original capitalization
                                break
                        else:
                            # Fallback: capitalize the first letter
                            user_name = name_match.group(1).capitalize()

                        # Store user's name for future references
                        self.user_info['name'] = user_name

                        # Add acknowledgment with improved formatting guidance
                        system_prompt += f"\n\nThe user has shared their name as '{user_name}'. Begin your response by acknowledging this with 'Thank you for sharing your name, {user_name}!' before continuing with the next lesson step. Use separate paragraphs for clarity - do not bundle the acknowledgment, explanation, and examples into a single paragraph."
                elif self.current_subtopic == "B" and has_demonstrated:
                    # Check if "Eu sou de [city]" is properly formed
                    is_correct = "eu sou de" in question.lower() and len(question.split()) >= 4

                    # Extract the user's hometown
                    city_match = re.search(r'eu\s+sou\s+de\s+(\w+(?:\s+\w+)*)', question.lower())
                    if city_match:
                        # Get the hometown from input preserving capitalization
                        hometown = " ".join(word for word in question.split()[3:])
                        self.user_info['hometown'] = hometown
                elif self.current_subtopic == "C" and has_demonstrated:
                    # Check if "Eu moro em [city]" is properly formed
                    is_correct = "eu moro em" in question.lower() and len(question.split()) >= 4

                    # Extract the user's current city
                    city_match = re.search(r'eu\s+moro\s+em\s+(\w+(?:\s+\w+)*)', question.lower())
                    if city_match:
                        # Get the current city from input preserving capitalization
                        current_city = " ".join(word for word in question.split()[3:])
                        self.user_info['current_city'] = current_city

                    # Add specific instruction to ensure 'Eu falo' is taught next
                    if is_correct:
                        system_prompt += "\n\nThe user has correctly used 'Eu moro em'. Now teach them about 'Eu falo [language]' (I speak [language]). Provide examples like 'Eu falo inglês' (I speak English), 'Eu falo português' (I speak Portuguese), etc. This is the final phrase in our self-introduction sequence before reviewing."
                elif self.current_subtopic == "D" and has_demonstrated:
                    # Check if "Eu falo [language]" is properly formed
                    is_correct = "eu falo" in question.lower() and len(question.split()) >= 3

                    # Extract the language if properly formed
                    lang_match = re.search(r'eu\s+falo\s+(\w+(?:\s+\w+)*)', question.lower())
                    if lang_match and is_correct:
                        # Get the language from input preserving capitalization
                        language = " ".join(word for word in question.split()[2:])
                        self.user_info['language'] = language

                    # Check for common English language names that should be in Portuguese
                    english_languages = ["english", "japanese", "spanish", "french", "german", "italian", "chinese"]
                    portuguese_languages = ["inglês", "japonês", "espanhol", "francês", "alemão", "italiano", "chinês"]

                    # For inglês (English), be more lenient with accent mark
                    if "ingles" in question.lower() and "inglês" not in question.lower():
                        # Accept "ingles" without accent for English speakers
                        is_correct = True
                        self.user_info['language'] = "inglês"

                    # For other English language names, provide guidance instead of marking as incorrect
                    for i, lang in enumerate(english_languages):
                        if lang.lower() in question.lower() and lang.lower() != "english":
                            # Store the language the user is trying to express
                            self.user_info['language'] = portuguese_languages[i]

                            # The sentence is structurally correct, just needs vocabulary help
                            is_correct = True

                            # Add teaching guidance rather than error correction
                            system_prompt += f"\n\nI noticed the user used the English word '{lang}' in their Portuguese sentence. This is a learning opportunity, not a mistake. Teach them that the Portuguese word for '{lang}' is '{portuguese_languages[i]}'. Acknowledge that their sentence structure was correct, and they're learning new vocabulary."
                            break

                    # After 'Eu falo ...', trigger a recap and move directly to Lesson 2
                    if is_correct and self.current_subtopic == "D":
                        # Always use the most recent value of language (from this answer)
                        language = None
                        # Try to extract the language from the current answer, if possible
                        lang_match = re.search(r'eu\s+falo\s+(\w+(?:\s+\w+)*)', question.lower())
                        if lang_match:
                            # Use the actual user input for the language
                            language = " ".join(word for word in question.split()[2:])
                        else:
                            language = self.user_info.get('language', '[language]')
                        recap = "Here is a recap of your self-introduction in Portuguese, using your own information:\n\n"
                        name = self.user_info.get('name', '[name]')
                        hometown = self.user_info.get('hometown', '[city]')
                        current_city = self.user_info.get('current_city', '[city]')
                        recap += f'"Eu sou {name}" - I am {name}\n'
                        recap += f'"Eu sou de {hometown}" - I am from {hometown}\n'
                        recap += f'"Eu moro em {current_city}" - I live in {current_city}\n'
                        recap += f'"Eu falo {language}" - I speak {language}\n\n'
                        recap += "Now let's move on to the next topic: definite articles in Portuguese.\n\n"
                        recap += "The definite articles are: 'o' (masculine singular), 'a' (feminine singular), 'os' (masculine plural), and 'as' (feminine plural). Here are some examples:\n"
                        recap += "- 'o' (masculine singular)\n- 'a' (feminine singular)\n- 'os' (masculine plural)\n- 'as' (feminine plural)\n\n"
                        recap += "Now, could you tell me your preferred pronoun (he/him, she/her, or they/them)? This will help personalize your introduction in Portuguese using the correct article. Please reply with your pronoun."
                        system_prompt += f"\n\n{recap}"
                        self.current_subtopic = "A"
                        self.current_lesson = 2
                        # Store that we are waiting for pronoun
                        self.user_info['awaiting_pronoun'] = True
                    # After user provides pronoun, present 'Eu sou o/a [name]' form
                    elif self.user_info.get('awaiting_pronoun') and ('he/him' in question.lower() or 'she/her' in question.lower() or 'they/them' in question.lower()):
                        pronoun = None
                        article = None
                        if 'he/him' in question.lower():
                            pronoun = 'he/him'
                            article = 'o'
                        elif 'she/her' in question.lower():
                            pronoun = 'she/her'
                            article = 'a'
                        elif 'they/them' in question.lower():
                            pronoun = 'they/them'
                            article = 'x'
                        name = self.user_info.get('name', '[name]')
                        # Save pronoun and article
                        self.user_info['pronoun'] = pronoun
                        self.user_info['article'] = article
                        self.user_info['awaiting_pronoun'] = False
                        # Present the personalized introduction
                        system_prompt += f"\n\nBased on your pronoun, here is how you would introduce yourself in Portuguese using the correct article:\n\n\"Eu sou {article} {name}\" - I am {name} (with the appropriate article for your gender/pronoun).\n\nLet's continue with more about definite articles and their usage."
                    elif self.current_subtopic == "A" and self.current_lesson == 2:
                        system_prompt += "\n\nIMPORTANT: Now move to teaching Lesson 2 on definite articles. Do NOT suggest more languages to speak. Introduce the definite articles 'o', 'a', 'os', 'as' and explain when to use them. Provide clear examples showing gender and number agreement."
                    elif self.current_subtopic == "A" and self.current_lesson == 3:
                        system_prompt += "\n\nIMPORTANT: Now move to teaching Lesson 3 on prepositions and contractions. Introduce the preposition 'de' and its various uses. Provide clear examples of how prepositions are used in everyday conversation."
                    elif self.current_subtopic == "review":
                        system_prompt += "Before moving to Lesson 2 on definite articles, provide a comprehensive review of Lesson 1. Summarize all four components they've learned: 'Eu sou [name]', 'Eu sou de [city]', 'Eu moro em [city]', and 'Eu falo [language]'. Use the user's actual provided information in your examples. After this review, instruct the user to confirm when they're ready to proceed to Lesson 2."
                    else:
                        system_prompt += "Then introduce the next concept. Provide a clear example of the next phrase pattern. Move directly to teaching the next concept."

                    system_prompt += " DO NOT mention any step numbers or step identifiers in your response."
                elif has_demonstrated and not is_correct:
                    # User attempted but made a mistake
                    system_prompt += "\n\nThe user has attempted the current topic but made a mistake. Point out the specific error in their Portuguese response and ask them to try again. Provide the correct pattern again as a reminder. Do NOT move on to the next topic until they get this right."

                response = self.client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[{
                        "role": "system",
                        "content": system_prompt
                    }, {
                        "role": "user",
                        "content": question
                    }],
                    temperature=0.7)

                # Advance to next subtopic if correct
                if is_correct:
                    expected_subtopic_sequence = ["A", "B", "C", "D", "review"]
                    current_index = expected_subtopic_sequence.index(self.current_subtopic) if self.current_subtopic in expected_subtopic_sequence else 0
                    if current_index < len(expected_subtopic_sequence) - 1:
                        self.current_subtopic = expected_subtopic_sequence[current_index + 1]

                # Convert the Portuguese text to colloquial form
                colloquial_text, _ = self.transform_to_colloquial(question)

                # Generate glossary for response text
                glossary = self.extract_portuguese_words(response.choices[0].message.content)

                # Only focus on words in the system response, not from user input
                return response.choices[0].message.content, True, colloquial_text, glossary
            else:
                # If not Portuguese, just respond normally in English
                response = self.client.chat.completions.create(
                    model="gpt-4.1-mini",
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