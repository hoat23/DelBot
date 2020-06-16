
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
    #logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.mBUG)
    log = logging_advance(_index="debug-python", service='', send_elk=True)
    log.print_debug("INI |", data_json={}, name_function="__main__")
    #sys.setdefaultencoding( "utf-8" )
    idx_sheet = 0#int( input('retomar sheet:') ) # 3 tipos = ["Consejo Directivo","Presidencia","Gerencia General"]
    idx_doc = 0 #870#868#828#696#516#424#366 #69 #14#int( input('retomar docum:') )
    
    retomar={'idx_sheet': idx_sheet, 'idx_doc': idx_doc}
    ## open browser and login
    url = "https://localhost:44347/umbraco/"
    user = "usuario@osiptel.com"
    pasw = "maQUEtaHTML567"
    
    driver = login(url, user, pasw)

    ## loading excel
    filename = "Filtrado_2.xlsx"
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
    log.print_debug("INI | Variables de inicio ", data_json={'retomar': retomar, 'filename': filename}, name_function="__main__")
    data_json = load_excel(fullpath, list_sheets, columns_rename=columns_rename)
    #print_json(data_json)
    time.sleep(5)
    ## loading page formulario
    load_page_formulario(url,driver)

    ## loading data from excel
    fill_data_formulario(data_json, list_sheets, driver, retomar = retomar)
    
    log.print_debug("END |", data_json={}, name_function="__main__")
    pass