from twilio.rest import Client
import pytz
from datetime import datetime

class WhatsAppManager:
    def __init__(self):
        self.twilio_client = Client(os.getenv('TWILIO_SID'), os.getenv('TWILIO_TOKEN'))
        self.sa_timezone = pytz.timezone('Africa/Johannesburg')
        self.templates = {
            'welcome': {
                'en': "Hi {name}! Thanks for contacting us. Reply with:\n1 for English\n2 for Afrikaans\n3 for isiZulu",
                'af': "Hallo {name}! Dankie dat jy ons gekontak het. Antwoord met:\n1 vir Engels\nn2 vir Afrikaans",
                'zu': "Sawubona {name}! Siyabonga ukusithintayo. Phendula ngo:\n1 ngesiNgisi\n2 ngesiZulu"
            },
            'followup': {
                'en': "Hi {name}, don't miss our launch special! Get {discount}% off when you sign up this week: {link}",
                'af': "Hallo {name}, moenie ons beginspesiale misloop nie! Kry {discount}% af wanneer jy hierdie week aansluit: {link}",
                'zu': "Sawubona {name}, ungaphuthelwa yisipesheli sethu! Thola {discount}% phansi uma ubhalisa kuleli sonto: {link}"
            }
        }

    def send_whatsapp_message(self, to: str, template: str, language: str = 'en', **kwargs):
        """Send localized WhatsApp message"""
        try:
            # Format message with personalization
            message_body = self.templates[template][language].format(**kwargs)
            
            # Determine appropriate sending time (SA business hours)
            now = datetime.now(self.sa_timezone)
            if 8 <= now.hour < 20:  # 8am-8pm SAST
                send_time = now
            else:
                send_time = now.replace(hour=9, minute=0) + timedelta(days=1)
            
            # Schedule message
            self.twilio_client.messages.create(
                body=message_body,
                from_='whatsapp:' + os.getenv('TWILIO_WHATSAPP_NUMBER'),
                to='whatsapp:' + to,
                schedule_type='fixed',
                send_at=send_time.isoformat()
            )
            
            # Log interaction
            self._log_whatsapp_interaction(to, template, language)
            
            return True
        except Exception as e:
            self._log_whatsapp_error(to, str(e))
            return False

    def handle_incoming_message(self, from_number: str, message: str):
        """Process incoming WhatsApp messages"""
        # Simple language detection
        language = self._detect_language(message)
        
        # Check if it's an opt-in
        if message.strip().lower() in ['join', 'start', 'info']:
            self._add_to_broadcast_list(from_number)
            return self._send_welcome_message(from_number)
        
        # Handle numeric menu responses
        if message.strip().isdigit():
            return self._handle_menu_selection(from_number, int(message), language)
        
        # Default response
        return self._send_default_response(from_number, language)

    def launch_whatsapp_campaign(self, contacts: list):
        """Execute bulk WhatsApp campaign"""
        for contact in contacts:
            self.send_whatsapp_message(
                to=contact['number'],
                template='followup',
                language=contact.get('language', 'en'),
                name=contact.get('name', 'there'),
                discount=20,
                link=f"https://signup.example.com/?ref=whatsapp{contact['id']}"
            )
