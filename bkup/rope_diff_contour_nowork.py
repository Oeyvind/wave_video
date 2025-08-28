import cv2
import numpy as np 

# Open the video file
cap = cv2.VideoCapture("rope_2.mp4")
ret, current_frame = cap.read()
previous_frame = current_frame
#previous_frame_mag = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)    

while(cap.isOpened()):
    current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    previous_frame_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)    

    # diff
    frame_diff = cv2.absdiff(current_frame_gray,previous_frame_gray)
    
    ret, thresh = cv2.threshold(frame_diff, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #cnt = contours[4]
    print(contours)
    if len(contours) > 0:
        cv2.drawContours(thresh, contours, -1, (0,255,0), 3)

    #cv2.imshow("Sobel Edge Detection", gradient_magnitude)
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

    previous_frame = current_frame.copy()
    ret, current_frame = cap.read()

cap.release()
cv2.destroyAllWindows()