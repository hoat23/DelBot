#coding: utf-8
#Developer: Deiner Zapata Silva
#https://recursospython.com/codigos-de-fuente/grabador-teclado-mouse/
#http://nitratine.pythonanywhere.com/youtube/python-hotkeys
#http://recursospython.com/guias-y-manuales/autopy-toolkit/

#pip install autopy
#pip install pynput


from pynput.keyboard import Key, Listener 
from pynput import mouse
from pynput import keyboard
import logging, time
import FileTextManager as ftm
from datetime import datetime
import PlayMovUser as pmu

# LOGGING --------------------------------------------------------------
# Level of logging: 
#   1 -> DEBUG   : Detailed information, typically of interest only when diagnostigs problems.
#   2 -> INFO    : Confirmation that things are working as expected
#   3 -> WARNING : An indication that somtehin unexpected happened. Indicate problems in the near future.
#   4 -> ERROR   : Due to a more serious problem, the software has not been able to perform some function.
#   5 -> CRITICAL: A serious error, indicating that the program itself may be uneble to continue running.
# CONFIGURANDO LOGGER-----------------------------------------------------
"""
formater = '%(asctime)s :%(message)s'
logging.basicConfig(level=logging.DEBUG,#filename="keylogger.log",
                    format=formater) #LogRecord attributes
logger = logging.getLogger(__name__)
print("init_logging() "+str(logger)+" - [level=DEBUG]")
logging.debug("LOGGING INICIALIZADO")
"""
def extract_description(key):
    only_key = str(key)
    punto = only_key.find(".")
    if(punto>0):
        only_key = only_key[punto+1:]
    
    if(only_key[0]=="'" and only_key[len(only_key)-1]=="'"):
        only_key = only_key[1:len(only_key)-1]
    
    if(only_key=="right"):
        only_key = "R"
    if(only_key=="middle"):
        only_key = "M"
    if(only_key=="left"):
        only_key = "L"
    
    return only_key

logText = ftm.FileTextManager()
enableCatchEvent = True

class CatchEventUser():
    @staticmethod
    def stopCatchEvent():
        global enableCatchEvent
        enableCatchEvent=False

    # KEYBOARD -------------------------------------------------------------
    #defining function to print when key is pressed
    @staticmethod
    def on_press(key):
        newKey = extract_description(key)
        asctime = datetime.now() 
        text =  str('{0} | KD{1}'.format(asctime, newKey))
        print(text)
        logText.writeln( text )

    #defining function to print when key is released 
    
    @staticmethod
    def on_release(key):
        global lastKey, enableCatchEvent
        newKey = extract_description(key)
        asctime = datetime.now() 
        text = str('{0} | KU{1}'.format(asctime, newKey))
        print(text)
        logText.writeln( text )
        lastKey = newKey
        if key == Key.esc or enableCatchEvent:
            # Stop listener 
            return False 
    # MOUSE ---------------------------------------------------------------
    """
    def on_move(x, y):
        logText = ftm.FileTextManager()
        logText.writeln("Pointer moved to {0}".format((x,y)))
    """
    
    @staticmethod
    def on_click(x, y, button, pressed):
        button = extract_description(button)
        asctime = datetime.now()
        text = str('{0} | M{1}{2}{3}'.format( asctime, button , ('D' if pressed else 'U') , (x,y)))
        print(text)
        logText.writeln( text )

    @staticmethod
    def on_scroll(x, y, dx, dy):
        asctime = datetime.now()
        text = str('{1} | MS{2}{3}'.format(asctime, 'D' if dy < 0 else 'U', (x,y)))
        print(text)
        logText.writeln( text )

    # COLLECT ALL EVENT OF--------------------------------------------------------
    @staticmethod
    def recordMov():
        ceu = CatchEventUser()
        with mouse.Listener(on_click=ceu.on_click, on_scroll=ceu.on_scroll) or Listener(on_press=ceu.on_press, on_release=ceu.on_release) as listener: #on_move=ceu.on_move, 
            #listener.join()
            with keyboard.Listener(on_press=ceu.on_press, on_release=ceu.on_release) as listener:
                listener.join()
    # REPLAY ALL OF USER DID------------------------------------------------------
    @staticmethod
    def playMov():
        try:
            print("closing file...")
            logText.close()
        finally:
            logText.open("logTxt.txt")
            lineas = logText.read()
            user = pmu.PlayMovUser()
            user.executeActions(lineas)
###############################################################################

#ceu = CatchEventUser()
#ceu.recordMov()
#ceu.playMovSaved()

