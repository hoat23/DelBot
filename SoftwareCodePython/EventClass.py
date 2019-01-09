# Developer: Deiner Zapata Silva
#pip install pyscreenshot

import threading as th
from time import sleep
import pyscreenshot as pyss
from PIL import ImageChops
import ChangesInImages as cim
import CatchEventUser as ceu

stopWDS = False

def generateName(nameScreen): #screen_XXXX.png
    posGuion = nameScreen.find("_")
    posDot = nameScreen.find(".")
    strNum = nameScreen[posGuion+1:posDot]
    contNum = int(strNum) + 1 
    newName = "screen_"+str(contNum)+".png"
    print(newName)
    return newName

def msleep(delay):
    sleep( (delay * 1.0) / 1000.0 )
    return
#######################################################################################################
class EventClass():
    def __init__(self):
        self.tWDU = None
        self.tWDS = None
    @staticmethod
    def playMovUser():
        print("PlayMovUser....")
        obj=ceu.CatchEventUser()
        obj.playMov()

    @staticmethod
    def WatchDogUser():
        print("WatchDogUser....")
        obj=ceu.CatchEventUser()
        obj.recordMov()
        return

    @staticmethod
    def WatchDogScreen():
        #https://stackoverflow.com/questions/20580785/python-how-to-detect-any-changes-in-the-screen
        print("WatchDogScreen....")
        global stopWDS
        nameScreen = "screen_0000.png"
        while(not stopWDS): #for i in range(0,2):
            msleep(230)
            imgOld = pyss.grab()
            #nameScreen = generateName(nameScreen)
            #pyss.grab_to_file(nameScreen)#"ss_old.png"
            while(True and not stopWDS):
                msleep(2)
                imgNew = pyss.grab()
                diff = ImageChops.difference(imgNew, imgOld)
                bbox = diff.getbbox()
                if bbox is not None:
                    break
            # Diferencia encontrada 
            nameScreen = generateName(nameScreen)
            pyss.grab_to_file(nameScreen)#"ss_new.png"
            #alg = cim.ChangesInImages("ss_old.png","ss_new.png","no") # "no" -> no muestra imgen con cambios
            #alg.run()
        
        return
    
    def runWatchDogUser(self):
        e = EventClass()
        self.tWDU = th.Thread(target=e.WatchDogUser)
        self.tWDU.start()

    def runWatchDogScreen(self):
        e = EventClass()
        self.tWDS = th.Thread(target=e.WatchDogScreen)
        self.tWDS.start()
    
    def stopWatchDogUser(self):
        print("falta detener stopwatchdoguser.....")
        obj=ceu.CatchEventUser()
        obj.stopCatchEvent()

    def stopWatchDogScreen(self):
        print("Deteniendo hilo watchdogscreen...")
        global stopWDS
        stopWDS = True

#######################################################################################################    
def run():
    threads = list()
    e = EventClass()
    t = th.Thread(target=e.WatchDogUser)
    t.start()
    threads.append(t)
    t = th.Thread(target=e.WatchDogScreen) #, args=(i,)) 
    threads.append(t)
    t.start()
    print("EventClass:Launched . . . [WatchDogUser , WatchDogScreen]")
#######################################################################################################

#run()