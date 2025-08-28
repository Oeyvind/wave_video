import numpy as np
import cv2


cap = cv2.VideoCapture("rope_2.mp4")

while(True):
  # Capture frame-by-frame
   ret, frame = cap.read()

   # Our operations on the frame come here
   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   blur = cv2.GaussianBlur(gray,(5,5),2)
   #ret, thresh_img = cv2.threshold(blur,100,255,cv2.THRESH_BINARY)
   thresh_img = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,15,5)

   contours =  cv2.findContours(thresh_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2]
   for c in contours:
       cv2.drawContours(frame, [c], -1, (0,255,0), 3)
   
   # Display the resulting frame
   cv2.imshow('frame',frame)
   if cv2.waitKey(15) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()