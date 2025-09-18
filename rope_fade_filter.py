import cv2
import numpy as np 
import imutils

# Open the video file
cap = cv2.VideoCapture("rope_ximea_1.mp4")#rope_1.mp4")
ret, current_frame = cap.read()
previous_frame = current_frame.copy()
dimensions = current_frame.shape
output = np.zeros(dimensions[:2], dtype="uint8")

while(cap.isOpened()):
    cur_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    edgeMap = imutils.auto_canny(cur_gray)
    sub = np.astype(output*0.5, 'uint8')
    output = cv2.subtract(cur_gray,sub) 
    #output = np.clip(output,0,255)  

    # Display result
    cv2.imshow("Canny Edge Detection", output)

    if cv2.waitKey(15) & 0xFF == ord('q'):
        break

    previous_frame = current_frame.copy()
    ret, current_frame = cap.read()

cap.release()
cv2.destroyAllWindows()