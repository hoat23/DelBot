# coding: utf-8
# Developer: Deiner Zapata Silva.
# Date: 10/06/2020
# Description: Carga la pagina "formulario" y llena los datos respectivos
#########################################################################################
import logging
import json
import time
import unicodedata
from utils import *
import pyautogui as gui
import pyperclip as pyc #pip install pyperclip
import html
from load_doc_principal_y_asociados import *
from utils_vision import *
from logging_advance import *
#######################################################################################
log = logging_advance(_index="debug-python", service='fill_data_formulario.py', send_elk=True)
#######################################################################################
## Normalizar cadenas de caracteres
def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper()).replace('\n', ' ').replace('\r', '')
    return s

def load_page_formulario(url,driver):
    #selenium chrome driver with extensions
    log.print_info("INI | url={0}".format(url), name_function=__name__)
    time.sleep(2)
    url_formulario = "{0}#/content/content/edit/1200".format(url)
    driver.get(url_formulario)
    time.sleep(2)
    return driver

def load_page_crearresolucion(filename="boton_crearresolucion.png", directory="D:/DPA/img", pos_xy=None): #D://DPA//bin//
    #logging.debug("load_page_crearresolucion | {0}".format(filename))
    log.print_info("boton".format(filename), name_function="load_page_crearresolucion")
    fullpath = "{0}/{1}".format(directory, filename)
    cont = 0
    while ((pos_xy==None) and (cont < 20)):
        time.sleep(3.2)
        pos_xy = gui.locateOnScreen(fullpath, confidence=0.8, grayscale=True)
        log.print_info("search_buton {1} [{0}] |".format(filename,pos_xy), name_function="load_page_crearresolucion")
        cont = cont + 1
    
    try:
        pos_xy = gui.center(pos_xy)
        log.print_info("click_on_buton {1} [{0}]".format(filename,pos_xy), name_function="load_page_crearresolucion")
        gui.click(pos_xy)
        time.sleep(1)
        log.print_info("return True", name_function="load_page_crearresolucion")
        return True
    except:
        log.print_error("buton_not_found [{0}]".format(filename))
        log.print_info("return False", name_function="load_page_crearresolucion")
        return False

def valida_fill_data_formulario():
    return

def search_elem_in_options(elem_to_search, one_select, tag_name='option'):
    for option in one_select.find_elements_by_tag_name(tag_name):
        OPTION = normalize(option.text.upper())
        ELEM_TO_SEARCH = normalize(elem_to_search.upper())
        logging.debug(" search_elem_in_options | {0} | {1}".format(OPTION, elem_to_search))
        if OPTION == ELEM_TO_SEARCH:
            option.click()
    #input("key")
    return True

def fill_data_one_doc(data_json, one_sheet, driver ):
    """
    funcion que llena los datos de un data_json en la pagina de formulario.
    data_json:  es una fila del excel
    data_json = {
        "anio": 2019,
        "enlace": "https://www.osiptel.gob.pe/articulo/res0259-2019-gg",
        "materia": "NORMAS",
        "or": "GG",
        "resolucion": "N\u00b0 0259-2019-GG/OSIPTEL",
        "submateria": "NORMAS",
        "tema": "Ampliaci\u00f3n de Plazo para la remisi\u00f3n de comentarios al Proyecto de  Instructivo T\u00e9cnico para el cumplimiento de las Normas Complementarias para la Implementaci\u00f3n del Registro Nacional de Equipos Terminales M\u00f3viles para la Seguridad"
    }
    """
    #.encode('ascii', 'xmlcharrefreplace').decode('utf-8')
    numero_res = ( unicodedata.normalize('NFD', data_json['resolucion'] ) ).replace('\n', ' ').replace('\r', '')
    anio = data_json['anio']
    description = (unicodedata.normalize('NFD', data_json['tema'] ) ).replace('\n', ' ').replace('\r', '')
    link_pagina = unicodedata.normalize('NFD', data_json['enlace'] )
    materia = unicodedata.normalize('NFD', data_json['materia'] ).upper()
    submateria = unicodedata.normalize('NFD', data_json['submateria']).upper()
    organo_res = unicodedata.normalize('NFD', data_json['or'] )

    log.print_debug("{0}".format(numero_res), name_function=__name__)
    driver.implicitly_wait(10)
    # Ingreso de información correspondiente
    driver.find_element_by_id("headerName").send_keys()
    driver.execute_script("document.getElementById('headerName').value='"+numero_res[:-1]+"'")
    driver.find_element_by_id("headerName").send_keys(numero_res[-1:])
    driver.execute_script("document.getElementById('seo_titulo').value='"+numero_res[:-1]+"'")
    driver.find_element_by_id ("seo_titulo").send_keys(numero_res[-1:])
    driver.execute_script("document.getElementById('seo_desc').value='"+description[:-1]+"'")
    driver.find_element_by_id ("seo_desc").send_keys(description[-1:])
    driver.execute_script("document.getElementById('res_titulo').value='"+numero_res[:-1]+"'")
    driver.find_element_by_id ("res_titulo").send_keys(numero_res[-1:])
    driver.execute_script("document.getElementById('res_desc').value='"+description[:-1]+"'")
    driver.find_element_by_id ("res_desc").send_keys(description[-1:])
    """
    # Ingreso de información correspondiente
    driver.find_element_by_id("headerName").send_keys()
    driver.find_element_by_id("headerName").send_keys(numero_res)
    driver.find_element_by_id ("seo_titulo").send_keys(numero_res)
    driver.find_element_by_id ("seo_desc").send_keys(description)
    driver.find_element_by_id ("res_titulo").send_keys(numero_res)
    driver.find_element_by_id ("res_desc").send_keys(description)"""

    # Ingreso de datos por bloque de selección
    select = driver.find_elements_by_xpath("//*[@name='dropDownList']")
    search_elem_in_options(organo_res, select[0]) # Organo Resolutivo
    search_elem_in_options(materia, select[1]) # Materia
    search_elem_in_options(submateria, select[2]) # Submateria
    search_elem_in_options(str(anio), select[3]) # Anio
    # Operadoras -> buscador general, Expedientes->Expedientes , para Pedidos de opinion Pedidos
    search_elem_in_options('Operadoras', select[5])

    return valida_fill_data_formulario()

def fill_data_formulario(data_json, list_sheets, driver, retomar={'idx_sheet': 0, 'idx_doc': 0},directory="D:/scraping/book23"):
    log.print_info("driver.current_url = [{0}]".format(driver.current_url), name_function="fill_data_formulario")
    idx_sheet = 0  + retomar['idx_sheet']
    while idx_sheet < len(list_sheets): # 3 tipos = ["Consejo Directivo","Presidencia","Gerencia General"]
        one_sheet = list_sheets[idx_sheet]
        key = one_sheet.lower().replace(" ","")
        bucket_documents = data_json[key] # diccionario de documentos por cada tipo
        log.print_debug("one_sheet=[{0}] | {1}".format(one_sheet, len(bucket_documents)), name_function="fill_data_formulario")
        idx = 0 + retomar['idx_doc']
        while idx < len(bucket_documents):
            one_document = bucket_documents[idx]
            one_document.update({'idx':idx, 'sheet': one_sheet})
            sub_directory =  unicodedata.normalize( 'NFD', one_document['or'] )
            path_directory_princ = "{0}/{1}/{2}".format(directory, sub_directory, idx+1)
            one_document = valida_path(path_directory_princ, one_document)#queda pendiente validar one_document dentro de valida path
            log.print_debug("one_document", data_json=one_document, name_function="fill_data_formulario")
            if len(one_document['doc_principal'])>0:
                #new formulario
                while not load_page_crearresolucion():
                    log.print_debug("loading new page [crearresolucion]", name_function="fill_data_formulario")
                    time.sleep(2)
                    pass
                
                #load page 
                log.print_info("reload page idx={0}".format(idx), name_function="fill_data_formulario")
                fill_data_one_doc(one_document, one_sheet, driver)
                
                if load_doc_principal_y_asociados(one_document,driver):
                    time.sleep(3)
                else:
                    log.print_error("don't load doc principal y asociados", name_fuction="fill_data_formulario")
                #Guardar la resolución
                log.print_debug("click guardar resolucion ", name_function="fill_data_formulario")
                driver.implicitly_wait(10)
                btn_guardar = driver.find_elements_by_xpath("//*[@ng-click='vm.clickButton($event)']")
                btn_guardar[2].click()
                time.sleep(5)
                log.print_debug("click boton_back_to_new_resolucion", name_function="fill_data_formulario")
                driver.implicitly_wait(10)
                #driver.findElement(By.xpath("//*[@ng-click='goBack()']")).click();
                btn_back = driver.find_elements_by_xpath("//*[@ng-click='goBack()']")
                btn_back[0].click()
                log.print_debug("next document", name_function="fill_data_formulario", data_json={'idx':idx+1})
                time.sleep(5)
            idx = idx + 1
    log.print_info("return drive", name_function="fill_data_formulario")
    return drive
#######################################################################################
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.debug("| INI | {0} testing".format(__file__))
    load_page_crearresolucion()
    """
    list_sheets = ["Consejo Directivo","Presidencia","Gerencia General"]
    data_json = {
        "consejodirectivo":[],
        "presidencia": [],
        "gerenciageneral": [
            {
                "anio": 2019,
                "enlace": "https://www.osiptel.gob.pe/articulo/res0259-2019-gg",
                "materia": "NORMAS",
                "or": "GG",
                "resolucion": "N\u00b0 0259-2019-GG/OSIPTEL",
                "submateria": "NORMAS",
                "tema": "Ampliaci\u00f3n de Plazo para la remisi\u00f3n de comentarios al Proyecto de  Instructivo T\u00e9cnico para el cumplimiento de las Normas Complementarias para la Implementaci\u00f3n del Registro Nacional de Equipos Terminales M\u00f3viles para la Seguridad"
            },
            {
                "anio": 2019,
                "enlace": "https://www.osiptel.gob.pe/articulo/res0295-2019-gg",
                "materia": "SANCIONES Y MEDIDAS",
                "or": "GG",
                "resolucion": "N\u00b0 0295-2019-GG/OSIPTEL",
                "submateria": "SANCIONES Y MEDIDAS",
                "tema": "PAS - FIBERLUX S.A.C."
            }
        ]
    }
    url = "http://44.231.13.118/umbraco/#/content/content/edit/1200"
    
    driver_json = loadYMLtoJSON('driver_web.yml')
    executor_url = driver_json['executor_url']
    session_id = driver_json['session_id']
    #driver = attach_to_session(executor_url,session_id)
    driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    driver.session_id = session_id
    logging.debug("recovery_driver={0}".format(driver.session_id))
    print(driver.current_url)
    #driver.session_id = id_
    #objweb.get('http://ya.ru/')
    #rpt = fill_data_formulario(data_json, list_sheets)

    """

    logging.debug("| END | {0} testing".format(__file__))
    pass