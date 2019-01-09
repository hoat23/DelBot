#coding: utf-8
# pip install win32api
# pip install win32con
# pip install pyautogui -> OK (https://media.readthedocs.org/pdf/pyautogui/latest/pyautogui.pdf)
import cv2
import time
import pyautogui as py
from pynput.mouse import Button
from pynput.keyboard import Key
import pynput
##############################################################################################
mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()

class PlayMovUser():
    def executeActions(self,textActionsSaved):
        for textOneAction in textActionsSaved:
            self.executeOneAction(textOneAction)

    def extractAction(self,textOneAction):
        twoPoints = textOneAction.find('|')
        oneAction = ""
        if(twoPoints>0):
            oneAction= textOneAction[twoPoints+2:]
        return oneAction
    
    def extractPositionMouse(self,oneAction):
        x=""
        y=""
        coordAux = oneAction.find("(")
        if(coordAux>0):
            coordCom = oneAction.find(",")
            x = oneAction[coordAux+1:coordCom]
            coordAux = oneAction[coordCom+1:]
            coordAux2 = coordAux.find(")")
            y = coordAux[1:coordAux2]
            #print("("+x+" : "+y+")")
        return int(x), int(y)
    
    def executeOneAction(self,textOneAction):
        oneAction = self.extractAction(textOneAction)
        if(oneAction[0]=="K"): #Evento de teclado
            self.executeKeyboardAction(oneAction)
        if(oneAction[0]=="M"): #Evento de mouse
            self.executeMouseAction(oneAction)
    
    def executeKeyboardAction(self,oneAction):
        action = oneAction[1]
        command= oneAction[2]

        if(len(command)==1):
            pushKey = command
        else:
            if(command=="alt"):
                pushKey = Key.alt
            if(command=="alt_l"):
                pushKey = Key.alt_l
            if(command=="alt_r"):
                pushKey = Key.alt_r
            if(command=="alt_gr"):
                pushKey = Key.alt_gr
            if(command=="backspace"):
                pushKey = Key.backspace
            if(command=="caps_lock"):
                pushKey = Key.caps_lock
            if(command=="cmd"):
                pushKey = Key.cmd
            if(command=="cmd_l"):
                pushKey = Key.cmd_l
            if(command=="cmd_r"):
                pushKey = Key.cmd_r
            if(command=="ctrl"):
                pushKey = Key.ctrl
            if(command=="ctrl_l"):
                pushKey = Key.ctrl_l
            if(command=="ctrl_r"):
                pushKey = Key.ctrl_r
            if(command=="delete"):
                pushKey = Key.delete
            if(command=="down"):
                pushKey = Key.down
            if(command=="end"):
                pushKey = Key.end
            if(command=="enter"):
                pushKey = Key.enter
            if(command=="esc"):
                pushKey = Key.esc
            if(command=="f1"):
                pushKey = Key.f1
            if(command=="f2"):
                pushKey = Key.f2
            if(command=="f3"):
                pushKey = Key.f3
            if(command=="f4"):
                pushKey = Key.f4
            if(command=="f5"):
                pushKey = Key.f5
            if(command=="f6"):
                pushKey = Key.f6
            if(command=="f7"):
                pushKey = Key.f7
            if(command=="f8"):
                pushKey = Key.f8
            if(command=="f9"):
                pushKey = Key.f9
            if(command=="f10"):
                pushKey = Key.f10
            if(command=="f11"):
                pushKey = Key.f11
            if(command=="f12"):
                pushKey = Key.f12
            if(command=="f13"):
                pushKey = Key.f13
            if(command=="f14"):
                pushKey = Key.f14
            if(command=="f15"):
                pushKey = Key.f15
            if(command=="f16"):
                pushKey = Key.f16
            if(command=="f17"):
                pushKey = Key.f17
            if(command=="f18"):
                pushKey = Key.f18
            if(command=="f19"):
                pushKey = Key.f19
            if(command=="f20"):
                pushKey = Key.f20
            if(command=="home"):
                pushKey = Key.home
            if(command=="left"):
                pushKey = Key.left
            if(command=="page_down"):
                pushKey = Key.page_down
            if(command=="page_up"):
                pushKey = Key.page_up
            if(command=="right"):
                pushKey = Key.right
            if(command=="shift"):
                pushKey = Key.shift
            if(command=="shift_l"):
                pushKey = Key.shift_l
            if(command=="shift_r"):
                pushKey = Key.shift_r
            if(command=="space"):
                pushKey = Key.space
            if(command=="tab"):
                pushKey = Key.tab
            if(command=="up"):
                pushKey = Key.up
            #--------------------------------
            if(command=="insert"):
                pushKey = Key.insert
            if(command=="menu"):
                pushKey = Key.menu
            if(command=="num_lock"):
                pushKey = Key.num_lock
            if(command=="pause"):
                pushKey = Key.pause
            if(command=="print_screen"):
                pushKey = Key.print_screen
            if(command=="scroll_lock"):
                pushKey = Key.scroll_lock

        if(action=="U"):
            keyboard.release(pushKey)
        if(action=="D"):
            keyboard.press(pushKey)
        return

    def executeMouseAction(self,oneAction):
        actionButton = oneAction[1]
        command = oneAction[2]
        pX ,pY = self.extractPositionMouse(oneAction)
        #print("posicion ("+str(pX)+":"+ str(pY)+")")
        #mouse.move(pX , pY)
        py.moveTo(pX,pY,0)
        if(actionButton=="R"):
            #print("Button.right")
            push = 'right'
            #push = Button.right
        if(actionButton=="M"):
            #print("Button.middle")
            push = 'middle'
            #push = Button.middle
        if(actionButton=="L"):
            #print("Button.left")
            push = 'left'
            #push = Button.left
        
        if(command=="U"):
                #print("Up")
                #mouse.release(push)
                py.mouseUp(x=pX, y=pY, button=push)
        if(command=="D"):
                #print("Down")
                #mouse.press(push)
                py.mouseDown(x=pX, y=pY, button=push)
        return


"""
width,height = py.size()
print("width (%d , %d)" % (width , height) )
img = py.screenshot()
print(img)
#py.screenshot('./Delbot/screenshot.png')
x_y = py.locateOnScreen('./Delbot/img2search.png')
print("Coordenadas  img:"+str(x_y))
x_y = py.locateCenterOnScreen('./Delbot/img2search.png')    
print("Coord center img:"+str(x_y))

for i in py.locateAllOnScreen('./Delbot/img2search.png'):
    print("Coord bucle :"+str(i))
##############################################################################################
print("move mouse to (100,100)")
py.moveTo(200,100,0)
print("mouse movido")
##############################################################################################
print("Rastreo de coordenadas")
for i in range(0,100):
    x,y = py.position()
    print(" x =" + str(x) + ", y =" + str(y) )
    time.sleep(0.01)
#----------------------------------------------------------
"""

