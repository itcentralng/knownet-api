import os
import africastalking

def send_sms(recipient, message, sender=None):
        # Set your app credentials
        username = os.getenv("AT_USERNAME")
        api_key = os.getenv("AT_API_KEY")

        # Initialize the SDK
        africastalking.initialize(username, api_key)

        # Get the SMS service
        sms = africastalking.SMS
        # Set the numbers you want to send to in international format
        recipients = [recipient]

        # Set your shortCode or senderId
        sender = sender or os.getenv("AT_SHORTCODE")
        try:
            # Thats it, hit send and we'll take care of the rest.
            sms.send(message, recipients, sender)
        except Exception as e:
            print ('Encountered an error while sending: %s' % str(e))