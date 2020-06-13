# coding: utf-8
# Developer: Deiner Zapata Silva.
# Date: 13/06/2020
# Description: Credenciales para ingestar datos al cluster
#########################################################################################
credentials= {
    "gloumedia": {
        "url": "http://44.231.13.118/umbraco/",
        "user": "usuario@osiptel.com",
        "pasw": "maQUEtaHTML567"
    },
    "elastic": {
        "url": "https://eb86380581ab45aab2f6959fd35dbb3b.us-west-2.aws.found.io:9243",
        "user": "ingest",
        "pasw": "ingestgloumedia"
    }
}

URL = credentials['elastic']['url']
USER = credentials['elastic']['user']
PASS = credentials['elastic']['pasw']
#########################################################################################


