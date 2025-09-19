import cv2
import numpy as np
from matplotlib import pyplot as plt

cap = cv2.VideoCapture("rope_2.mp4")#rope_ximea_1.mp4")
ret, current_frame = cap.read()
current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
previous_gray = np.copy(current_gray)

mask1 = np.zeros(current_frame.shape[:2], dtype="uint8")
pts = np.array([[250,300],[1260,300],[1260,750],[250,500]], np.int32)
pts = pts.reshape((-1,1,2))
polyg = cv2.fillPoly(mask1,pts=[pts],color=255)

blank = np.zeros_like(current_frame)



while(True):
    ret, current_frame = cap.read()
    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    #frame_diff = cv2.absdiff(current_gray,previous_gray)
    #frame_diff_masked = cv2.bitwise_and(frame_diff, frame_diff, mask=mask1)
    frame_diff = cv2.subtract(current_gray,previous_gray)
    frame_diff = np.clip(frame_diff,0,255)
    frame_diff_masked = cv2.bitwise_and(frame_diff, frame_diff, mask=mask1)
    frame_diff_masked = cv2.blur(frame_diff_masked, (5,5))
    ret,fdm_thresh = cv2.threshold(frame_diff_masked, 20,255, cv2.THRESH_BINARY)
    #fdm_thresh = cv2.adaptiveThreshold(frame_diff_masked,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    noise = np.zeros_like(current_gray)
    mean = 0
    std_dev = 30
    fdm_nois = cv2.add(fdm_thresh, cv2.randn(noise, mean, std_dev))
    # show mask
    polyg_show = cv2.polylines(current_frame,pts=[pts],isClosed=True, color=(255,0,0),thickness=2)

    # fft
    f = np.fft.fft2(frame_diff_masked)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20*np.log(np.abs(fshift))

    f2 = np.fft.fft2(fdm_nois)
    fshift2 = np.fft.fftshift(f2)
    magnitude_spectrum2 = 20*np.log(np.abs(fshift2))

    # grayscale to color    
    mags_bgr = cv2.cvtColor(np.astype(magnitude_spectrum, 'uint8'), cv2.COLOR_GRAY2RGB)
    mags_bgr2 = cv2.cvtColor(np.astype(magnitude_spectrum2, 'uint8'), cv2.COLOR_GRAY2RGB)
    frame_diff_masked_bgr = cv2.cvtColor(frame_diff_masked, cv2.COLOR_GRAY2RGB)
    fdm_thresh_masked_bgr = cv2.cvtColor(fdm_nois, cv2.COLOR_GRAY2RGB)
    
    # assemble image grid
    h_concat = np.concatenate((current_frame, mags_bgr), axis=1)

    zoom_factor = 4
    mags_y, mags_x = np.shape(mags_bgr)[:2]
    mags_bgr_zoom = cv2.resize(mags_bgr[int((mags_y/2)-((mags_y/2)/zoom_factor)):int((mags_y/2)+((mags_y/2)/zoom_factor)),
                                        int((mags_x/2)-((mags_x/2)/zoom_factor)):int((mags_x/2)+((mags_x/2)/zoom_factor))], 
                                        None, fx=zoom_factor, fy=zoom_factor)
    h2_concat = np.concatenate((frame_diff_masked_bgr, mags_bgr_zoom), axis=1)

    mags_bgr_zoom2 = cv2.resize(mags_bgr2[int((mags_y/2)-((mags_y/2)/zoom_factor)):int((mags_y/2)+((mags_y/2)/zoom_factor)),
                                        int((mags_x/2)-((mags_x/2)/zoom_factor)):int((mags_x/2)+((mags_x/2)/zoom_factor))], 
                                        None, fx=zoom_factor, fy=zoom_factor)
    h3_concat = np.concatenate((fdm_thresh_masked_bgr, mags_bgr_zoom2), axis=1)
    
    hv_concat = np.concatenate((h_concat, h2_concat, h3_concat), axis=0)
    insize = np.shape(hv_concat)
    downsamp = 3
    output = cv2.resize(hv_concat, (int(insize[1]/downsamp), int(insize[0]/downsamp)))
    cv2.imshow('frame', output)

    fps = 20
    frame_time = 1000/fps
    #wait_time = int(frame_time - processing_time)
    #if wait_time < 1: wait_time = 1
    key = cv2.waitKey(int(frame_time))

    if key == ord('q'):
            break
    if key == ord('p'):
        cv2.waitKey(-1) #wait until any key is pressed

    # Update the previous frame and previous points
    previous_gray = np.copy(current_gray)
    
cv2.destroyAllWindows()
cap.release()