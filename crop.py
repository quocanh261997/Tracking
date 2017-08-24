import cv2
import numpy as np
import os
from car import Car
car_cascade = cv2.CascadeClassifier("data/cascade.xml")
cap = cv2.VideoCapture("hello.mp4")
carList = []
carID = -1
while(cap.isOpened()):
    ret,frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.equalizeHist(frame_gray)
    cars = car_cascade.detectMultiScale(frame_gray,scaleFactor=2,minNeighbors=6)
    found = False
    for (x,y,w,h) in cars:
        if len(carList)==0:
            c = Car(x,y,w,h)
            carList.append(c)
            carID = c.id
        else:
            list.sort(carList, key=lambda car:car.id)
            for i in range(0,len(carList)):
                if abs(carList[i].cx-x)<15 or abs(carList[i].cy-y)<15:
                    carList[i].cx = x
                    carList[i].cy = y
                    carID = carList[i].id
                    found = True
                    break
            if not found:
                c = Car(x,y,w,h)
                carList.append(c)
                carID = c.id
            copyList = carList[:]
            for i in copyList:
                if i.cy in range(800,630):
                    carList.remove(i)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(frame,str(carID),(x,y),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2,cv2.LINE_AA)
    cv2.imshow("Video",frame)
    if cv2.waitKey(20)==27:
        break
cap.release()
cv2.destroyAllWindows()



# def detectAndDisplay(frame):c
#     resize_frame = cv2.resize(frame,(600,338))
#     frame_gray = cv2.cvtColor(resize_frame,cv2.COLOR_BGR2GRAY)
#     frame_gray = cv2.equalizeHist(frame_gray)
#     height = frame.rows
#     minCarSize = 0.1*height
#     maxCarSize = 0.3*height
#
#     cars = car_cascade.detectMultiScale(frame, scaleFactor=2, minNeighbors=6, minSize=(minCarSize,minCarSize), maxSize=(maxCarSize,maxCarSize))
#     for (x,y,w,h) in cars:
#         c = Car(x,y,w,h)
#         car.append(c)
#
# #Prevent a car being detected multiple time as a new one]
# def filterSame(car=[]):
#     list.sort(car, key=lambda car: car.id)
#     for i in range(0,len(car)):
#         for a in range(i+1,len(car)):
#             if (abs(car[i].cx-car[i].cy)<5):
#                 del car[a]
#                 a -= 1
#     return car
