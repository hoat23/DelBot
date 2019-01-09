#coding: utf-8

#pip install pyttsx -> ok - no funciona - falta engine
#pip install engine -> errors

#pip install pypiwin32

#coding:utf-8
# pip install pyttsx3
# Autor: Deiner Zapata Silva

import os
import sys
import pyttsx3

class VoiceBot():
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('volume',1.0)
        self.engine.setProperty('rate',320)
        self.engine.setProperty('voice','spanish')
        self.activo = True

    def enable(self, activo):
        if(activo):
            self.activo=activo
        else:
            self.activo=False

    def speak(self, texto):
        try:
            if(self.activo):
                self.engine.say(texto)
                self.engine.runAndWait()
        except Exception:
            print("ERROR: VoiceBot::speak() ")
            e = sys.exc_info()[1]
            print(e.args[0])

    def readFileTXT(self, nameFileTXT):
        fullText = open(nameFileTXT)
        self.speak("Leyendo archivo ["+nameFileTXT+"]")
        for linea in fullText.readlines():
            linea = linea[:-1]
            self.speak(linea)

#voiceDelBot  = VoiceBot()
#voiceDelBot.speak("Hola soy delbot")