import cv2
import numpy as np 
import imutils

# Open the video file
cap = cv2.VideoCapture("rope_2.mp4")
ret, current_frame = cap.read()
previous_frame = current_frame
#previous_frame_mag = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY) 
dimensions = current_frame.shape
mask = np.zeros(current_frame.shape[:2], dtype="uint8")
#rect = cv2.rectangle(mask,(250,300),(1280,700),255,-1)
pts = np.array([[250,400],[1260,200],[1260,700],[800,700],[250,500]], np.int32)
pts = pts.reshape((-1,1,2))
polyg = cv2.fillPoly(mask,pts=[pts],color=255)

while(cap.isOpened()):
    current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    previous_frame_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)    

    # diff
    frame_diff = cv2.absdiff(current_frame_gray,previous_frame_gray)
    frame_diff_masked = cv2.bitwise_and(frame_diff, frame_diff, mask=mask)
    
    ret, thresh = cv2.threshold(frame_diff_masked, 15, 255, 0)
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    cnts = imutils.grab_contours(contours)
    if len(cnts) > 0:
        for c in cnts:
            M = cv2.moments(c)
            #perimeter = cv2.arcLength(c,False)
            #approx = cv2.approxPolyDP(c,0.1,False)
            epsilon = 0.01*cv2.arcLength(c,False)
            approx = cv2.approxPolyDP(c,epsilon,False)
            cv2.drawContours(current_frame_gray, [approx], -1, (0,255,0), 3)
            
        
    #    c = max(cnts, key=cv2.contourArea)
    #    cv2.drawContours(current_frame_gray, [c], -1, (0,255,0), 3)

    # Display result
    cv2.imshow("Rope", current_frame_gray)
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

    previous_frame = current_frame.copy()
    ret, current_frame = cap.read()

cap.release()
cv2.destroyAllWindows()