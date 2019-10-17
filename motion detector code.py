import cv2,times
from datetime import  datetime
import pandas as pd
first_frame=None
status_list=[None,None]
times=[]
df=pd.DataFrame(columns=["Start","End"])
#create  adapter/object for capturing video
video=cv2.VideoCapture(0)

while True:
    status=0
    #start the camera and capture frames.Frame is a 2D numpy array which contains intensity of each pixel of a frame.
    check, frame = video.read()
    #convert frame into Gray Scale Image for removing noise up to an extent.
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    gray=cv2.GaussianBlur(gray,(21,21),0)

    #This is first frame.
    if first_frame is None:
        first_frame=gray
        continue
    # calculate change in intensity of pixels when motion is there.
    delta_frame=cv2.absdiff(first_frame,gray)
    thresh_frame=cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
    thresh_frame=cv2.dilate(thresh_frame,None,iterations=2)

    (cnts,_)=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    #find contours in the area>10000 in the captured frame
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status=1
        (x,y,w,h)=cv2.boundingRect(contour)
        # create rectangular box around the required contour which shows the area where motion is detected .
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
    status_list.append(status)
     #if case is 0,1 then object the object was  not present in previous frame but entered into the current frame and vice versa in case 1,0.
     # Notice the time of entry and exit of object in the frame.
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())

    #Show all the images on the screen with caption
    cv2.imshow("Gray Frame",gray)
    cv2.imshow("Delta Frame",delta_frame)
    cv2.imshow("Threshold Frame",thresh_frame)
    cv2.imshow("Color Frame",frame)
    key=cv2.waitKey(1)

    #If user presses 'q' then stop  capturing frame.
    if key==ord('q'):
        if status==1:
            times.append(datetime.now())
            break
print(status_list)
print(times)

#create dataframe for storing start time and end time of motion of an object in the frame.
for i in range(0,len(times),2):
    df=df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)
    #convert dataframe into csv file for better display.
    df.to_csv("Times.csv")
#release the video adapter
video.release()





