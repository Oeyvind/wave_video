import cv2
import numpy as np 
import imutils

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
    
    blur = cv2.GaussianBlur(frame_diff,(5,5),2)
    ret, thresh_img = cv2.threshold(blur,15,255,cv2.THRESH_BINARY)

    cnts = cv2.findContours(thresh_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        print(c)
        # draw the shape of the contour on the output image, compute the
        # bounding box, and display the number of points in the contour
        output = current_frame_gray.copy()
        cv2.drawContours(output, [c], -1, (0, 255, 0), 3)
        (x, y, w, h) = cv2.boundingRect(c)


    # Display result
    cv2.imshow("Test", current_frame_gray)
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

    previous_frame = current_frame.copy()
    ret, current_frame = cap.read()

cap.release()
cv2.destroyAllWindows()