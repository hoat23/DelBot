# coding: utf-8
######################################################################################
# Developer: Deiner Zapta Silva
# Date: 10/01/2021
# Lat update: 04/02/2021
# Description: querys used in elasticsearch
# Notes: Nothing... :-)
######################################################################################
def query_userdata(chatId):
	body_query = { 
		'query': {
			'match': {
				'chatId': chatId 
			} 
		} 
	}
	return body_query

def query_last_message(chatId,dialog_direction=None):
	if dialog_direction!=None:
		query_string = "user.chatId: \"{0}\" AND dialog.direction: \"{1}\"".format(chatId,dialog_direction)
	else:
		query_string = "user.chatId: \"{0}\"".format(chatId)
	
	body_query = {
	"query": {
		"query_string": {
			"query": query_string
		}
	},
	"sort": [{"dialog.timestamp": {"order": "desc"}}],
	"size": 1
	#"_source": ["dialog_flow"]
	}
	return body_query

def query_first_bloque(level, tracking):
	query_string = "bloque.level: {0} AND bloque.tracking: \"{1}\"".format(level,tracking);
	body_query = {
		"query": {
			"query_string": {
				"query": query_string
			}
		},
		"size": 1,
		"_source": ["message", "bloque"]
	}
	return body_query

def query_next_bloque_v2(user_response, level, tracking):
	query_string = "bloque.response: \"{0}\" AND bloque.level: {1} AND bloque.tracking: \"{2}\"".format(user_response,level,tracking)
	body_query = {
		"query": {
			"query_string": {
				"query": query_string
			}
		},
		"size": 1,
		"_source": ["message", "bloque"]
	}
	return body_query
def query_next_bloque(msg_default, response, level, tracking):
	if (msg_default==None):
	    query_string = "NOT bloque.response: * AND bloque.level: {0} AND bloque.preview: \"{1}\"".format(level,tracking)
	else:
	    query_string = "bloque.response: \"{0}\" AND bloque.level: {1} AND bloque.preview: \"{2}\"".format(response,level,tracking)
	
	body_query = {
		"query": {
			"query_string": {
				"query": query_string
			}
		},
		"size": 1,
		"_source": ["message", "bloque"]
	}
	return body_query
