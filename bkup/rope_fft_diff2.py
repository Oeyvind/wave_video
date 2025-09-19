import cv2
import numpy as np
from matplotlib import pyplot as plt

cap = cv2.VideoCapture("rope_2.mp4")#rope_ximea_1.mp4")
ret, current_frame = cap.read()
current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
previous_gray = np.copy(current_gray)
dimensions = current_frame.shape

mask1 = np.zeros(current_frame.shape[:2], dtype="uint8")
pts = np.array([[250,300],[1260,300],[1260,750],[250,500]], np.int32)
pts = pts.reshape((-1,1,2))
polyg = cv2.fillPoly(mask1,pts=[pts],color=255)

wavecenter_y_left = np.max([pts[0][0][1],pts[3][0][1]]) - int(abs(pts[0][0][1]-pts[3][0][1])*0.5)
wavecenter_y_right = np.max([pts[1][0][1],pts[2][0][1]]) - int(abs(pts[1][0][1]-pts[2][0][1])*0.5)
mask_left = pts[0][0][0] # left top, assumes vertical left edge
mask_right = pts[1][0][0] # right top, as above

blank = np.zeros_like(current_frame)

def centroid_1D_from_img(input_img, output_img, show_centroid, centroid_color):
    # centroid
    centroid_1D = np.zeros(dimensions[1])
    for i in range(dimensions[1]):
        y_coords = np.nonzero(input_img[:,i])
        if len(y_coords[0]) > 0:
            y_centroid = np.mean(y_coords)
            y_centroid = int(np.round(y_centroid))
            centroid_1D[i] = y_centroid
            if show_centroid:
                cv2.circle(output_img, (i,y_centroid),5, centroid_color, 1)# display centroid
    return centroid_1D

def fill_in_missing_points(y_init, input_1D, output_1D, output_img, show_fill_blanks, fill_blanks_color):
    # fill in missing points
    x_prev = 0
    y_prev = y_init
    savepoint = 0
    firstpoint = [] # for filling filter padding to the left
    create_line = 0
    for i in range(dimensions[1]):
        y_value = input_1D[i]
        if y_value == 0:
            if savepoint == 0:
                x_prev = i
                create_line = 1
            savepoint = 1
        else: 
            if firstpoint == []: 
                firstpoint = [i,y_value]
            if create_line > 0:
                line_len = i-x_prev
                line = np.linspace(y_prev, y_value, line_len)
                #print('create_line', i, y_prev, y_value)
                output_1D[x_prev:i] = np.reshape(line, shape=(line_len,))
                create_line = 0
            #print('write y_value', i, y_value)
            output_1D[i] = y_value
            y_prev = y_value
            savepoint = 0
    # fill any blank spaces at the end of the array
    for i in range(x_prev,dimensions[1]+filter_padding):
        output_1D[i] = y_prev
    if show_fill_blanks:
        for i in range(mask_left,dimensions[1]):
            cv2.circle(output_img, (i,int(output_1D[i])), 3, fill_blanks_color, 1)
    return output_1D

def median_1D(input_1D, filter_padding, filter_size1, filter_size2, output_img, show_medianfilter, medianfilter_color):
    # median filtering
    for i in range(dimensions[1]+filter_padding-filter_size1):
        input_1D[i+int(filter_size1/2)] = np.median(input_1D[i:i+filter_size1])
    for i in range(dimensions[1]+filter_padding-filter_size2):
        input_1D[i+int(filter_size2/2)]= np.median(input_1D[i:i+filter_size2])    
    if show_medianfilter:
        for i in range(mask_left,dimensions[1]):
            cv2.circle(output_img, (i,int(wave_1D[i])), 3, medianfilter_color, 1)
    return input_1D

def lowpass_1D(input_1D, output_img, filter_padding, filter_size1, filter_size2, show_lowpassfilter, lowpass_color):
    # lowpass
    for i in range(dimensions[1]+(filter_padding*2)-filter_size1):
        input_1D[i+int(filter_size1/2)] = np.mean(input_1D[i:i+filter_size1])
    for i in range(dimensions[1]+(filter_padding*2)-filter_size2):
        input_1D[i+int(filter_size2/2)] = np.mean(input_1D[i:i+filter_size2])
    if show_lowpassfilter:
        for i in range(mask_left,dimensions[1]):
            cv2.circle(output_img, (i,int(input_1D[i])), 4, lowpass_color, 1)
    return input_1D



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
    print(np.shape(frame_diff_masked), np.shape(fdm_thresh))    
    #fdm_thresh = cv2.adaptiveThreshold(frame_diff_masked,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    
    # 1D wave, find centroid, fill in blanks, filter
    _, binary_img = cv2.threshold(frame_diff_masked, 5, 255, cv2.THRESH_BINARY)
    # output img for display of curves
    wave_img = np.zeros((dimensions[0], dimensions[1],3), np.uint8)
    # find centroid, disambiguation of rope trace
    show_centroid = False
    centroid_color = (255,0,0)
    centroid_1D = centroid_1D_from_img(binary_img, wave_img, show_centroid, centroid_color)
    # fill in any blanks in the wave
    filter_padding = 50
    wave_1D = np.zeros(dimensions[1]+filter_padding*2)
    show_fill_blanks = False
    fill_blanks_color = (255,255,255)
    wave_1D = fill_in_missing_points(wavecenter_y_left, centroid_1D, wave_1D, wave_img, show_fill_blanks, fill_blanks_color)
    # median filtering
    filter_size1 = 9
    filter_size2 = 21
    show_medianfilter = False
    medianfilter_color = (255,255,255)
    wave_1D = median_1D(wave_1D, filter_padding, filter_size1, filter_size2, wave_img, show_medianfilter, medianfilter_color)
    # lowpass
    filter_size1 = 40
    filter_size2 = 50
    show_lowpassfilter = True
    lowpass_color = (255,255,255)
    wave_1D = lowpass_1D(wave_1D, wave_img, filter_padding, filter_size1, filter_size2, show_lowpassfilter, lowpass_color)

    # show mask
    polyg_show = cv2.polylines(current_frame,pts=[pts],isClosed=True, color=(255,0,0),thickness=2)

    # fft
    f = np.fft.fft2(frame_diff_masked)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20*np.log(np.abs(fshift))

    wave_img_gray = cv2.cvtColor(wave_img, cv2.COLOR_BGR2GRAY)
    f2 = np.fft.fft2(wave_img_gray)
    fshift2 = np.fft.fftshift(f2)
    magnitude_spectrum2 = 20*np.log(np.abs(fshift2))

    # grayscale to color    
    mags_bgr = cv2.cvtColor(np.astype(magnitude_spectrum, 'uint8'), cv2.COLOR_GRAY2RGB)
    mags_bgr2 = cv2.cvtColor(np.astype(magnitude_spectrum2, 'uint8'), cv2.COLOR_GRAY2RGB)
    frame_diff_masked_bgr = cv2.cvtColor(frame_diff_masked, cv2.COLOR_GRAY2RGB)
    fdm_thresh_masked_bgr = cv2.cvtColor(fdm_thresh, cv2.COLOR_GRAY2RGB)
    
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
    h3_concat = np.concatenate((wave_img, mags_bgr_zoom2), axis=1)
    
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