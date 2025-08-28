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
    current_frame_gray = cv2.blur(current_frame_gray, (5, 5))
    previous_frame_gray = cv2.blur(previous_frame_gray, (5, 5))

    # diff
    frame_diff = cv2.absdiff(current_frame_gray,previous_frame_gray)
    #frame_diff = cv2.blur(frame_diff, (10, 5))
    frame_diff_masked = cv2.bitwise_and(frame_diff, frame_diff, mask=mask)
    
    # Threshold the image to find white pixels (intensity > 200)
    _, binary_img = cv2.threshold(frame_diff_masked, 10, 255, cv2.THRESH_BINARY)
    for i in range(dimensions[1]):
        new = np.zeros(dimensions[0])
        y_coords = np.nonzero(binary_img[:,i])
        if len(y_coords[0]) > 0:
            y_centroid = np.mean(y_coords)        
            y_centroid = int(np.round(y_centroid))
            new[y_centroid] = 255
        binary_img[:,i] = new
    
    kernel = np.ones((5, 15),np.uint8)
    dilation = cv2.dilate(binary_img,kernel,iterations = 2)
    dilation = cv2.blur(dilation, (50, 15))
    
    for i in range(dimensions[1]):
        new = np.zeros(dimensions[0])
        y_coords = np.nonzero(dilation[:,i])
        if len(y_coords[0]) > 0:
            y_centroid = np.mean(y_coords)        
            y_centroid = int(np.round(y_centroid))
            new[y_centroid] = 255
        dilation[:,i] = new

    # Display result
    cv2.imshow("Rope", cv2.add(dilation, current_frame_gray))
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

    previous_frame = current_frame.copy()
    ret, current_frame = cap.read()

cap.release()
cv2.destroyAllWindows()