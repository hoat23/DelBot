#pip install twilio==5.7.0
# Download the helper library from https://www.twilio.com/docs/python/install
# Media message max size 5MB
# Last Update: 20/06/2020
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
from credentials import *
from twilio.rest import Client
# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure

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
    print(message) #
    print(message.sid)
    return message

def send_sms(text_to_send, to_number="+51999222333", client_obj=client_obj):
    message = client_obj.messages \
                    .create(
                        body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                        from_='+15017122661',
                        to='+15558675310'
                    )
    print(message)
    return message
######################################################################################################

if __name__== "__main__"
    ##################################### TWILIO TESTING #############################################
    client_obj = Client(account_sid, auth_token)
    text_to_send = "Hola mundo...\n from Python"
    img_url = "https://github.com/hoat23/hoat23.github.io/blob/master/img/Hoat23.jpg?raw=true"
    #send_whatsapp(text_to_send, to_number="+51999222333", client_obj=client_obj, img_url=img_url)
    #whatsapp://send?phone=<e164 number>&text=Hello!
