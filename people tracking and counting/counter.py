import cv2
import numpy as np
import pandas as pd
import time
import datetime
import csv

cap = cv2.VideoCapture("walk.avi")
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")
ret, frame1 = cap.read()
ret, frame2= cap.read()

h = 1366
w = 840
frameArea = h * w
areaTH = frameArea / 250
print('Area Threshold', areaTH)

kernel = np.ones((5, 5), np.uint8)
total = 0

while cap.isOpened():
    contour = face_cascade.detectMultiScale(frame1, scaleFactor=1.5, minNeighbors=5)
    dif = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(dif, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5), 0)
    kernel, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    erode = cv2.erode(thresh, None, iterations=3)
    dilated = cv2.dilate(erode, None, iterations=10)
    erode2 = cv2.erode(dilated, None, iterations=3)
    dilated2 = cv2.dilate(dilated, None, iterations=7)
    contours, kernel= cv2.findContours(dilated2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    ret, labels = cv2.connectedComponents(dilated2)
    Id = ret
    total = 0
    for contour in contours:
        total = total + 1
        M = cv2.moments(contour)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < 900:
            continue
        cv2.circle(frame1, (cx, cy), 5, (0, 0, 255), -1)
        cv2.rectangle(frame1, (x,y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame1, "status: {}".format('movement'), (10,20), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 2)
        title = ('People tracking are:' + str(ret))
        #title1 = ('People counted:' + str(total))
        cv2.putText(frame1, title, (10, 90), cv2.FONT_HERSHEY_SIMPLEX,1 , (0, 255, 255), 2 )
        #cv2.putText(frame1, title1, (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    #cv2. drawContours(frame1, contours, -1, ( 0, 255, 0 ), 2)
    cv2.imshow("ekk", frame1)
    cv2.imshow("cek", dilated)
    cv2.imshow("eee", erode)

    #cv2.imshow("wuw", dilated2)
    #cv2.imshow("uwu", erode2)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27 :
        break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour,Minute,Second=timeStamp.split(":")
    row = [ Id, date, timeStamp]
    with open('Allrecap\Allrecap.csv', 'a+') as csvFile:
        #counted = counted.drop_duplicates(subset=['Id'], keep='last')
        writer = csv.writer(csvFile)
        writer.writerow(row)
    print(row)
    #print(Id)
#df = pd.read_csv('Allrecap\Allrecap.csv')
header_names = ['value', 'date', 'time']
df = pd.read_csv('Allrecap\Allrecap.csv', header = None, skiprows=1, names=header_names)
#df.head()
value_sum = df['value'].sum()
value_mean = df['value'].mean()
df['time']=pd.to_datetime(df['time'])
time_head = df['time'].head(1)
time_tail = df['time'].tail(1)
time_estimation = [time_head,time_tail]
row = [Id, date, timeStamp, value_sum, value_mean,time_estimation]
with open('Allrecap\Allrecap.csv', 'a+') as csvFile:
        #counted = counted.drop_duplicates(subset=['Id'], keep='last')
        writer = csv.writer(csvFile)
        writer.writerow(row)
#print("total person has been counted :",value_sum)
print("average person has been counted :",value_mean)
print("time estimation are ",time_estimation)
#print("total person has been counted:",total)

cv2.destroyAllWindows()
cap.realese()


