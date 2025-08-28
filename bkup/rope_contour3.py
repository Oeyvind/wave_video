import numpy as np
import cv2
import imutils


cap = cv2.VideoCapture("rope_2.mp4")
ret, current_frame = cap.read()
previous_frame = current_frame

while(True):
    # Our operations on the frame come here
    gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    previous_frame_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)    

    # diff
    frame_diff = cv2.absdiff(gray,previous_frame_gray)

    blur = cv2.GaussianBlur(frame_diff,(5,5),0)
    ret, thresh_img = cv2.threshold(blur,200,255,cv2.THRESH_BINARY)
    
    thresh_img = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,15,5)
    '''
    contours =  cv2.findContours(thresh_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    cnt = contours[0]
    M = cv2.moments(cnt)
    #print( M )
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt,True)
    epsilon = 0.1*cv2.arcLength(cnt,True)
    approx = cv2.approxPolyDP(cnt,epsilon,True)

    #for c in contours:
    #   cv2.drawContours(frame, [c], -1, (0,255,0), 3)
    cv2.drawContours(frame, [approx], -1, (0, 255, 0), 3)
    '''
    cnts = cv2.findContours(thresh_img.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)
    # draw the shape of the contour on the output image, compute the
    # bounding box, and display the number of points in the contour
    output = gray.copy()
    cv2.drawContours(output, [c], -1, (0, 255, 0), 3)
    (x, y, w, h) = cv2.boundingRect(c)
    
    # Display the resulting frame
    cv2.imshow('frame',frame_diff)
    if cv2.waitKey(15) & 0xFF == ord('q'):
        break

    previous_frame = current_frame.copy()
    ret, current_frame = cap.read()


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()