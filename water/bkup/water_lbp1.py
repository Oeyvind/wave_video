import numpy as np
import cv2 as cv
from skimage.feature import local_binary_pattern

def extract_texture(frame):
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Example using Local Binary Patterns
    radius = 3
    n_points = 8 * radius
    lbp_image = local_binary_pattern(gray_frame, n_points, radius, method="uniform")
    return lbp_image

def extract_wave_shapes(frame):
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Apply Canny edge detection
    edges = cv.Canny(gray_frame, 50, 150)
    # Find contours
    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # You can then filter or analyze these contours based on shape properties (e.g., area, aspect ratio)
    return contours

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
    old_frame = frame.copy()

    # Extract texture
    texture_features = extract_texture(frame)#_diff)
    # Extract wave shapes
    wave_contours = extract_wave_shapes(frame)#_diff)
    
    tf = np.astype(texture_features, 'uint8')
    print('features', np.sum(texture_features), np.sum(tf))
    tf_brg = cv.merge([tf,blank,blank])
    img = cv.add(frame, tf_brg)
    cv.drawContours(frame, wave_contours, -1, (0, 255, 0), 2)
    cv.imshow('frame', frame_diff)#tf_brg)#frame)#frame_diff)
    
    fps = 10
    frame_time = 1000/fps
    wait_time = int(frame_time)
    key = cv.waitKey(wait_time)
    if key == ord('q'):
        break
    if key == ord('p'):
        cv.waitKey(-1) #wait until any key is pressed


cv.destroyAllWindows()