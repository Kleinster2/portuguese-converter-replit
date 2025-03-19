
from twilio.rest import Client
from portuguese_converter import convert_text
from flask import request
from dotenv import load_dotenv
import os

load_dotenv()

class TwilioHandler:
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.client = Client(self.account_sid, self.auth_token)
        self.whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
    
    def handle_message(self, request_data):
        incoming_msg = request_data.get('Body', '').strip()
        sender = request_data.get('From', '')
        
        # Convert text using existing transformer
        result = convert_text(incoming_msg)
        response_text = result['after']
        
        # Send transformed text back via WhatsApp
        self.client.messages.create(
            body=response_text,
            from_=f'whatsapp:{self.whatsapp_number}',
            to=sender
        )
