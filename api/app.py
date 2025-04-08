
from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
from portuguese_converter import convert_text
from tts_converter import TTSConverter
from twilio_handler import TwilioHandler
from llm_processor import LLMProcessor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Try to initialize Twilio, but continue even if it fails
try:
    twilio = TwilioHandler()
    twilio_enabled = True
    logger.info("Twilio successfully initialized")
except ValueError as e:
    logger.warning(f"Twilio initialization failed: {e}")
    twilio = None
    twilio_enabled = False

# Initialize LLM processor
llm_processor = LLMProcessor()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return send_from_directory('..', 'index.html')

@app.route('/api/portuguese_converter', methods=['GET', 'POST'])
def handle_portuguese_converter():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        text = data['text']
        result = convert_text(text)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error: {str(e)}")


@app.route('/api/tts', methods=['POST'])
def text_to_speech():
    try:
        data = request.get_json()
        text = data.get('text', '')
        variant = data.get('variant', 'br')
        if not text:
            return jsonify({'error': 'No text provided'}), 400

        tts = TTSConverter()
        audio_content = tts.synthesize_speech(text, variant)

        if audio_content:
            return Response(audio_content, mimetype='audio/mpeg')
        else:
            return jsonify({'error': 'Failed to generate audio'}), 500

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/correct_text', methods=['POST'])
def correct_text():
    """Endpoint for correcting typos, syntax, and grammar with LLM"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        text = data['text']
        corrected_text, message = llm_processor.correct_text(text)

        return jsonify({
            'original': text,
            'corrected': corrected_text,
            'message': message
        })
    except Exception as e:
        logger.error(f"Error in text correction: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/transform_colloquial', methods=['POST'])
def transform_colloquial():
    """Endpoint for transforming text to colloquial Portuguese using LLM"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        text = data['text']
        colloquial_text, message = llm_processor.transform_to_colloquial(text)

        return jsonify({
            'original': text,
            'colloquial': colloquial_text,
            'message': message
        })
    except Exception as e:
        logger.error(f"Error in colloquial transformation: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/process_text', methods=['POST'])
def process_text():
    """Combined endpoint for correction and conversion"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        text = data['text']
        apply_correction = data.get('correct', False)
        apply_conversion = data.get('convert', False)
        use_llm_conversion = data.get('use_llm', False)

        result = {'original': text}

        # Step 1: Correct text if requested
        if apply_correction:
            corrected_text, correction_message = llm_processor.correct_text(text)
            result['corrected'] = corrected_text
            result['correction_message'] = correction_message
            # Use corrected text for next step if available
            text_for_conversion = corrected_text
        else:
            text_for_conversion = text

        # Step 2: Convert to colloquial Portuguese if requested
        if apply_conversion:
            if use_llm_conversion:
                # Use LLM-based transformation
                colloquial_text, conversion_message = llm_processor.transform_to_colloquial(text_for_conversion)
                result['conversion'] = {
                    'text': colloquial_text,
                    'llm_based': True,
                    'message': conversion_message
                }
            else:
                # Use rule-based transformation
                conversion_result = convert_text(text_for_conversion)
                result['conversion'] = conversion_result
                result['conversion']['llm_based'] = False

        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in process_text: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Unified endpoint for all chat interactions.
    The LLM will interact with the user and handle transformation requests when needed.
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        user_text = data['text']

        # Check if this is a request to transform text
        transform_keywords = ['transform', 'convert', 'colloquial', 'informal', 'brazilian portuguese']
        is_transform_request = any(keyword in user_text.lower() for keyword in transform_keywords)

        if is_transform_request:
            # Extract the text to be transformed
            # First, try to identify if there's a specific text to transform
            response = llm_processor.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an assistant that identifies text to be transformed. If the user wants to transform text to colloquial Brazilian Portuguese, extract the exact text they want to transform. If no specific text is identified, respond with 'NO_TEXT'."},
                    {"role": "user", "content": user_text}
                ],
                temperature=0.1
            )

            extracted_text = response.choices[0].message.content

            if extracted_text != "NO_TEXT":
                # If specific text was identified, transform it
                llm_transformed, _ = llm_processor.transform_to_colloquial(extracted_text)

                # Also apply rule-based transformation for comparison
                rule_based = convert_text(extracted_text)

                # Get the LLM to create a response about the transformation
                explanation_response = llm_processor.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant explaining Portuguese text transformation. Respond in a friendly, conversational way. Mention that you're showing both LLM and rule-based transformations."},
                        {"role": "user", "content": f"The user wants to transform this text: '{extracted_text}'"}
                    ],
                    temperature=0.7
                )

                return jsonify({
                    'response': explanation_response.choices[0].message.content,
                    'transformation': {
                        'original': extracted_text,
                        'llm': llm_transformed,
                        'rule_based': rule_based['after']
                    }
                })
            else:
                # If no specific text identified, ask for it (in English)
                return jsonify({
                    'response': "I'd be happy to transform Portuguese text to colloquial Brazilian Portuguese! Please provide the text you'd like me to transform."
                })
        else:
            # Regular chat interaction - detect Portuguese and show transformation if applicable
            response, is_portuguese, colloquial_version, glossary = llm_processor.ask_question(user_text)

            result = {
                'response': response,
                'glossary': glossary
            }

            # Include transformation if Portuguese was detected and this isn't a command/question
            if is_portuguese and len(user_text.split()) > 3 and not user_text.endswith('?'):
                result['transformation'] = {
                    'llm': colloquial_version,
                    'rule_based': convert_text(user_text)['after']
                }

            return jsonify(result)

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/ask_llm', methods=['POST'])
def ask_llm():
    """Interactive endpoint for LLM chat with Portuguese detection"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        user_text = data['text']

        # Process the user's text with the LLM
        response, is_portuguese, colloquial_version, glossary = llm_processor.ask_question(user_text)

        # If no glossary was returned but there are Portuguese phrases in the response,
        # try to extract them directly
        if not glossary and '"' in response and not is_portuguese:
            glossary = llm_processor.extract_portuguese_words(response)
            
        result = {
            'response': response,
            'is_portuguese': is_portuguese,
            'glossary': glossary
        }

        # Include colloquial version if Portuguese was detected
        if is_portuguese and colloquial_version:
            result['colloquial'] = colloquial_version

            # Also include rule-based transformation for comparison
            rule_based = convert_text(user_text)
            result['rule_based'] = rule_based['after']

        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in ask_llm: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/webhook/twilio', methods=['POST'])
def twilio_webhook():
    try:
        if not twilio_enabled:
            logger.warning("Twilio webhook called but Twilio is not configured")
            return jsonify({'error': 'Twilio is not configured'}), 503

        twilio.handle_message(request.form)
        return '', 200
    except Exception as e:
        logger.error(f"Error in Twilio webhook: {str(e)}")
        return '', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=False)
