import time
import threading
import Quartz.CoreGraphics as CG
import numpy as np
import cv2
from pynput.keyboard import Key, Controller
import os
import sys
from operator import itemgetter

def initialize():
    #assigning global variables
    global white
    global keyboard
    global dino 
    global dinosleep
    global generation
    global go

    white = [255,255,255]

    #initialize keyboard for input
    keyboard = Controller()

    #loading and processing the templates
    dino = cv2.imread("dino.png")
    dino = cv2.resize(dino,(0,0),fx=0.5,fy=0.5)
    dino = imgproc(dino)
    dino = cv2.Canny(dino,150,200)

    dinosleep = cv2.imread("dinosleep.png")
    dinosleep = cv2.resize(dinosleep,(0,0),fx=0.5,fy=0.5)
    dinosleep = imgproc(dinosleep)
    dinosleep = cv2.Canny(dinosleep,150,200)
    
    cacy = cv2.imread("cacy.png")
    cacy = cv2.resize(cacy,(0,0),fx=0.5,fy=0.5)
    cacy = imgproc(cacy)

    go = cv2.imread("go.png")
    go = cv2.resize(go,(0,0),fx=0.5,fy=0.5)
    go = imgproc(go)
    go = cv2.Canny(go,150,200)

    generation = 1

def main():
    while True:
        t1 = time.time()
        image  = screen_cap()
        temp = imgproc(image)
        edgy   = cv2.Canny(temp,150,200)  
        result1 = cv2.matchTemplate(edgy,dino,cv2.TM_CCOEFF_NORMED)
        result2 = cv2.matchTemplate(edgy,dinosleep,cv2.TM_CCOEFF_NORMED)

        minVal,maxVal1,minLoc,maxLoc1 = cv2.minMaxLoc(result1)
        minVal,maxVal2,minLoc,maxLoc2 = cv2.minMaxLoc(result2)

        if maxVal1 > 0.3 or maxVal2 >0.3:  
            found = True
            if maxVal1>maxVal2:
                l,t    = maxLoc1
                r,d    = 43,34
                dinoedge = l+45
            else:
                l,t    = maxLoc2
                r,d    = 58,34
                dinoedge = l+58

            roi = image[:,l+r+2:l+r+400]

            if isgameover(roi):
                savestate()
                print ("gameover")
                time.sleep(1)

                threading.Thread(target = pressup()).start()
                os.system("clear")

            image  = cv2.rectangle(image,(l,t),(l+r,t+d),(0,0,255),2)
            
            obs = findobstacle(roi)

            if obs:
                x,y,w,h = interpret(obs)
                if x <40 and y > 70:
                    threading.Thread(target = pressup).start()
                cv2.rectangle(roi,(x,y),(w,h),(0,0,255),2)

            cv2.imshow("ts",image)
            cv2.waitKey(1)
        #last_img = 
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
    #processed_img = cv2.Canny(processed_img,150,200)  
    return processed_img

def isgameover(img):
    temp = cv2.Canny(img,150,200)
    res = cv2.matchTemplate(temp,go,cv2.TM_CCOEFF_NORMED)
    minValf,maxValf,minLocf,maxLocf = cv2.minMaxLoc(res)
    if maxValf>0.5:
        return True
    return False

def findobstacle(img):

    temp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(temp,127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    objects = []
    library = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 200:
            x,y,w,h = cv2.boundingRect(cnt)
            box = [x,y,x+w,y+h]
            if w < 100:
                objects.append(box)

    return objects

def interpret(obs):
    obs = sorted(obs,key = itemgetter(0))
    objs=[]
    #print (len(obs))
    objs.append(obs[0])
    for i in range(len(obs)-1):
        #print("yes")
        x1,y1,w1,h1 = obs[i]
        x2,y2,w2,h2 = obs[i+1]
        if x2 - w1 < 10 and x2 - w1>-10:
            #print (x2,w1)
            objs.append(obs[i+1])
        else:
            break

    #print(len(obs),len(objs))

    objs = np.array(objs)
    a = objs[:,:1]
    b = objs[:,1:2]
    c = objs[:,2:3]
    d = objs[:,3:]

    garbage,e = min(enumerate(a), key=itemgetter(1))
    garbage,f = min(enumerate(b), key=itemgetter(1))
    garbage,g = max(enumerate(c), key=itemgetter(1))
    garbage,h = max(enumerate(d), key=itemgetter(1))

    temp = [e,f,g,h]
    #if g-e > 60:
     #   sys.exit(0)
    return temp

def savestate():
    pass

def pressup():
    keyboard.press(Key.space)
    time.sleep(0.1)
    keyboard.release(Key.space)

def get_score:
    
if __name__ == '__main__':
    initialize()
    main()
