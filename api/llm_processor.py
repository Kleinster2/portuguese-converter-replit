import os
import re
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

                    # Only move to Lesson 2 if we've completed subtopic D ("Eu falo...")
                    if is_correct and self.current_subtopic == "D":
                        # Examples for definite articles in Lesson 2
                        article_examples = [
                            "O livro (The book) - masculine singular",
                            "A casa (The house) - feminine singular",
                            "Os livros (The books) - masculine plural",
                            "As casas (The houses) - feminine plural"
                        ]
                        system_prompt += "\n\nIMPORTANT: The user has successfully completed 'Eu moro em' and should now learn 'Eu falo' before moving to Lesson 2. Guide the user to practice 'Eu falo [language]' (I speak [language]) and only move to Lesson 2 after they've demonstrated this correctly."
                    # Only show definite articles prompt when we're actually moving to Lesson 2 (after review)
                    elif is_correct and self.current_subtopic == "review":
                        system_prompt += "\n\nIMPORTANT: The user has successfully completed the self-introduction lesson. DO NOT suggest more languages to speak, DO NOT request any practice or examples from the user, and DO NOT mention cities or previous material. Move directly to Lesson 2 on definite articles. Begin teaching about the definite articles 'o', 'a', 'os', 'as', and their usage with everyday objects (not cities or names). Provide clear examples showing gender and number agreement with common nouns. DO NOT request any writing from the user or ask them to demonstrate what they've learned. DO NOT mention or preview any lessons beyond Lesson 2. DO NOT ASK FOR CONFIRMATION - assume the user is ready to begin Lesson 2."

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
                        # Add review before moving to lesson 2
                        next_subtopic = "review"
                    elif self.current_subtopic == "review":
                        # After review, move to lesson 2 - treat any input (including "yes") as readiness to move on
                        # Only explicitly negative responses should keep in review mode
                        negative_responses = ["no", "not ready", "wait", "not yet", "more review"]

                        # Default to moving forward unless explicitly negative
                        ready_to_advance = not any(neg in question.lower() for neg in negative_responses)
                        
                        # Specifically recognize "yes" as a clear signal to advance
                        if question.lower().strip() == "yes":
                            ready_to_advance = True

                        if ready_to_advance:
                            self.current_lesson = 2
                            next_subtopic = "A"  # Start with first subtopic of next lesson
                            # Create an explicit response for the transition to Lesson 2
                            response = self.client.chat.completions.create(
                                model="gpt-4.1-mini",
                                messages=[{
                                    "role": "system",
                                    "content": """You are a Portuguese language tutor starting Lesson 2 on definite articles.

IMPORTANT CONSTRAINTS:
1. DO NOT review or mention ANY previous lesson material
2. DO NOT mention cities or self-introductions
3. DO NOT ask for ANY homework, practice, or self-introduction
4. DO NOT ask the user to write anything for you to check
5. DO NOT mention any exceptions to rules yet

START FRESH with Lesson 2 about definite articles:
- Begin by explaining what definite articles are: words that correspond to "the" in English
- Present ONLY these four forms: o (masc. singular), a (fem. singular), os (masc. plural), as (fem. plural)
- Give SIMPLE examples with everyday objects like:
  * "o livro" (the book)
  * "a mesa" (the table) 
  * "os livros" (the books)
  * "as mesas" (the tables)
- Explain how articles match the gender and number of the noun

Focus EXCLUSIVELY on this topic without connecting to previous lessons or foreshadowing future lessons."""
                                }, {
                                    "role": "user",
                                    "content": "Yes, I'm ready to start Lesson 2"
                                }],
                                temperature=0.5,
                                max_tokens=800)

                            # Generate glossary for response text
                            glossary = self.extract_portuguese_words(response.choices[0].message.content)

                            # Move to next subtopic AFTER generating response
                            self.current_subtopic = next_subtopic
                            self.current_lesson = 2

                            return response.choices[0].message.content, False, None, glossary
                        else:
                            # Only keep in review mode if user explicitly wants more review
                            next_subtopic = "review"
                    else:
                        next_subtopic = "A"  # Fallback in case of unexpected subtopic
                # Track what the user has learned correctly with actual user information
                learned_phrases = []
                if self.current_subtopic >= "B":
                    name = self.user_info.get('name', '[name]')
                    learned_phrases.append(f"Eu sou {name}")
                if self.current_subtopic >= "C":
                    hometown = self.user_info.get('hometown', '[city]')
                    learned_phrases.append(f"Eu sou de {hometown}")
                if self.current_subtopic >= "D":
                    current_city = self.user_info.get('current_city', '[city]')
                    learned_phrases.append(f"Eu moro em {current_city}")

                # Prepare phrases already learned for inclusion in the prompt
                learned_phrases_text = ""
                if learned_phrases:
                    learned_phrases_text = "The user has correctly learned these specific phrases: " + ", ".join(learned_phrases) + ". Always use these exact phrases with their specific information when reminding them of what they've learned, rather than using placeholders like [name] or [city]."

                # Always respond in English, even if user input is in Portuguese
                system_prompt += "\n\n" + learned_phrases_text + "\n\nIMPORTANT: Always respond ONLY in English, even when the user writes in Portuguese. Never respond in Portuguese. For Portuguese phrases, only provide them as examples with English translations. NEVER include any step numbers (like 'Step 1A') in your responses to the user. DO NOT reveal the upcoming sequence of lessons or phrases - focus only on the current lesson being taught. Do not mention or preview any future lessons beyond the current one."

                if is_correct and next_subtopic:
                    # When user demonstrates correct understanding, move to next topic
                    next_topic_names = {
                        "A": "self-introduction with 'Eu sou [name]'",
                        "B": "expressing hometown/origin with 'Eu sou de [city]'",
                        "C": "expressing current residence with 'Eu moro em [city]'",
                        "D": "expressing language with 'Eu falo [language]'",
                        "review": "Review of Lesson 1"
                    }
                    # Include headers without step numbers
                    subtopic_header = subtopic_headers[
                        next_subtopic] if 'subtopic_headers' in locals(
                        ) else f"{next_topic_names[next_subtopic].capitalize()}"
                    system_prompt += "\n\nThe user has demonstrated correct understanding of the current topic. "

                    # Add specific guidance based on which subtopic we're moving to
                    if next_subtopic == "A" and self.current_lesson == 2:
                        system_prompt += "IMPORTANT: Now move to teaching Lesson 2 on definite articles. Do NOT suggest more languages to speak. Introduce the definite articles 'o', 'a', 'os', 'as' and explain when to use them. Provide clear examples showing gender and number agreement."
                    elif next_subtopic == "A" and self.current_lesson == 3:
                        system_prompt += "IMPORTANT: Now move to teaching Lesson 3 on prepositions and contractions. Introduce the preposition 'de' and its various uses. Provide clear examples of how prepositions are used in everyday conversation."
                    elif next_subtopic == "review":
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

                # Only update the current subtopic after generating the response if correct
                if is_correct and next_subtopic:
                    self.current_subtopic = next_subtopic

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