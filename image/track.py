import cv2
import numpy as np
from car import Car
from collections import deque
car = []

#Delete cars that have different or same id, but too close too each other
def filterSame(car):
    list.sort(car, key=lambda car:car.id)
    car = car[::-1]
    newCar = []
    for i in range(0,len(car)-1):
        for a in range(i+1,len(car)):
            if car[i] not in newCar:
                if abs(car[i].cx-car[a].cx)<5:
                    if car[a] not in newCar:
                        newCar.append(car[a])
    car = [x for x in car if x not in newCar]
    return car

#Update the coordinates for dx and dy
def updateDXY(car):
    for i in range(0,len(car)):
        if car[i].xs[0]!=0 and car[i].xs[4]!=0:
            car[i].dx = abs(car[i].xs[(car[i].exe-1)%5]-car[i].xs[(car[i].exe-5)%5])/5.0
            car[i].dy = abs(car[i].ys[(car[i].exe-1)%5]-car[i].ys[(car[i].exe-5)%5])/5.0
    return car

#Remove points that are (0,0), which are filled automatically by the deque
def filterCenter(cenA):
    cenB = deque(maxlen=64)
    for i in cenA:
        if i!=(0,0):
            cenB.append(i)
    return cenB

#Update the fx and fy coordinates of the car
def updateFXY(car):
    for i in range(0,len(car)):
        car[i].fx = car[i].fx + car[i].dx
        car[i].fy = car[i].fy + car[i].dy
    return car

#Remove detected cars that have the same coordinate as the comparing car
def filterRectOne(detected, car):
    filter = []
    for (x,y,w,h) in detected:
        if car.cx!=x and car.cy!=y:
            filter.append((x,y,w,h))
    return filter

#Update the car that is already detected in the last frame
def filter(car,a):
    newList = []
    for i in a:
        if i.id!=car.id:
            newList.append(i)
    newList.append(car)
    return newList

#Remove car that fails a lot
def getRid(car):
    filter = []
    for i in range(0,len(car)):
        if car[i].stat<40:
            filter.append(car[i])
    return filter

#Remove duplicate cars
def filterRect(detected,cars):
    filtered = []
    for (x,y,w,h) in detected:
        dup = False
        for a in cars:
            if x == a.cx and y == a.cy:
                dup = True
        if not dup:
            filtered.append((x,y,w,h))
    return filtered

#Find the closest car in the array to the compared car
def findClosest(car, objs):
    minx, miny, minrad, minwid, minhei = 0,0,10000,0,0
    if car.stat == 1:
        for (x,y,w,h) in objs:
            if x-car.cx >= -15 or y-car.cy >= -15:
                if (pow(x-car.cx,2)+pow(y-car.cy,2))<minrad:
                    minx = x
                    miny = y
                    minrad = pow(x-car.cx,2)+pow(y-car.cy,2)
                    minwid = w
                    minhei = h
    else:
        for (x,y,w,h) in objs:
            if x-car.cx >= -15 or y-car.cy >= -15:
                if (pow(x-car.fx,2)+pow(y-car.fy,2))<minrad:
                    minx = x
                    miny = y
                    minrad = pow(x-car.fx,2)+pow(y-car.fy,2)
                    minwid = w
                    minhei = h
    c = Car(minx,miny,minwid,minhei,car.id)
    c.center = car.center
    c.center.appendleft((minx+minwid//2,miny+minhei//2))
    c.prex = car.cx
    c.prey = car.cy
    if len(objs)==0 or minrad > 2000:
        c.id = -1
    elif car.stat == 1:
        c.xs = car.xs[:]
        c.ys = car.ys[:]
        c.xs[car.exe%5] = car.cx
        c.ys[car.exe%5] = car.cy
        c.exe = car.exe + 1
    return c

def detectAndDisplay(frame,car_cascade):
    global car
    frame = cv2.resize(frame,(800,450))
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.equalizeHist(frame_gray)
    cars = car_cascade.detectMultiScale(frame_gray,scaleFactor=1.2,minNeighbors=20)
    for (x,y,w,h) in cars:
        print("x: {}, y: {} \n".format(x,y))
    if len(car)==0:
        for (x,y,w,h) in cars:
            d = Car(x,y,w,h)
            d.center.appendleft((x+w//2,y+h//2))
            car.append(d)
    else:
        k = 0
        while(k<len(car)):
            b = findClosest(car[k],cars)
            if b.id != -1:
                car = filter(b,car)
                k -= 1
                cars = filterRectOne(cars,b)
            else:
                car[k].stat += 1
                if car[k].stat>1:
                    car[k].exe = 0
            k += 1
        car = getRid(car)
        car = updateDXY(car)
        car = updateFXY(car)
        car = filterSame(car)
        cars = filterRect(cars,car)
        for (x,y,w,h) in cars:
            d = Car(x,y,w,h)
            d.center.appendleft((x+w//2,y+h//2))
            car.append(d)
    # for i in range(0,len(car)):
    #     car[i].center.appendleft((car[i].cx,car[i].cy))
    #     print(car[i].center)
    for i in car:
        i.center = filterCenter(i.center)
        cv2.rectangle(frame,(i.cx,i.cy),(i.cx+i.width,i.cy+i.height),(0,255,0),2)
        cv2.putText(frame, str(i.id),(i.cx,i.cy),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2,cv2.LINE_AA)
        for j in range(1,len(i.center)):
            if i.center[j-1] is None or i.center[j] is None:
                continue
            thickness = int(np.sqrt(64 / float(j + 1)) * 2.5)
            cv2.line(frame, i.center[j-1],i.center[j],(0,0,255),3)
    cv2.imshow("Video Detection",frame)

#Turn on the heat baby
car_cascade = cv2.CascadeClassifier("data/cascade.xml")
cap = cv2.VideoCapture("hello.mp4")
if(cap.isOpened()):
    while(True):
        success,frame = cap.read()
        if not success:
            print("no more frame available")
        detectAndDisplay(frame,car_cascade)
        c = cv2.waitKey(30)
        if c==ord('c'):
            break
cap.release()
cv2.destroyAllWindows()
