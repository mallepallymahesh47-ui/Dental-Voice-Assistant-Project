from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()


ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
MY_NO = os.getenv("MY_PHONE_NUMBER")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

call = client.calls.create(
    to=MY_NO,
    from_="+18148014951",
    url="https://handler.twilio.com/twiml/EH9d61e06b7440bc4619af73b9ec69b4dd"
)

