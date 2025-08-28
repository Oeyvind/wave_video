import cv2
import numpy as np 

# Open the video file
cap = cv2.VideoCapture("rope_2.mp4")
ret, current_frame = cap.read()
previous_frame = current_frame
#previous_frame_mag = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY) 
dimensions = current_frame.shape
mask = np.zeros(current_frame.shape[:2], dtype="uint8")
#rect = cv2.rectangle(mask,(250,300),(1280,700),255,-1)
pts = np.array([[250,300],[1260,300],[1260,750],[250,500]], np.int32)
pts = pts.reshape((-1,1,2))
polyg = cv2.fillPoly(mask,pts=[pts],color=255)

while(cap.isOpened()):
    current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    previous_frame_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)    

    # diff
    frame_diff = cv2.absdiff(current_frame_gray,previous_frame_gray)
    frame_diff_masked = cv2.bitwise_and(frame_diff, frame_diff, mask=mask)
    
    # Display result
    cv2.imshow("Rope", frame_diff_masked)
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

    previous_frame = current_frame.copy()
    ret, current_frame = cap.read()

cap.release()
cv2.destroyAllWindows()