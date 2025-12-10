import cv2
import numpy as np 

# Open the video file
cap = cv2.VideoCapture("inderoy_pool_2.mp4")#Nidelv_brygger3.mp4")
ret, current_frame = cap.read()
previous_frame = current_frame
previous_frame_mag = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)    

while(cap.isOpened()):
    current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
 
    # Apply Sobel operator
    sobelx = cv2.Sobel(current_frame_gray, cv2.CV_64F, 1, 0, ksize=3 )  # Horizontal edges
    sobely = cv2.Sobel(current_frame_gray, cv2.CV_64F, 0, 1, ksize=3)  # Vertical edges
    
    # Compute gradient magnitude
    gradient_magnitude = cv2.magnitude(sobelx, sobely)
    
    # Convert to uint8
    gradient_magnitude = cv2.convertScaleAbs(gradient_magnitude)

    # diff
    frame_diff = cv2.absdiff(gradient_magnitude,previous_frame_mag)
    previous_frame_mag = gradient_magnitude
    
    # Display result
    cv2.imshow("Sobel Edge Detection", gradient_magnitude)
           
    fps = 10
    frame_time = 1000/fps
    wait_time = int(frame_time)
    key = cv2.waitKey(wait_time)
    if key == ord('q'):
        break
    if key == ord('p'):
        cv2.waitKey(-1) #wait until any key is pressed

    previous_frame = current_frame.copy()
    ret, current_frame = cap.read()

cap.release()
cv2.destroyAllWindows()