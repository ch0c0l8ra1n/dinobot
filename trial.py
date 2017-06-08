import time
import threading
import Quartz.CoreGraphics as CG
import numpy as np
import cv2
from pynput.keyboard import Key, Controller
import os

def initialize():
    #assigning global variables
    global keyboard
    global dino 
    global dinosleep
    global cacy
    global go

    #initialize keyboard for input
    keyboard = Controller()

    #loading and processing the templates
    dino = cv2.imread("dino.png")
    dino = cv2.resize(dino,(0,0),fx=0.5,fy=0.5)
    dino = imgproc(dino)

    dinosleep = cv2.imread("dinosleep.png")
    dinosleep = cv2.resize(dinosleep,(0,0),fx=0.5,fy=0.5)
    dinosleep = imgproc(dinosleep)
    
    cacy = cv2.imread("cacy.png")
    cacy = cv2.resize(cacy,(0,0),fx=0.5,fy=0.5)
    cacy = imgproc(cacy)

    go = cv2.imread("go.png")
    go = cv2.resize(go,(0,0),fx=0.5,fy=0.5)
    go = imgproc(go)



def main():
    while True:
        t1 = time.time()
        image  = screen_cap()
        edgy   = imgproc(image)
        result1 = cv2.matchTemplate(edgy,dino,cv2.TM_CCOEFF_NORMED)
        result2 = cv2.matchTemplate(edgy,dinosleep,cv2.TM_CCOEFF_NORMED)

        minVal,maxVal1,minLoc,maxLoc1 = cv2.minMaxLoc(result1)
        minVal,maxVal2,minLoc,maxLoc2 = cv2.minMaxLoc(result2)
        if maxVal1 > 0.3 or maxVal2 >0.3:    
            if maxVal1>maxVal2:
                l,t    = maxLoc1
                image  = cv2.rectangle(image,(l,t),(l+45,t+34),(0,0,255),2)
                dinoedge = l+45
            else:
                l,t    = maxLoc2
                image  = cv2.rectangle(image,(l,t),(l+58,t+34),(0,0,255),2)
                dinoedge = l+58
            roi    = image[:133,l:420]
            roi = imgproc(roi)

            if isgameover(roi):
                savestate()
                print ("gameover")
                time.sleep(1)
                keyboard.press(Key.space)
                keyboard.release(Key.space )
                os.system("clear")

            #keyboard.press(Key.space)
            #keyboard.release(Key.space)
            cv2.imshow("ts",roi)
            cv2.waitKey(1)
        print (time.time()-t1)

def screen_cap():
    region = CG.CGRectMake(225, 125, 832-225, 275-125 )
    screen = CG.CGWindowListCreateImage(region, CG.kCGWindowListOptionOnScreenOnly, CG.kCGNullWindowID, CG.kCGWindowImageDefault)
    width = CG.CGImageGetWidth(screen)
    height = CG.CGImageGetHeight(screen)
    bytesperrow = CG.CGImageGetBytesPerRow(screen)
    pixeldata = CG.CGDataProviderCopyData(CG.CGImageGetDataProvider(screen))
    screen = np.frombuffer(pixeldata, dtype=np.uint8)
    screen = screen.reshape((height, bytesperrow//4, 4))
    screen = screen[:,:width,:]
    screen = cv2.resize(screen, (0,0), fx=0.5, fy=0.5)
    return screen

def imgproc(img):
    processed_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    processed_img = cv2.GaussianBlur(processed_img,(5,5),2)
    processed_img = cv2.Canny(processed_img,150,200)  
    return processed_img

def isgameover(img):
    res = cv2.matchTemplate(img,go,cv2.TM_CCOEFF_NORMED)
    minValf,maxValf,minLocf,maxLocf = cv2.minMaxLoc(res)
    if maxValf>0.5:
        return True
    return False

def savestate():
    pass
    
if __name__ == '__main__':
    initialize()
    main()