import numpy as np
import cv2 as cv
from skimage.feature import local_binary_pattern


# Open the video file
cap = cv.VideoCapture("inderoy_pool_2.mp4")
ret, old_frame = cap.read()
dimensions = np.shape(old_frame)[:2]
blank = np.zeros(dimensions, dtype='uint8')
print(dimensions, np.shape(blank))
#import sys
#sys.exit()

while True:
    ret, frame = cap.read()
    frame_diff = cv.subtract(frame,old_frame)
    frame_diff = np.clip(frame_diff,0,255)
    frame_diff = cv.blur(frame_diff, (7, 7))
    old_frame = frame.copy()

    # Extract wave shapes
    gray_frame = cv.cvtColor(frame_diff, cv.COLOR_BGR2GRAY)
    # Apply Canny edge detection
    edges = cv.Canny(gray_frame, 50, 150)
    edges1 = cv.Canny(gray_frame, 1, 50)
    edges2 = cv.Canny(gray_frame, 150, 250)
    # Find contours
    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    edges_b = cv.merge([edges,blank,edges1])
    cv.drawContours(frame, contours, -1, (0, 100, 0), 6)
    output = cv.add(edges_b, frame_diff)
    cv.imshow('frame', output)#tf_brg)#frame)#frame_diff)
    
    fps = 10
    frame_time = 1000/fps
    wait_time = int(frame_time)
    key = cv.waitKey(wait_time)
    if key == ord('q'):
        break
    if key == ord('p'):
        cv.waitKey(-1) #wait until any key is pressed


cv.destroyAllWindows()