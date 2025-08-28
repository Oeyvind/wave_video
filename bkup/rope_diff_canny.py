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
    
    # Apply Gaussian Blur to reduce noise
    blur = cv2.GaussianBlur(current_frame_gray, (5, 5), 1.4)
    
    # Apply Canny Edge Detector
    edges = cv2.Canny(blur, threshold1=0, threshold2=200)

    # Display result
    cv2.imshow("Canny Edge Detection", edges)
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

    previous_frame = current_frame.copy()
    ret, current_frame = cap.read()

cap.release()
cv2.destroyAllWindows()