# coding: utf-8
# Developer: Deiner Zapata Silva.
# Date: 10/06/2020
# Description: Ingresa user,pass y login to url.
#########################################################################################
import logging
import time
import pyautogui as gui
import pyperclip as pyc #pip install pyperclip
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from utils import *
from logging_advance import *

def build_driver_web(path_driver="D:\scraping\chromedriver.exe"):
    options = webdriver.ChromeOptions() 
    options.add_argument("--start-maximized")
    options.add_argument("--lang=es")
    options.add_argument("charset=UTF-8")
    driver = webdriver.Chrome(path_driver, options=options)
    return driver

def load_url(url, driver=build_driver_web()):
    driver.get (url)
    driver.implicitly_wait(10)
    driver_json ={
        "executor_url": driver.command_executor._url,
        "session_id": driver.session_id
    }
    save_yml(driver_json,nameFile="driver_web.yml")
    logging.info("session_id: {0} | url : {1}".format(driver_json['session_id'],driver_json['executor_url']))
    return driver

def input_string(string):
    time.sleep(1)
    pyc.copy(string)
    #pyc.waitForPaste(timeout=1)
    gui.keyDown('ctrl')
    gui.press('v')
    gui.keyUp('ctrl')
    time.sleep(1)

def load_credentials(user, pasw):
    driver.find_element_by_id("umb-username").send_keys(user)
    driver.find_element_by_id ("umb-passwordTwo").send_keys(pasw)
    driver.find_element_by_xpath("//button[@type='submit']").click()
    return True


if __name__ == "__main__":
    x = logging_advance(service=__file__, send_elk=False)
    x.print_debug("", data_json={}, name_function="__main__")
    url = "https://localhost:44347/umbraco/"
    user = "usuario@osiptel.com"
    pasw = "maQUEtaHTML567"
    rpt = load_url(url)
    load_credentials(user,pasw)
    while(True):
        pass
    x.print_debug("", data_json={}, name_function="__main__")
    pass