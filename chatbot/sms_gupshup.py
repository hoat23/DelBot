#coding: UTF-8 
#########################################################################################
# Developer: Deiner Zapata Silva.
# Date: 20/03/2021
# Last update: 04/04/2021
# Description: Server to conect Streak - Webhoook
# Notes: Send and receive message from Gupshup
# PostmanCollections: https://www.postman.com/collections/820a513fd242f49cc01d
# Documentation: https://www.gupshup.io/developer/docs/bot-platform/guide/whatsapp-api-documentation-sp
#########################################################################################
import sys
import requests
import json
import time
from datetime import datetime, timedelta
from credentials import GUPSHUP
from utils import *
import urllib
from utils_logging import get_logger
######################################################################################
logger = get_logger('sms_gupshup.py', level='DEBUG')
######################################################################################
def get_header(content_type):
	headers = headers = {
		'Content-Type': content_type,
		'Accept-Encoding': 'gzip, deflate, br',
		'Connection': 'keep-alive',
		'apikey': GUPSHUP['TOKEN']
	}
	return headers

def get_url_api(funcionality):
	URL = 'https://api.gupshup.io/sm/api'
	APPNAME = GUPSHUP['APPNAME']
	URL_API = {
		'Balance': "{}/v2/wallet/balance".format(URL),
		'Opted_in_contacts': "{}/v1/users/{}".format(URL, APPNAME),
		"Register_user": "{}/v1/app/opt/in/{}".format(URL, APPNAME)
	}

	return URL_API.get(funcionality)

def get_balance(timeout = 3):
	headers = get_header('application/json')
	URL_API = get_url_api('Balance')
	rpt = requests.get( url=URL_API , headers=headers , data=None , timeout=timeout)
	return rpt.json()

def get_opted_in_contacts(timeout = 3):
	"""
	Gets the list of all opted-in and opted-out users and the timestamp for the last message sent by user. Useful to check if a user is opted in and to calculate when the session will be closed for a user.
	"""
	URL_API = get_url_api('Opted_in_contacts')
	headers = get_header('application/json')
	#data = json.dumps(data)
	rpt = requests.get( url=URL_API , headers=headers , data=None , timeout=timeout)
	return rpt.json()

def get_register_user(phonenumber, timeout = 3):
	"""
	Use this API to register at Gupshup's database when a user agrees to receive messages from your company. The user may tell you that he/she agrees via SMS, phone, e-mail etc. You will only be allowed to send template messages to users for whom you registered the optin.
	URL: https://www.gupshup.io/whatsapp/view-users;bName=HolaMusa;bt=true
	"""
	URL_API = get_url_api('Register_user')
	headers = get_header('application/x-www-form-urlencoded')
	data = {'user': phonenumber}

	data = urllib.parse.urlencode( data )
	rpt = requests.post( url=URL_API, headers=headers , data=data , timeout=timeout)
	logger.info("register_user | {}".format(rpt))
	return rpt

def drive_reformat_url(drive_url):
	if drive_url.find("https://drive.google.com/file/d/")>=0 and drive_url.find("/view")>=0:
		drive_url = drive_url.replace("/view","")
		drive_url = drive_url.replace("https://drive.google.com/file/d/","https://drive.google.com/u/0/uc?id=")
	return drive_url

def send_one_message_gs(text_to_send, to_number, from_, num_tries=3, APPNAME=GUPSHUP['APPNAME'], timeout = 5):
	"""
	ERROR  -> img="https://drive.google.com/file/d/1jwjpPNsq40G7PN7qmznPhFvGxXq3En8C/view"
	CORRECT-> text_to_send="img=https://drive.google.com/u/0/uc?id=1jwjpPNsq40G7PN7qmznPhFvGxXq3En8C&export=download"
	CORRECT-> text_to_send="img=https://drive.google.com/u/0/uc?id=1jwjpPNsq40G7PN7qmznPhFvGxXq3En8C"
	"""
	if text_to_send==None:
		logger.info("send_one_message | Gupshup | MSG NULL |".format(text_to_send))
		return False

	for i in range(0, num_tries):
		try:
			message = text_to_send
			text_foot_multimedia = ""

			if text_to_send.find('img=')>=0:
				multimedia_url = text_to_send[ text_to_send.find('img=')+4:]
				multimedia_url = drive_reformat_url(multimedia_url)
				logger.debug("send_one_message|URL={}".format(multimedia_url))
				message = {
					"type":"image",
					"originalUrl":multimedia_url,
					"previewUrl":multimedia_url,
					"caption":text_foot_multimedia
				}

			if text_to_send.find('aud=')>=0:
				multimedia_url = text_to_send[ text_to_send.find('aud=')+4:]
				multimedia_url = drive_reformat_url(multimedia_url)
				logger.debug("send_one_message|URL={}".format(multimedia_url))
				message = {
					"type":"audio",
					"url":multimedia_url
				}

			if text_to_send.find('vid=')>=0:
				text_foot_image = ""
				multimedia_url = text_to_send[ text_to_send.find('vid=')+4:]
				multimedia_url = drive_reformat_url(multimedia_url)
				logger.debug("send_one_message|URL={}".format(multimedia_url))
				message = {
					"type":"video",
					"url":multimedia_url,
					"caption": text_foot_multimedia
				}

			URL_API = "https://api.gupshup.io/sm/api/v1/msg"
			headers = get_header('application/x-www-form-urlencoded')
			data = {
					'channel': 'whatsapp',
					'source': from_,
					'destination': to_number,
					'message': message,
					'src.name': APPNAME,

			}

			data = urllib.parse.urlencode( data )
			rpt = requests.post( url=URL_API, headers=headers , data=data , timeout=timeout)
			if rpt.status_code == 200:
				logger.info( "Success send [{}]".format(text_to_send) )
			else:
				logger.error("Fail send    [{}]".format(text_to_send) )
		except Exception as e:
			logger.error("Sending {}".format(text_to_send))
			logger.error(e)
		else:
			break
	else:
		logger.critical("Fail send message Gupshup [{}]".format(text_to_send))
	return True

if __name__ == '__main__':

	from credentials import TEST_VARIABLES

	rpt_json = get_balance()
	logger.info("Balance $:", extra=rpt_json)

	rpt_json = get_opted_in_contacts()
	logger.info("Opted in contacts", extra=rpt_json)

	to_number = TEST_VARIABLES['phonenumber']
	rpt_json = get_register_user(to_number)
	logger.info("Register a user", extra=rpt_json)

	logger.info("Send message")
	from_ = GUPSHUP ['PHONENUMBER']

	logger.info("Send image")
	send_one_message_gs("img=https://images.pexels.com/photos/248797/pexels-photo-248797.jpeg", to_number, from_, num_tries=3)

	logger.info("Send audio")
	send_one_message_gs("aud=https://drive.google.com/file/d/1rFgR85d1ZUJ2j4ZlHI1eRbtK2WXamhnR/view", to_number, from_, num_tries=3)

	logger.info("Send video")
	send_one_message_gs("vid=http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4", to_number, from_, num_tries=3)
	
	logger.info("Testing massive messages")
	for i in range(0,2):
		message = 'text_to_send {}'.format(i)
		send_one_message(message, to_number, from_, num_tries=3)
	

