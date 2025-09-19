import cv2
import numpy as np 
#import scipy
#from scipy.signal import decimate
from skimage.feature import local_binary_pattern


import imutils
import osc_io
import time
timethen = time.time()

fps = 40
cap = cv2.VideoCapture("rope_ximea_1.mp4")
ret, current_frame = cap.read()
previous_frame = current_frame
dimensions = current_frame.shape
print(dimensions)
mask = np.zeros(dimensions[:2], dtype="uint8")
pts = np.array([[int(dimensions[1]*0.05),int(dimensions[0]*0.2)],
                [int(dimensions[1]*0.96),int(dimensions[0]*0.3)],
                [int(dimensions[1]*0.96),int(dimensions[0]*0.8)],
                [int(dimensions[1]*0.05),int(dimensions[0]*0.8)]], np.int32)
max_amp = np.max(pts[:,1])-np.min(pts[:,1])
pts = pts.reshape((-1,1,2))
polyg = cv2.fillPoly(mask,pts=[pts],color=255)
# print mask center y left and center y right
print(pts[0][0][1],pts[3][0][1])
mask_left = pts[0][0][0] # left top, assumes vertical left edge
mask_right = pts[1][0][0] # right top, as above
print('mask LR', mask_left, mask_right)
show_mask = True
send_counter = 0


# BGR colors
red = (0,0,255)
blue = (255,0,0)
green = (0,255,0)
yellow = (0,255,255)
pink = (255,0,255)
light_blue = (255,255,0)
orange = (0,128,255)
light_green = (204,255,153)
purple = (255,102,178)
light_pink = (204,153,255)
dull_green = (0,128,0)
dull_red = (0,0,128)

#def extract_texture(frame):
#    #gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#    # Example using Local Binary Patterns
#    radius = 3
#    n_points = 8 * radius
#    lbp_image = local_binary_pattern(frame, n_points, radius, method="uniform")
#    return lbp_image

try:
    print('Starting video. Press q to exit.')
    while True:
        time_start = time.time()
        current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        previous_frame_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)    
        # diff and mask
        frame_diff = cv2.subtract(current_frame_gray,previous_frame_gray)
        frame_diff = np.clip(frame_diff,0,255)
        frame_diff_masked = cv2.bitwise_and(frame_diff, frame_diff, mask=mask)
        frame_diff_masked = cv2.blur(frame_diff_masked, (5,5))
        # threshold the image to make hard black/white
        _, binary_img = cv2.threshold(frame_diff_masked, 5, 255, cv2.THRESH_BINARY)
        # output img for display of curves
        wave_img = np.zeros((dimensions[0], dimensions[1],3), np.uint8)

        # downsample
        dfactor = 32
        downsampled = binary_img[::dfactor,::dfactor]
        #downsampled = extract_texture(downsampled_)
        #kernel = np.ones((3,3),np.uint8) # A 5x5 rectangular kernel
        #downsampled = cv2.erode(downsampled_, kernel, iterations = 1)
        dsize = int(np.sum(np.ma.getmask(np.ma.masked_greater(downsampled,0))))
        i = 0
        for x in range(np.shape(downsampled)[0]):
            for y in range(np.shape(downsampled)[1]):
                if downsampled[x,y] > 0:
                    i += 1
                    #print('i', i, dsize, np.sum(binary_img))
                    osc_msg = fps,dsize,i,x,y
                    osc_io.sendOSC('wave_video_xy', osc_msg) # send OSC back to client
        
        # Display result
        output = downsampled#qbinary_img#cv2.add(current_frame, wave_img)    
        #if show_mask:
        #    polyg_show = cv2.polylines(output,pts=[pts],isClosed=True, color=(255,0,0),thickness=2)
        size_ = 640
        scale = size_/np.shape(output)[1] # data array shape is y,x
        size = (size_,int(np.shape(output)[0]*scale))
        output = cv2.resize(output, size)
        cv2.imshow("Rope", output)
        previous_frame = current_frame.copy()
        ret, current_frame = cap.read()
        if not ret:
            break

        # timing, frame rate
        time_now = time.time()
        processing_time = (time_now - time_start)*1000
        frame_time = 1000/fps
        wait_time = int(frame_time - processing_time)
        if wait_time < 1: wait_time = 1
        key = cv2.waitKey(wait_time)

        if key == ord('q'):
            break
        if key == ord('p'):
            cv2.waitKey(-1) #wait until any key is pressed

except KeyboardInterrupt:
    cap.release()
    cv2.destroyAllWindows()
print('Done.')
