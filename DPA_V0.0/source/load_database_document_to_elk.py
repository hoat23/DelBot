# coding: utf-8
# Developer: Deiner Zapata Silva.
# Date: 10/06/2020
# Description: Ingresa user,pass y login to url.
#########################################################################################
import logging
import requests
import yaml #pyyaml
import json
import sys
import time
import datetime
import os
import pandas as pd
import unicodedata
from pandas import read_excel # pip install xlrd
from utils import *
from elastic import *

INDEX = "document_bd/_doc"
path_full = "C:/Users/LENOVO/Documents/PythonCode/ProyectoOsiptel/files/Documents2019.csv"
data_json = loadCSVtoJSON(path_full,encoding="UTF-8")
elk = elasticsearch()
cant_bloques = int( len(data_json)/100)

for doc_100 in range(0, cant_bloques+1):
    print("first_bloque {}/{}".format(doc_100,cant_bloques))
    list_doc = []
    for idx in range(0,100):
        one_json = data_json[doc_100*100 + idx]
        data = one_json['data']
        tmp_json = json.loads(data)
        one_json.update(tmp_json)
        list_doc.append(one_json)
        time.sleep(1000)
    elk.post_bulk(list_doc,header_json={"index":{"_index":"document_bd","_type":"_doc"}})

