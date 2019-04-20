# coding: utf-8
# Developer: Deiner Zapata Silva.
# Date: 19/04/2019
# Description: API de consulta la Biblia para integrar con messenger
#########################################################################################
# Todos iniciamos con un gran amor a la ciencia, luego el ego interfiere, 
# la obsesion y cuando volteas ya estas muy lejos de donde querias
#########################################################################################
import sys, requests, json, ast
from credentials import *
from utils import print_json, print_list
from datetime import datetime, timedelta
#########################################################################################
def get_versiculo(passage, biblia_version = "RVR60.js"):
    """
    RVR60   : Reina Valera Revisada (1960)
    RVA     : Reina-Valera Actualizada
    http://bibliaapi.com/docs/Available_Bibles

    Arg passage(string) : "Lucas 3:4-5"   |  "Mateo 27:27-36"
    """
    get_json = {"uri" : "https://api.biblia.com/v1/bible/content/"+biblia_version+"?key="+API_KEY_BIBLE+"&"+"passage="+passage+"&culture=es&style=oneVersePerLine"}
    rpt = req_get (get_json)
    if 'text' in rpt:
        txt = rpt['text'].split("\r\n")
    else:
        txt = ["Upsss... algo anda mal."]
        print("{0}|WARN | get_versiculo | {1}".format( datetime.utcnow().isoformat() , txt[0] ))
    return txt
#######################################################################################
def req_get(get_json , timeout=None):
    json_rpt = {}
    try:
        headers = {'Content-Type': 'application/json'}
        URL_API = get_json['uri']
        rpt = requests.get( url=URL_API , headers=headers, timeout=timeout)
        if not( (rpt.status_code)==200 or (rpt.status_code)==201 ):
            print("{0}|WARN | req_get | {1} | {2} | URL_API=[{3}]".format( datetime.utcnow().isoformat() , rpt.status_code, rpt.reason, URL_API[:40]) )
        json_rpt = rpt.json()#json_rpt = rpt.text
    except:
        print("{0}|ERROR| req_get ".format(datetime.utcnow().isoformat()) )
    finally:
        return json_rpt
#######################################################################################
if __name__ == "__main__":
    print("{0}|INFO | api_bible testing ".format( datetime.utcnow().isoformat() ))
    txt_list = get_versiculo("josue 1:9")
    print_list(txt_list)