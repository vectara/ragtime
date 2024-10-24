import logging
import os

from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from utils import query_vectara

ACCOUNT_SID = os.getenv("ACCOUNT_SID", None)
Auth_TOKEN = os.getenv("Auth_TOKEN", None)
twilio_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")


app = Flask(__name__)
vectara_prompt = 'vectara-summary-ext-24-05-med-omni'

if ACCOUNT_SID and Auth_TOKEN:
    # Initialize Twilio client
    client = Client(ACCOUNT_SID, Auth_TOKEN)


# Function to send a WhatsApp message via Twilio
@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    logging.info(request.form.get('Body'))
    incoming_message = request.form.get('Body')
    user_phone_number = request.form.get('From')
    vectara_conv_id, response, _ = query_vectara(incoming_message, None, vectara_prompt, None, bot_type="whatsapp")

    logging.info(response)

    # Send the response back to the user with a status callback
    message = client.messages.create(
        body=response,
        from_=twilio_whatsapp_number,
        to=user_phone_number,
        # status_callback="https://your-server-url.com/message-status"
    )

    # Respond to Twilio with an empty response (optional)
    resp = MessagingResponse()
    return str(resp)


async def start_whatsapp_bot():
    app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
