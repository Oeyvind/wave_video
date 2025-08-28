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
    
    # muddy
    ##ret, thresh = cv2.threshold(binary_img, 127, 255, 1)  
    ##kernel = np.ones((5, 5),np.uint8)
    ##erosion = cv2.morphologyEx(thresh, cv2.MORPH_ERODE, kernel, iterations = 4)
    ##ret, thresh1 = cv2.threshold(erosion, 127, 255, 1)
    ##blur = cv2.blur(thresh1, (5, 5))
    ##ret, thresh2 = cv2.threshold(blur, 145, 255, 0)
    ##kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    ##final = cv2.morphologyEx(thresh2, cv2.MORPH_ERODE, kernel1, iterations = 2)
    
    #https://stackoverflow.com/questions/43293915/how-could-i-make-the-discontinuous-contour-of-an-image-consistant
    # bezier approximation, then connect the beziers...?
    # OR: use contours

    # Display result
    cv2.imshow("Rope", binary_img)
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

    previous_frame = current_frame.copy()
    ret, current_frame = cap.read()

cap.release()
cv2.destroyAllWindows()