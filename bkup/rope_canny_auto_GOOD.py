import cv2
import numpy as np 
import imutils

# Open the video file
cap = cv2.VideoCapture("rope_1.mp4")
ret, current_frame = cap.read()

while(cap.isOpened()):
    gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    edgeMap = imutils.auto_canny(gray)

    # Display result
    cv2.imshow("Canny Edge Detection", edgeMap)

    if cv2.waitKey(15) & 0xFF == ord('q'):
        break

    previous_frame = current_frame.copy()
    ret, current_frame = cap.read()

cap.release()
cv2.destroyAllWindows()