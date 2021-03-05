#pip install twilio==5.7.0
# Download the helper library from https://www.twilio.com/docs/python/install
# Media message max size 5MB
# Last Update: 04/13/2021
######################################################################################
# https://www.twilio.com/blog/whatsapp-media-support
"""
curl  'https://api.twilio.com/2010-04-01/Accounts/MYUSER/Messages.json' -X POST 
--data-urlencode 'To=whatsapp:+51999222333'  
--data-urlencode 'From=whatsapp:+14155238886' 
--data-urlencode  'Body=Hello! I am Deiner testing my code.!!!' 
-u MYUSER:MYPASSWORD
"""
######################################################################################
import time
import datetime
from credentials import *
from twilio.rest import Client
# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
######################################################################################
account_sid = TWILIO['ID']
auth_token = TWILIO['TOKEN']
######################################################################################
twilio_fiels_whatsapp = [
"originalMessage",
"SmsMessageSid",
"NumMedia",
"SmsSid",
"SmsStatus",
"Body",
"To",
"NumSegments",
"MessageSid",
"AccountSid",
"From",
"ApiVersion",
"chatId",
"userId",
"transport",
"ts",
]

def twilio_request_to_json(request, fielstosave=twilio_fiels_whatsapp):
    data_json = {}
    for field in fielstosave:
        data_json.update({ field : request.values.get(field) })
    data_json.update({'timestamp': datetime.datetime.utcnow().isoformat()})
    return data_json

######################################################################################
client_obj = Client(account_sid, auth_token)

def send_whatsapp(text_to_send, to_number="+51999222333", client_obj=client_obj, img_url="https://images.unsplash.com/photo-1545093149-618ce3bcf49d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80"):
    to_num = "whatsapp:{0}".format(  to_number )
    from_num = "whatsapp:{0}".format( "+14155238886" )
    message = client_obj.messages \
                    .create(
                        media_url=[img_url],
                        body=text_to_send,
                        from_=from_num,
                        to=to_num
                    )
    
    #print(message.sid)
    return message

def send_sms(text_to_send, to_number="+51999222333", from_ = '+15017122661', client_twilio=client_obj):
    if len(text_to_send)==0:
        text_to_send = "Join Earth's mightiest heroes. Like Kevin Bacon."
    
    message = send_one_message(text_to_send, to_number, from_, client_twilio)
    return message

def get_twilio_connection():
    client_twilio = Client(account_sid, auth_token)
    return client_twilio

def send_one_message(text_to_send, to_number, from_, client_twilio, num_tries=3):
    if text_to_send == None:
        print("send_one_message | MSG NULL |".format(text_to_send))
        return False
    for i in range(0, num_tries):
        try:
            client_twilio.messages \
                    .create(
                        body=text_to_send,
                        from_=from_,
                        to=to_number
                    )
        except Exception as e:
            print("send_one_message |   ERROR  |{}|".format(text_to_send))
        else:
            break
    else:
        print("send_one_message | CRITICAL |{}|".format(text_to_send))
    return True
######################################################################################################
if __name__== "__main__":
    ##################################### TWILIO TESTING #############################################
    client_obj = get_twilio_connection()
    text_to_send = "Hola mundo...\n from Python"
    img_url = "https://github.com/hoat23/hoat23.github.io/blob/master/img/Hoat23.jpg?raw=true"
    #send_whatsapp(text_to_send, to_number="+51999222333", client_obj=client_obj, img_url=img_url)
    #whatsapp://send?phone=<e164 number>&text=Hello!
