import numpy as np
import cv2 as cv

# Open the video file
#cap = cv.VideoCapture("inderoy_pool_2.mp4")#Nidelv_brygger3.mp4")
cap = cv.VideoCapture("rope_2.mp4")#rope_ximea_1.mp4")

ret, frame1 = cap.read()
prvs = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[..., 1] = 255
while(1):
    ret, frame2 = cap.read()
    if not ret:
        print('No frames grabbed!')
        break
    next = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)

    scale = 0.75
    levels = 3
    wsize = 15
    itr = 1
    poly = 5
    psigma = 1.1
    flags = cv.OPTFLOW_FARNEBACK_GAUSSIAN
    flow = cv.calcOpticalFlowFarneback(prvs, next, None, scale, levels, wsize, itr, poly, psigma, flags)
    mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
    hsv[..., 0] = ang*180/np.pi/2
    hsv[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
    bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
    
    
    cv.imshow('frame2', bgr)
       
    fps = 20
    frame_time = 1000/fps
    wait_time = int(frame_time)
    key = cv.waitKey(wait_time)
    if key == ord('q'):
        break
    if key == ord('p'):
        cv.waitKey(-1) #wait until any key is pressed

    prvs = next
cv.destroyAllWindows()