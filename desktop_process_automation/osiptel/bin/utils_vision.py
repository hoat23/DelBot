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

def get_text_boxes( imagePath="fullscreen.png", 
                    east = "frozen_east_text_detection.pb",
                    newH = 576,
                    newW = 1024,
                    min_confidence=0.5 ):
    # image  -> path to our input image
    # east   -> EAST scene text detector model file path
    # newH -> Resized image height - must be multiple of 32 - default=320*3
    # newW -> Resized image weight - must be multiple of 32 - default=320*5
    # min_confidence-> probability threshold to determine text - default=0.5
    
    image = cv2.imread(imagePath) # it is working variable
    orig = image.copy()
    (H,W) = image.shape[:2]
    print("INFO | get_text_boxes | {0}x{1}".format(H,W))
    rW = W / float(newW)
    rH = H / float(newH)
    image = cv2.resize(image, (newW, newH))
    (H,W) = image.shape[:2]
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid", # FIRST LAYER : output probabilities of a region containing text or not.
        "feature_fusion/concat_3"        # SECOND LAYER: bounding box coordinates of text.
    ]
    net = cv2.dnn.readNet( east )
    blob = cv2.dnn.blobFromImage(
        image , 1.0 , (W,H) , (123.68, 116.78, 103.94) , swapRB=True, crop=False 
        )
    start = time.time()
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)
    end = time.time()
    print("INFO | get_text_boxes | {:.6f} seconds".format(end-start))
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []
    for y in range(0,numRows):
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]
        for x in range(0, numCols):
            if (scoresData[x] < min_confidence):
                continue
            (offsetX, offsetY) = (x * 4.0 , y * 4.0)
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]) )
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]) )
            startX = int(endX - w)
            startY = int(endY - h)
            rects.append(  (startX, startY, endX, endY)  )
            confidences.append(  scoresData[x]  )

    boxes = non_max_suppression(np.array(rects) , probs=confidences)
    for (startX, startY, endX, endY) in boxes:
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY *rH)
        print("{0}\t{1}".format(startX,startY))
        print("{0}\t{1}".format(endX,endY))
        cv2.rectangle( orig , (startX,startY) , (endX,endY) , (0,255,0) , 2 )
    cv2.imshow("Text detection",orig)
    print("Press <ESC> to close windows")
    while(1):
        if ( cv2.waitKey(20) & 0xFF==27):#Detecta la tecla <ESC>
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)
    logging.debug("| INI | {0} testing".format(__file__))
    with mss() as sct:
        filename = sct.shot(mon=-1, output='fullscreen.png')
        get_text_boxes(imagePath=filename)
    #detect_text()
    logging.debug("| END | {1} testing".format(__file__))
    pass
