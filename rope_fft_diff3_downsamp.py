import cv2
import numpy as np
from matplotlib import pyplot as plt

cap = cv2.VideoCapture("rope_2.mp4")#rope_ximea_1.mp4")
ret, current_frame = cap.read()
insize1 = np.shape(current_frame)[:2]
dsamp1 = 4
current_frame = cv2.resize(current_frame, (int(insize1[1]/dsamp1), int(insize1[0]/dsamp1)))
current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
previous_gray = np.copy(current_gray)
dimensions = np.shape(current_gray)

mask1 = np.zeros(current_frame.shape[:2], dtype="uint8")

pts = np.array([[dimensions[1]*0.195,dimensions[0]*0.42],
                [dimensions[1]*0.98, dimensions[0]*0.42],
                [dimensions[1]*0.98, dimensions[0]*1.1],
                [dimensions[1]*0.195,dimensions[0]*0.7]], np.int32)
pts = pts.reshape((-1,1,2))
polyg = cv2.fillPoly(mask1,pts=[pts],color=255)

blank = np.zeros_like(current_frame)



while(True):
    ret, current_frame = cap.read()
    current_frame = cv2.resize(current_frame, (int(insize1[1]/dsamp1), int(insize1[0]/dsamp1)))
    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    #frame_diff = cv2.absdiff(current_gray,previous_gray)
    #frame_diff_masked = cv2.bitwise_and(frame_diff, frame_diff, mask=mask1)
    frame_diff = cv2.subtract(current_gray,previous_gray)
    frame_diff = np.clip(frame_diff,0,255)
    frame_diff_masked = cv2.bitwise_and(frame_diff, frame_diff, mask=mask1)
    frame_diff_masked = cv2.blur(frame_diff_masked, (5,5))
    # show mask
    polyg_show = cv2.polylines(current_frame,pts=[pts],isClosed=True, color=(255,0,0),thickness=2)

    # fft
    f1 = np.fft.fft2(frame_diff_masked)
    fshift1 = np.fft.fftshift(f1)
    magnitude_spectrum = 20*np.log(np.abs(fshift1))
    ffilt1 = np.copy(fshift1)
    filt_coef = 0.05
    filt_coord = [int(dimensions[0]*(0.5-filt_coef)), int(dimensions[0]*(0.5+filt_coef)),
                  int(dimensions[1]*(0.5-filt_coef)), int(dimensions[1]*(0.5+filt_coef)),]
    print(filt_coord, dimensions)
    filt = np.zeros_like(current_gray)
    filt[filt_coord[0]:filt_coord[1], filt_coord[2]:filt_coord[3]] = 1
    ffilt1 = ffilt1*filt
    #ffilt1[filt_coord[0]:filt_coord[1], filt_coord[2]:filt_coord[3]] = 0
    fshift_back1 = np.fft.ifftshift(ffilt1)
    img_back1 = np.fft.ifft2(fshift_back1)
    img_back1 = np.real(img_back1)

    ftest_filter = np.copy(frame_diff_masked)
    ftest_filter[filt_coord[0]:filt_coord[1], filt_coord[2]:filt_coord[3]] = 255

    # grayscale to color    
    mags_bgr = cv2.cvtColor(np.astype(magnitude_spectrum, 'uint8'), cv2.COLOR_GRAY2RGB)
    frame_diff_masked_bgr = cv2.cvtColor(frame_diff_masked, cv2.COLOR_GRAY2RGB)
    ftest_filter_bgr = cv2.cvtColor(ftest_filter, cv2.COLOR_GRAY2RGB)
    img_back1 = cv2.cvtColor(np.astype(img_back1, 'uint8'), cv2.COLOR_GRAY2RGB)

    # assemble image grid
    zoom_factor = 4
    mags_y, mags_x = np.shape(mags_bgr)[:2]
    mags_bgr_zoom = cv2.resize(mags_bgr[int((mags_y/2)-((mags_y/2)/zoom_factor)):int((mags_y/2)+((mags_y/2)/zoom_factor)),
                                        int((mags_x/2)-((mags_x/2)/zoom_factor)):int((mags_x/2)+((mags_x/2)/zoom_factor))], 
                                        None, fx=zoom_factor, fy=zoom_factor)
    
    h_concat = np.concatenate((current_frame, mags_bgr), axis=1)
    h2_concat = np.concatenate((frame_diff_masked_bgr, mags_bgr_zoom), axis=1)
    h3_concat = np.concatenate((ftest_filter_bgr, img_back1), axis=1)

    hv_concat = np.concatenate((h_concat, h2_concat, h3_concat), axis=0)
    insize = np.shape(hv_concat)
    downsamp = 1
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