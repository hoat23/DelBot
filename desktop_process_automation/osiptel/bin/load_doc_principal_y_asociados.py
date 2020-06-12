# coding: utf-8
# Developer: Deiner Zapata Silva.
# Date: 10/06/2020
# Description: Ingresa user,pass y login to url.
#########################################################################################
import logging
import time
import pyautogui as gui
import pyperclip as pyc #pip install pyperclip
import unicodedata
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from utils import *
from utils_vision import *
from subir_file import *

def load_page_load_documento_principal(filename="win_doc_principal.png", directory="D:/DPA/img", pos_xy=None): #D://DPA//bin//
    """
    Carga pagina usando driver
    """
    gui.scroll(1000)
    if load_page(filename=filename, directory=directory,pos_xy=None, set_click=True, intentos=5):#valida que la pagina ya cargo
        return True
    return False

def load_page_seleccionar_medio(filename="boton_selecciona_medio.png", directory="D:/DPA/img", pos_xy=None):
    gui.scroll(-1000)
    #time.sleep(1)
    if load_page(filename=filename, directory=directory,pos_xy=pos_xy, set_click=True, intentos=5):#valida que la pagina ya cargo
        return True
    return False

def load_page_goto(path_media, intentos=3, directory="D:/DPA/img"):

    for intento in range(0,intentos):
        if load_page(filename=path_media[-1], directory=directory, sleep_time=1, set_click=True, intentos=2):
            logging.info("load_page_goto | Its ok. [{0}]".format(filename))
            return True

        #Where i am
        iam_idx = -1
        lvl = 0
        for filename in path_media:
            gui.scroll(1000)# el directorio se indica en la parte superior de la ventana
            if load_page(filename=filename, directory=directory, sleep_time=1, set_click=True, intentos=2):
                iam_idx = lvl
                logging.info("load_page_goto | lvl={0}:{2} | {1}".format(iam_idx, filename, lvl))
                break
            lvl = lvl + 1
        
        time.sleep(5)
        if iam_idx!=-1:
            if iam_idx== 0: #win_media.png 
                print("esperandooooooooo.......")
                time.sleep(15)
                logging.info("load_page_repositorio_documentos")
                gui.scroll(1000)#empezamos busqueda progresiva desde arriba
                print("goto repositorio documentos ...")
                for intento in range(0,10):
                    gui.scroll(-100)
                    if load_page(filename="boton_repositorio_de_docum.png", sleep_time=1, set_click=True, intentos=2):#valida que la pagina ya cargo
                        break
            
            if iam_idx==1: #win_media_repositorio_de_documentos:
                logging.info("load_page_buscador_de_normas.png")
                gui.scroll(1000)#empezamos busqueda progresiva desde arriba
                for intento in range(0,10):
                    gui.scroll(-100)
                    if load_page(filename="boton_buscador_de_normas_y.png", sleep_time=1, set_click=True, intentos=2):#valida que la pagina ya cargo
                        break
    return False

def load_documento_principal(doc_principal, directory_doc_principal):
    if load_page_seleccionar_medio():
        path_media = [
            "win_media.png",
            "win_media_repositorio_de_documentos.png",
            "win_media_repositorio_de_documentos_buscador_de_normas.png"]
        
        if load_page_goto(path_media):
            if load_page(filename="boton_subir.png", set_click=True):
                subir_file(doc_principal, directory_doc_principal)
                logging.info("load_documento_principal [{0}]".format(doc_principal))
                cont = 0
                while cont<100:
                    time.sleep(1)
                    if load_page(filename="boton_seleccionar.png", set_click=True, sleep_time=2, intentos=5):
                        pass
                    if load_page(filename="boton_aceptar.png", set_click=True, sleep_time=2, intentos=5):
                        return True
                    cont = cont + 1
                return False
    return False

def load_documento_asociado(doc_asociado):
    directory = "D:/scraping/book20/CD/1"
    namefile = "res00194CDOSIPTEL.pdf"
    input("load_documento_asociado {0}".format(doc_asociado))
    #subir_file(namefile, directory)
    return True

def valida_path(path_directory_idx, one_document):
    #subir_file(namefile, directory)
    tree_files = get_files_in_directory(path_directory_idx, recursive=True, print_tree=False)
    if 'files' in tree_files:
        files_principal = tree_files['files']

    if 'subdir' in tree_files:
        files_asociados = tree_files['subdir']['files']
    else:
        files_asociados = []
    doc_principal = ""
    for file in files_principal:
        if file.find('.pdf'):
            doc_principal = file
    
    doc_asociados=[]
    for file in files_asociados:
        if file.find('.pdf'):
            doc_asociados.append(file)
    print("-----------------------------------------------------------")
    print_json(tree_files)
    print_json(one_document)
    print("-----------------------------------------------------------")
    return doc_principal, doc_asociados

def load_doc_principal_y_asociados(one_document, idx, one_sheet, directory="D:/scraping/book20"):
    logging.debug("load_doc_principal_y_asociados | {0}".format(one_document['enlace']))
    if idx<1: idx=1
    sub_directory =  unicodedata.normalize( 'NFD', one_document['or'] )
    path_directory_idx = "{0}/{1}/{2}".format(directory, sub_directory, idx)
    doc_principal,  doc_asociados = valida_path(path_directory_idx, one_document)#queda pendiente validar one_document

    intentos_load_page = 3
    for n_intento in range(0,intentos_load_page):
        if load_page_load_documento_principal() and len(doc_principal)>0:
            load_documento_principal(doc_principal, path_directory_idx)
            for one_doc_asociado in doc_asociados:
                load_documento_asociado(one_doc_asociado)
            #load_page(filename="boton_guardarypublicar.png", set_click=True, sleep_time=2.3, intentos=20)
            return True
        else:
            input("load_doc_principal_y_asociados ... error")
    return False

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)
    logging.debug("| INI | {0} testing".format(__file__))
    # Variables para testing
    one_doc = {
        "anio": 2019,
        "enlace": "https://www.osiptel.gob.pe/articulo/res0259-2019-gg",
        "materia": "NORMAS",
        "or": "GG",
        "resolucion": "N\u00b0 0259-2019-GG/OSIPTEL",
        "submateria": "NORMAS",
        "tema": "Ampliaci\u00f3n de Plazo para la remisi\u00f3n de comentarios al Proyecto de  Instructivo T\u00e9cnico para el cumplimiento de las Normas Complementarias para la Implementaci\u00f3n del Registro Nacional de Equipos Terminales M\u00f3viles para la Seguridad"
    }
    idx = 1
    one_sheet = "Gerencia General" # 3 tipos = ["Consejo Directivo","Presidencia","Gerencia General"]
    
    load_doc_principal_y_asociados(one_doc, idx, one_sheet)
    
    logging.debug("| END | {0} testing".format(__file__))
