from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
from portuguese_converter import convert_text
from tts_converter import TTSConverter
from twilio_handler import TwilioHandler
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
    app.run(host='0.0.0.0', port=3000, debug=False)