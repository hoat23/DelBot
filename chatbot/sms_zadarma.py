#pip install twilio==5.7.0
# Download the helper library from https://www.twilio.com/docs/python/install
# Media message max size 5MB
# Last Update: 20/06/2020
######################################################################################
# https://www.twilio.com/blog/whatsapp-media-support
######################################################################################
from credentials import *
from zadarma import api
from utils import *
import json
######################################################################################################
# https://github.com/zadarma/user-api-py-v1/blob/master/examples/example.py

YOU_KEY = credentials['zadarma']['key']
YOUR_SECRET = credentials['zadarma']['secret']
z_api = api.ZadarmaAPI(key=YOU_KEY, secret=YOUR_SECRET)

def send_sms(text_to_send, to_number="51999222333" ):
    """
    Parámetros:
    number: número de teléfono para enviar SMS (se pueden enumerar varios separados por comas);
    message: mensaje (restricciones estándar sobre la longitud de los SMS, en caso de exceder el límite, dividido en varios SMS);
    caller_id: (opcional) número de teléfono del que se envía el SMS (solo se puede enviar desde la lista de números de usuarios confirmados).
    """
    # send sms
    params = {
        "number": to_number,
        "message": text_to_send
    }
    rpt = z_api.call('/v1/sms/send/', format="json", request_type='POST', params=params)
    print_json(rpt)
    return rpt

if __name__ == "__main__":
    ##################################### ZADARMA TESTING ###########################################
    z_api = api.ZadarmaAPI(key=YOU_KEY, secret=YOUR_SECRET)
    print( " Get tariff information  - ZADARMA " )
    rpt = z_api.call('/v1/tariff/', format="json")
    print_json(rpt.json())

    print( " Send a text message to my cellphone ")
    my_number_cellphone = credentials['deiner']['cellphone'] # "51999222333"
    send_sms("Hoat23 05:15 20/06/2020", to_number=my_number_cellphone)

    # set callerid for your sip number
    #z_api.call('/v1/sip/callerid/', {'id': '1234567', 'number': '71234567890'}, 'PUT')
    # get information about coast
    #z_api.call('/v1/info/price/', {'number': '71234567891', 'caller_id': '71234567890'})
    