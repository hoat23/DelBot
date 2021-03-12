#coding: UTF-8 
#########################################################################################
# Developer: Deiner Zapata Silva.
# Date: 09/06/2020
# Last update: 09/06/2022
# Description: Codigo util, para leer y cargar datos
# sys.setdefaultencoding('utf-8') #reload(sys)
# pip install pycryptodome
# https://www.pyimagesearch.com/2018/08/20/opencv-text-detection-east-text-detector/
# pip install --upgrade imutils
#########################################################################################
import time
from imutils.object_detection import non_max_suppression
import numpy as np 
import cv2
import argparse
import os
import io
from mss.windows import MSS as mss
import logging
import pyautogui as gui
import pyperclip as pyc #pip install pyperclip
import unicodedata

def load_page(filename="img_to_search.png", directory="D:/DPA/img",pos_xy=None, set_click=False, intentos=20,sleep_time=3.2,dy=0):
    #logging.debug("load_page | {0}".format(filename))
    fullpath = "{0}/{1}".format(directory, filename)
    cont = 0
    pos_box = None 
    while ((pos_box==None) and (cont < intentos)):
        time.sleep(sleep_time)
        pos_box = gui.locateOnScreen(fullpath, confidence=0.8, grayscale=True)
        logging.debug("search_buton  | {0} | {1}".format(filename, pos_box))
        cont = cont + 1
    try:
        logging.debug("buton_found     | {0} | {1}".format(filename, pos_box))
        pos_xy = gui.center(pos_box)
        try:
           gui.dragTo(pos_xy.x, pox_xy.y + dy)
        except:
            pass
        if set_click and pos_xy!=None:
            logging.info("click_on_button  | {0} | {1}".format(filename, pos_xy))
            gui.click(pos_xy.x, pos_xy.y + dy)
        else:
            logging.error("click_on_button | pos_xy=None |")
        time.sleep(1)
        return True
    except:
        logging.error("buton_not_found  | {0}".format(filename))
        return False

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)
    logging.debug("| INI | {0} testing".format(__file__))
    load_page()
    logging.debug("| END | {1} testing".format(__file__))
    pass
