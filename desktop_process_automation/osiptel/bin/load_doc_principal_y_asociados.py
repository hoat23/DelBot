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
import io
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from utils import *
from utils_vision import *
from subir_file import *
from logging_advance import *
#######################################################################################
log = logging_advance(_index="debug-python", service='fill_data_formulario.py', send_elk=True)

x = logging_advance(service=__file__, send_elk=False)

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
            logging.info("load_page_goto | Its ok. [{0}]".format(path_media[-1]))
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

def load_documento_principal(doc_principal, directory_doc_principal, driver):
    #if load_page_seleccionar_medio():
    # Existen 3 rutas posibles
    
    agregar_documentos = driver.find_elements_by_xpath("//*[@ng-click='switchToMediaPicker()']")
    agregar_documentos[0].click() #click boton [Selecciona medio]
    
    path_media = [
        "win_media.png",
        "win_media_repositorio_de_documentos.png",
        "win_media_repositorio_de_documentos_buscador_de_normas.png"]
    
    if load_page_goto(path_media):
        if load_page(filename="boton_subir.png", set_click=True):
            # Subiendo documento principal
            subir_file(doc_principal, directory_doc_principal)
            log.print_error("documento principal subido", name_function=__name__)
            # ng-click="vm.clickButton($event)"
            
            cont=0
            while cont<100:
                time.sleep(1)

                if load_page(filename="boton_aceptar.png", set_click=True, sleep_time=2, intentos=5):
                    time.sleep(1)
                    log.print_info("return True", name_function=__name__)
                    return True
                
                if load_page(filename="boton_seleccionar.png", set_click=True, sleep_time=2, intentos=5):
                    time.sleep(1)
                    pass
                cont = cont + 1
            log.print_info("return False", name_function=__name__)
            return False
    log.print_info("return False", name_function=__name__)
    return False

def load_documento_asociado(doc_asociado_json,driver):
    doc_asociado = doc_asociado_json["doc_asociado"]
    rename_doc = doc_asociado_json["rename"]
    directory_doc = doc_asociado_json["directory"]

    agregar_documentos = driver.find_elements_by_xpath("//*[@ng-click='switchToMediaPicker()']")
    agregar_documentos[0].click() #click boton [Selecciona medio]
    driver.execute_script("document.getElementsByTagName('input')[13].value='"+rename_doc+"'")
    
    path_media = [
        "win_media.png",
        "win_media_repositorio_de_documentos.png",
        "win_media_repositorio_de_documentos_buscador_de_normas.png"]
    
    if load_page_goto(path_media):
        if load_page(filename="boton_subir.png", set_click=True):
            # Subiendo documento principal
            subir_file(doc_asociado, directory_doc)
            log.print_info("documento asociado [{0}]".format(doc_asociado), name_function=__name__)
            # ng-click="vm.clickButton($event)"
            
            cont=0
            while cont<100:
                time.sleep(1)
                if load_page(filename="boton_aceptar.png", set_click=False, sleep_time=1, intentos=5):
                    driver.find_elements_by_xpath("//input[@placeholder='Escribe un nombre...']")[2].send_keys('\b\b'*len(rename_doc)+rename_doc)
                    load_page(filename="boton_aceptar.png", set_click=True, sleep_time=2, intentos=3)
                    log.print_info("return True", name_function=__name__)
                    return True
                
                if load_page(filename="boton_seleccionar.png", set_click=True, sleep_time=2, intentos=5):
                    time.sleep(1)
                    log.print_debug("boton_seleccionar", name_function=__name__)
                    pass
                cont = cont + 1
            log.print_info("return False", name_function=__name__)
            return False
    log.print_info("return False", name_function=__name__)
    return False

def get_name_doc_asociado(filename, path_dir):
    filepath="{0}/{1}".format(path_dir, filename)
    name = ""
    with open(filepath) as fp:
            name = fp.readline()
    try:
        with open(filepath) as fp:
            name = fp.readline()
    except:
        log.print_error("filepath=[{0}]".format(filename), name_function=__name__)
    finally:
        fp.close()
    log.print_debug("return [{0}]".format(name), name_function=__name__)
    return name

def valida_path(path_directory_idx, one_document):
    #subir_file(namefile, directory)
    tree_files = get_files_in_directory(path_directory_idx, recursive=True, print_tree=False)
    #print_json(tree_files)
    if 'files' in tree_files:
        files_principal = tree_files['files']

    if 'subdir' in tree_files:
        files_asociados = tree_files['subdir']['files']
        path_dir = tree_files['subdir']['path']
    else:
        files_asociados = []
    doc_principal = ""
    for file in files_principal:
        if file.find('.pdf')>=0:
            doc_principal = file
    
    doc_asociados=[]
    for file in files_asociados:
        if file.find('.pdf')>=0:
            filename = file[:file.find('.pdf')]+".txt"
            name_doc_asociado = get_name_doc_asociado(filename, path_dir)
            doc_asociados.append({"doc_asociado": file, "rename": name_doc_asociado, "directory": path_dir})
    one_document.update({'doc_principal': doc_principal, 'doc_asociados': doc_asociados, 'tree_files': tree_files})
    return one_document

def load_doc_principal_y_asociados(one_document, driver, directory="D:/scraping/book20"):
    log.print_info("enlace={0}".format(one_document['enlace']), name_function=__name__)
    idx = one_document['idx']
    one_sheet = one_document['sheet']
    sub_directory =  unicodedata.normalize( 'NFD', one_document['or'] )
    path_directory_princ = "{0}/{1}/{2}".format(directory, sub_directory, idx+1)
    one_document = valida_path(path_directory_princ, one_document)#queda pendiente validar one_document dentro de valida path
    log.print_debug("one_document", data_json=one_document, name_function=__name__)

    agregar_documentos = driver.find_elements_by_xpath("//*[@ng-click='openLinkPicker()']")
    flagDocPric = False
    if len(one_document['doc_principal'])>0:
        # click en (anadir) para cargar nuevo documento principal
        agregar_documentos[0].click()
        flagDocPric=load_documento_principal(one_document['doc_principal'], path_directory_princ, driver)
    
    
    for one_doc_asociado in one_document['doc_asociados']:
        # click en (anadir) para cargar documento asociado
        agregar_documentos[1].click()
        load_documento_asociado(one_doc_asociado, driver)
    #load_page(filename="boton_guardarypublicar.png", set_click=True, sleep_time=2.3, intentos=20)
    if not flagDocPric:
        save_yml(one_document, nameFile="documents_error.yml", type_open="a")
        log.print_error("one_document", data_json=one_document, name_function=__name__)
    log.print_info("return {0}".format(flagDocPric), name_function=__name__)
    return flagDocPric

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
