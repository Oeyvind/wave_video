import cv2
import numpy as np 
import imutils

# Open the video file
cap = cv2.VideoCapture("Nidelv_brygger3.mp4")
ret, current_frame = cap.read()
previous_frame = current_frame
dimensions = current_frame.shape

while(cap.isOpened()):
    current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    previous_frame_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)    

    # diff
    current_frame_gray = cv2.blur(current_frame_gray, (3,3))
    previous_frame_gray = cv2.blur(previous_frame_gray, (3,3))
    #frame_diff = cv2.absdiff(current_frame,previous_frame)
    #frame_diff[0:,:,0] = 0
    #frame_diff[0:,:,2] = 0
    frame_diff = cv2.absdiff(current_frame_gray,previous_frame_gray)
    
    # Display result
    cv2.imshow("Water", frame_diff)
    
    key = cv2.waitKey(30)
    if key == ord('q'):
        break
    if key == ord('p'):
        cv2.waitKey(-1) #wait until any key is pressed

    previous_frame = current_frame.copy()
    ret, current_frame = cap.read()
    if not ret:
        break


cap.release()
cv2.destroyAllWindows()