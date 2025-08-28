import cv2
import numpy as np 

# Open the video file
cap = cv2.VideoCapture("nidelva_1.mp4")
ret, current_frame = cap.read()
previous_frame = current_frame

while(cap.isOpened()):
    current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    previous_frame_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)    
 
    # Apply Laplacian operator
    laplacian = cv2.Laplacian(current_frame_gray, cv2.CV_64F)
    
    # Convert to uint8
    laplacian_abs = cv2.convertScaleAbs(laplacian)
    
    # Display result
    cv2.imshow("Laplacian Edge Detection", laplacian_abs)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    previous_frame = current_frame.copy()
    ret, current_frame = cap.read()

cap.release()
cv2.destroyAllWindows()