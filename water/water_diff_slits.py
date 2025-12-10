import cv2
import numpy as np 
import imutils

# Open the video file
#cap = cv2.VideoCapture("Nidelv_brygger3.mp4")
cap = cv2.VideoCapture("dokkpark_2025_10.mp4")
ret, current_frame = cap.read()
dimensions = current_frame.shape
previous_frame = current_frame
previous_frame_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)    
step = False

while(cap.isOpened()):
    current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

    # diff
    #frame_diff = cv2.absdiff(current_frame_gray,previous_frame_gray)
    frame_diff = cv2.subtract(current_frame_gray,previous_frame_gray) # gets lighter
    #frame_diff = cv2.subtract(previous_frame_gray,current_frame_gray) # gets darker
    #frame_diff = cv2.blur(frame_diff, (3,3))
    # adjust image balance
    alpha = 0.7  # Contrast control (1.0 for no change)
    beta = 100    # Brightness control (positive for brighter, negative for darker)
    frame_diff = cv2.convertScaleAbs(frame_diff, alpha=alpha, beta=beta)
    thresh = 50
    _, frame_diff = cv2.threshold(frame_diff, thresh, 255, cv2.THRESH_TOZERO)

    # Display result
    frame_diff_bgr = cv2.cvtColor(frame_diff, cv2.COLOR_GRAY2BGR)
    frame_diff_bgr[0:,:,:2] = 0 # keep only red
    #frame_diff_bgr[0:,:,1] = 0

    # test
    alpha = 1.2  # Contrast control (1.0 for no change)
    beta = -150    # Brightness control (positive for brighter, negative for darker)
    current_frame_dark = cv2.convertScaleAbs(current_frame, alpha=alpha, beta=beta)

    current_frame_g_bgr = cv2.cvtColor(current_frame_gray, cv2.COLOR_GRAY2BGR)
    current_frame_g_bgr[0:,:,1:] = 0 # keep only blue 

    output = current_frame#cv2.add(current_frame_g_bgr, frame_diff_bgr)
    cv2.imshow("Water", output)
    
    key = cv2.waitKey(30)
    if key == ord('q'):
        break
    if key == ord('p'): # pause
        cv2.waitKey(-1) # any key release pause
    if key == ord('s'): # step frame by frame
        step = True
    if step:
        key = cv2.waitKey(-1) 
        if key != ord('s'): # use 's' to step, any key other than 's' releases step freeze
            step = False

    previous_frame_gray = current_frame_gray.copy()
    ret, current_frame = cap.read()
    if not ret:
        break


cap.release()
cv2.destroyAllWindows()