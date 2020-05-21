"""
    This program captures the time when an object enters the fram and when it leaves.
    It stores the time data in a CSV file that will be used for plotting time graph.
    Plotting a time graph is implemented on 'plotting.py' 
"""
import cv2, time, pandas
from datetime import datetime

first_frame = None
status_list = [None, None]
times_list = []

# create a df structure
data_frames = pandas.DataFrame(columns = ["Start", "End"]) 

video = cv2.VideoCapture(0)

while True:
    check, frame = video.read()

    status = 0

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # we need to blur the img and increase accuracy with width and height of 21 and a std deviation of 0
    gray_frame = cv2.GaussianBlur(gray_frame,(21,21),0)

    if first_frame is None:
        first_frame = gray_frame 
        continue # proceeds to the second frame

    delta_frame = cv2.absdiff(first_frame, gray_frame)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # create contours of white objects in thresh frame
    (cnts,_) = cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status = 1

        # if it's equal to and > 1000 create a rectangle and the draw it on a frame
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 3)

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[-1] == 1 and status_list[-2] == 0:
        times_list.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times_list.append(datetime.now())

    cv2.imshow("Capturing Gray Frame...", gray_frame)
    cv2.imshow("Capturing Delta Frame...", delta_frame)
    cv2.imshow("Capturing Thresh Frame...", thresh_frame)
    cv2.imshow("Capturing Color Frame", frame)

    wkey = cv2.waitKey(1)
    # print(gray_frame)
    # print(delta_frame)

    if wkey == ord('q'):
        if status == 1:
            times_list.append(datetime.now())

        break

print(status_list) # if there's an object it will print 1 and if none it prints 0
print(times_list)

# iterate through the times list and append the values in the data frame
for i in range(0, len(times_list), 2):
    data_frames = data_frames.append({"Start":times_list[i], "End":times_list[i+1]}, ignore_index=True)

data_frames.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows