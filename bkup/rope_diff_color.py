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
    diff = np.clip(current_frame-previous_frame,0,255)
    #sub = np.astype(output*0.5, 'uint8')
    #thresh = cv2.inRange(diff,(255,255,25), (255,255,255))
    blue = diff[:,:,0]
    green = diff[:,:,1]
    red = diff[:,:,2]
    ret,blue = cv2.threshold(blue, 200, 255, cv2.THRESH_BINARY)
    ret,green = cv2.threshold(green, 200, 255, cv2.THRESH_BINARY)
    ret,red = cv2.threshold(red, 200, 255, cv2.THRESH_BINARY)

    output = cv2.merge((blue,green,red))#thresh#diff#cv2.subtract(cur_gray,sub) 
    #output = np.clip(output,0,255)  

    # Display result
    cv2.imshow("Color diff", output)

    if cv2.waitKey(15) & 0xFF == ord('q'):
        break

    previous_frame = current_frame.copy()
    ret, current_frame = cap.read()

cap.release()
cv2.destroyAllWindows()