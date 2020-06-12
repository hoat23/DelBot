# coding: utf-8
# Developer: Deiner Zapata Silva.
# Date: 10/06/2020
# Description: Codigo para cargar archivos de forma grafica
#########################################################################################
import logging
import time
import pyautogui as gui
import pyperclip as pyc #pip install pyperclip
import unicodedata
from utils import *
from utils_vision import *
from os import walk
#########################################################################################
def subir_file(filename, directory):
    if load_page(filename="win_subir_file.png", directory="D:/DPA/img",pos_xy=None, set_click=True, intentos=3,sleep_time=2):
        logging.info("subir_file | {0}".format(filename))
        input_string_pyc(directory)
        gui.press('enter')
        if load_page(filename="input_filename.png", directory="D:/DPA/img",pos_xy=None, set_click=True, intentos=3,sleep_time=2):
            input_string_pyc(filename)
            gui.press('enter')
            logging.debug("subir_file | OK | {0}".format(filename))
            return True
    logging.error("subir_file | {0} | {1}".format(directory, filename))
    return False
        
def input_string_pyc(string):
    time.sleep(1)
    pyc.copy(string)
    #pyc.waitForPaste(timeout=1)
    gui.keyDown('ctrl')
    gui.press('v')
    gui.keyUp('ctrl')
    time.sleep(1)
    return

def get_files_in_directory(path_to_directory, recursive=False, print_tree=False):
    """
    obtiene archivos dentro de la ruta especificada (No es recursivo por defecto).
    """
    dir, subdirs, files = next(walk(path_to_directory))
    tree_files = {
        'path': dir,
        'files': files
    }
    if recursive:
        for sub_dir in subdirs:
            print("sub_dir {0}".format(sub_dir))
            path_subdir = "{0}/{1}".format(path_to_directory, sub_dir)
            tree_subdirs = get_files_in_directory(path_subdir, recursive=True, print_tree=False)
            tree_subdirs.update({'dir': sub_dir})
            tree_files.update( {'subdir': tree_subdirs})
    else:
        tree_files.update( {'subdirs': subdirs} )

    if print_tree: print_json(tree_files)
    return tree_files

#########################################################################################
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)
    logging.debug("| INI | {0} testing".format(__file__))
    directory = "D:/scraping/book20/CD/1"
    namefile = "res00194CDOSIPTEL.pdf"
    #subir_file(namefile, directory)
    get_files_in_directory(directory, recursive=True, print_tree=True)
    #detect_text()
    logging.debug("| END | {0} testing".format(__file__))
    pass
