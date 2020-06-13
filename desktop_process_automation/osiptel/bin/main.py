
# coding: utf-8
# Developer: Deiner Zapata Silva.
# Date: 10/06/2020
# Description: Ingresa user,pass y login to url.
#########################################################################################
import logging
import sys
import time
from utils import *
from login import *
from datamanager import *
from fill_data_formulario import *
from logging_advance import *
import pyautogui as gui
gui.FAILSAFE = True

if __name__ == "__main__":    
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)
    logging.debug("| INI | {0} testing".format(__file__))
    #sys.setdefaultencoding( "utf-8" )
    idx_sheet = 0#int( input('retomar sheet:') ) # 3 tipos = ["Consejo Directivo","Presidencia","Gerencia General"]
    idx_doc = 619#int( input('retomar docum:') )
    
    retomar={'idx_sheet': idx_sheet, 'idx_doc': idx_doc}
    ## open browser and login
    url = "https://localhost:44347/umbraco/"#"http://44.231.13.118/umbraco/"
    user = "usuario@osiptel.com"
    pasw = "maQUEtaHTML567"

    driver = login(url, user, pasw)

    ## loading excel
    filename = "Filtrado_1.xlsx"
    fullpath = "D:\\DPA\\files\\"+filename
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
    data_json = load_excel(fullpath, list_sheets, columns_rename=columns_rename)
    #print_json(data_json)
    time.sleep(5)
    ## loading page formulario
    load_page_formulario(url,driver)

    ## loading data from excel
    fill_data_formulario(data_json, list_sheets, driver, retomar = retomar)
    
    logging.debug("| END | {0} testing".format(__file__))
    pass