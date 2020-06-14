
# coding: utf-8
# Developer: Deiner Zapata Silva.
# Date: 10/06/2020
# Description: Ingresa user,pass y login to url.
#########################################################################################
import logging
import sys
import time
from utils_vision import *
from utils import *
from datamanager import *
from fill_data_formulario import *
from logging_advance import *
import pyautogui as gui
gui.FAILSAFE = True

while( True):
    load_page(filename="obj1.png", directory="D:/DPA/img",pos_xy=None, set_click=True, intentos=20,sleep_time=2,dy=0)
    time.sleep(4)
    load_page(filename="obj_02.png", directory="D:/DPA/img",pos_xy=None, set_click=True, intentos=20,sleep_time=2,dy=0)
    time.sleep(4)
    load_page(filename="obj_03.png", directory="D:/DPA/img",pos_xy=None, set_click=True, intentos=20,sleep_time=2,dy=0)
    time.sleep(4)
    load_page(filename="obj_04.png", directory="D:/DPA/img",pos_xy=None, set_click=True, intentos=20,sleep_time=2,dy=0)
    time.sleep(4)
    load_page(filename="obj_05.png", directory="D:/DPA/img",pos_xy=None, set_click=True, intentos=20,sleep_time=2,dy=0)
    time.sleep(10)
    time.sleep(4)
