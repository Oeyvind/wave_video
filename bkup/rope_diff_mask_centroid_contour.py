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
pts = np.array([[250,300],[1260,300],[1260,750],[250,500]], np.int32)
pts = pts.reshape((-1,1,2))
polyg = cv2.fillPoly(mask,pts=[pts],color=255)

while(cap.isOpened()):
    current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    previous_frame_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)    

    # diff
    frame_diff = cv2.absdiff(current_frame_gray,previous_frame_gray)
    frame_diff_masked = cv2.bitwise_and(frame_diff, frame_diff, mask=mask)
    
    # Threshold the image to find white pixels (intensity > 200)
    _, binary_img = cv2.threshold(frame_diff_masked, 20, 255, cv2.THRESH_BINARY)
    for i in range(dimensions[1]):
        new = np.zeros(dimensions[0])
        y_coords = np.nonzero(binary_img[:,i])
        if len(y_coords[0]) > 0:
            y_centroid = np.mean(y_coords)        
            y_centroid = int(np.round(y_centroid))
            new[y_centroid] = 255
        binary_img[:,i] = new
    bgr_image = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)
    contours = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(contours)
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        #cv2.drawContours(bgr_image, [c], -1, (0, 255, 0), 3)
        eps = 0.00001
        # approximate the contour
        peri = cv2.arcLength(c, False)
        approx = cv2.approxPolyDP(c, eps * peri, False)
        # draw the approximated contour on the image
        #cv2.drawContours(bgr_image, [approx], -1, (0, 255, 0), 10)

    #if len(cnts) > 0:
        #for c in cnts:
            #M = cv2.moments(c)
            #perimeter = cv2.arcLength(c,False)
            #approx = cv2.approxPolyDP(c,0.1,False)
            #epsilon = 0.001*cv2.arcLength(cnts,False)
            #approx = cv2.approxPolyDP(cnts,0.01,False)
            #cv2.drawContours(bgr_image, approx, -1, (0,255,0), 1)
            #cv2.drawContours(bgr_image, [cnts], -1, (0, 255, 0), 1)  # Draw original contour
            #cv2.drawContours(bgr_image, [approx], -1, (0, 0, 255), 1) # Draw approximated contour

    # Display result
    cv2.imshow("Rope", bgr_image)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

    previous_frame = current_frame.copy()
    ret, current_frame = cap.read()

cap.release()
cv2.destroyAllWindows()