from collections import deque
center = deque()
center.maxlen = 32
print(center)






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
