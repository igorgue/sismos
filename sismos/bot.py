from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

# Your Account SID from twilio.com/console
account_sid = "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
# Your Auth Token from twilio.com/console
auth_token = "your_auth_token"

client = Client(account_sid, auth_token)


def handle_message(message):
  # Your code here
  return "This is my response to your message"


message = "This is my response to your message"
response = MessagingResponse()
response.message(handle_message(message))
