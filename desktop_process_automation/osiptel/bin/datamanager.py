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
from pandas.io.json import json_normalize
from utils import *
#######################################################################################
def xlsx_2_pandas(fullpath, name_sheet, drop_colums=[], drop_rows=[], delete_columns_name=False): 
    only_name_file = os.path.basename(fullpath)
    fullpath_name, extension = os.path.splitext(fullpath)
    df = None
    if extension == '.xlsx':
        df = read_excel(fullpath, sheet_name = name_sheet, encoding='javascript') #Global, PERU
        #if delete_columns_name:
        #del df.columns.name
        logging.info("extract_sheet_from_xlsx | {1} | {0}".format(only_name_file, df.shape))
    else:
        print("xlsx_2_pandas | ERR | {0}".format(only_name_file))
    return df
#######################################################################################
def load_sheet(fullpath,name_sheet,columns_rename=None):
    df = xlsx_2_pandas(fullpath, name_sheet, delete_columns_name=True)
    if columns_rename!=None: df.columns = columns_rename
    df_str = df.to_json(orient= 'records') # orient : records, index, values, table, columns(default)
    # Selecting some fields
    bucket_documents = json.loads(df_str)
    logging.info("load_excel | {0} | {1}".format(name_sheet,len(bucket_documents)))
    return bucket_documents
#########################################################################################
def load_excel(fullpath, list_sheets,columns_rename=None):
    data_json = {}
    for name_sheet in list_sheets:
        bucket_documents = load_sheet(fullpath,name_sheet,columns_rename=columns_rename)
        #print_json(bucket_documents)
        tmp = name_sheet.lower().replace(" ","")
        if len(tmp)>0:
            data_json.update( {tmp: bucket_documents } )
    return data_json

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)
    logging.debug("| INI | {0} testing".format(__file__))
    fullpath = "D:\\DPA\\files\\Filtrado_1.xlsx"
    list_sheets = ["Consejo Directivo","Presidencia","Gerencia General"]
    columns_rename = [
        "resolucion",
        "anio",
        "tema",
        "enlace",
        "materia",
        "submateria",
        "or"
    ]
    data_json = load_excel(fullpath,list_sheets,columns_rename=columns_rename)
    print_json(data_json)
    logging.debug("| END | {0} testing".format(__file__))