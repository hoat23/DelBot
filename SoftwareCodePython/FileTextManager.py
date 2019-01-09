#coding: utf-8
#Developer: Deiner Zapata Silva
import sys
from pathlib import Path

##########################################################################################################
fileTxt = None

class FileTextManager():
    def __new__(cls):
        #Si no existe el atributo "instanciar"
        if not hasattr(cls, 'instance'):
            #Lo creamos
            cls.instance = super(FileTextManager, cls).__new__(cls)
        return cls.instance

    def open(self,nameFile,forze=False):
        global fileTxt
        my_file = Path(nameFile)
        if(fileTxt==None or forze):
            if not my_file.is_file():
                a= open(nameFile,"w")
                a.close()
            fileTxt = open(nameFile,'r+')

    def close(self):
        global fileTxt
        try:
            fileTxt.close()
        except Exception:
            print("ERROR: searchDiff ")
            e = sys.exc_info()[1]
            print(e.args[0])

    def write(self,lineTxt):
        global fileTxt
        self.open("logTxt.txt")
        fileTxt.write(lineTxt)

    def writeln(self,newLineTxt):
        global fileTxt
        self.open("logTxt.txt")
        fileTxt.write(newLineTxt+'\n')
        return

    def read(self):
        global fileTxt
        self.open("logTxt.txt",forze=True)
        lineas = fileTxt.readlines()
        return lineas