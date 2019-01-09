# Coding: utf-8
# Developer: Deiner Zapata Silva

#Detectar diferencias entre dos imágenes con OpenCV 
#https://robologs.net/2016/04/21/detectar-diferencias-entre-dos-imagenes-con-opencv-y-python/

import cv2
import sys
class ChangesInImages():
    def __init__(self,dirImg1='cap1.png',dirImg2='cap2.png',showChanges='yes'):
        self.dirImg1 = dirImg1
        self.dirImg2 = dirImg2
        self.img1 = []
        self.img2 = []
        self.imgShowChanges = []
        self.showChanges = showChanges
    
    def openImages(self):
        try:
            self.img1 = cv2.imread(self.dirImg1)
            self.img2 = cv2.imread(self.dirImg2)
        except Exception:
            print("ERROR: Can't reading images...")
            e = sys.exc_info()[1]
            print(e.args[0])
    
    def searchDiff(self):
        try:
            diff_in_images = cv2.absdiff(self.img1,self.img2)

            imagen_gris = cv2.cvtColor(diff_in_images, cv2.COLOR_BGR2GRAY)#Convertimos la imagen a gris
            _, contours, _ = cv2.findContours(imagen_gris, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            self.imgShowChanges = self.img2
            #Showing every one of the bourder
            for c in contours:
                if cv2.contourArea(c) >= 20:
                    posicion_x,posicion_y,ancho,alto = cv2.boundingRect(c) #Guardamos las dimensiones de la Bounding Box
                    cv2.rectangle(self.imgShowChanges,(posicion_x,posicion_y),(posicion_x+ancho,posicion_y+alto),(0,0,255),2) #Dibujamos la bounding box sobre diff1
        except Exception:
            print("ERROR: searchDiff ")
            e = sys.exc_info()[1]
            print(e.args[0])

    def showDiffImg(self):
        try:
            while(self.showChanges=='yes'):
                #Mostramos las imagenes. ESC para salir.
                #cv2.imshow('Imagen1', self.img1)
                cv2.imshow('Imagen with changes detected', self.imgShowChanges)
                #cv2.imshow('Diferencias detectadas', diff_in_images)
                tecla = cv2.waitKey(5) & 0xFF
                if tecla == 27:
                    break
            cv2.destroyAllWindows()
        except Exception:
            print("ERROR: showDiffImg")
            e = sys.exc_info()[1]
            print(e.args[0])
    
    def saveDiffImg(self):
        try:
            print("save diff")
        except Exception:
            print()

    def run(self):
        try:
            print("Iniciando <run> ChangeInImage()...")
            self.openImages()
            self.searchDiff()
            self.showDiffImg()
        except Exception:
            print("ERROR: testAlgortihm ")
            e = sys.exc_info()[1]
            print(e.args[0])

######################################################################################################################
"""
alg = ChangesInImages('cap1.png','cap2.png')
alg.run()
"""
