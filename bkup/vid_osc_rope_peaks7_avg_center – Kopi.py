import cv2
import numpy as np 
import scipy
import imutils
import osc_io
import time
timethen = time.time()

cap = cv2.VideoCapture("rope_2.mp4")
ret, current_frame = cap.read()
previous_frame = current_frame
dimensions = current_frame.shape
print(dimensions)
mask = np.zeros(dimensions[:2], dtype="uint8")
pts = np.array([[int(dimensions[1]*0.15),int(dimensions[0]*0.45)],
                [int(dimensions[1]*0.95),int(dimensions[0]*0.45)],
                [int(dimensions[1]*0.95),int(dimensions[0]*0.999)],
                [int(dimensions[1]*0.15),int(dimensions[0]*0.8)]], np.int32)
max_amp = np.max(pts[:,1])-np.min(pts[:,1])
pts = pts.reshape((-1,1,2))
polyg = cv2.fillPoly(mask,pts=[pts],color=255)
# print mask center y left and center y right
print(pts[0][0][1],pts[3][0][1])
wavecenter_y_left = np.max([pts[0][0][1],pts[3][0][1]]) - int(abs(pts[0][0][1]-pts[3][0][1])*0.5)
wavecenter_y_right = np.max([pts[1][0][1],pts[2][0][1]]) - int(abs(pts[1][0][1]-pts[2][0][1])*0.5)
print('wavecenter', wavecenter_y_left, wavecenter_y_right)
mask_left = pts[0][0][0] # left top, assumes vertical left edge
mask_right = pts[1][0][0] # right top, as above
print('mask LR', mask_left, mask_right)
send_counter = 0

empty_id = 9999
max_n_peaks = 99
peak_ids = np.zeros(max_n_peaks)
peak_ids += empty_id
peak_prev_ids = np.zeros(max_n_peaks)
peak_prev_ids += empty_id
current_peak_id = 0
peak_max_change = 50

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

centroid_color = purple
fill_blanks_color = yellow
medianfilter_color = green
lowpass_color = orange
wavecenter_color = dull_green
wavesign_color = dull_red
peaknegative_color = red
peakplus_color = green

show_centroid = False
show_fill_blanks = False
show_medianfilter = False
show_lowpassfilter = True
show_wavecenter = True
show_wavesign = False
show_mask = True
show_peaks = True

def peak_id_following(peak_indices, peak_ids, peak_prev_ids, current_peak_id, peak_max_change, max_n_peaks, empty_id, mask_left, mask_right):
    '''
    For a collection of peak indices (x-positions),
    give each peak an ID, and let that ID follow the peak when it moves (within a threshold).
    New peaks get a new ID, and peaks that disappear are deleted.
    Peaks outside the min max range are discarded.
    Output a list of currently active (peak,ID), and a list of deleted peak IDs
    '''    
    print('\npeak_indices', peak_indices)
    print('peak id following', np.where(peak_ids < empty_id), np.where(peak_prev_ids < empty_id))
    peak_id_copy = np.copy(peak_ids)
    remove_outside_range = []
    for i in range(len(peak_indices)):
        if peak_indices[i] > mask_right:
            remove_outside_range.append(i)
        if peak_indices[i] < mask_left:
            remove_outside_range.append(i)
    remove_outside_range.sort(reverse=True)
    for i in remove_outside_range:
        del peak_indices[i]

    deleted_ids = []
    new_ids = []
    continued_ids = []
    for p in peak_indices:
        current_peak_id = current_peak_id % max_n_peaks
        if np.min(peak_prev_ids) == empty_id: # if no previous ids, just write new ones
            #print(p,'peak ids empty, write new')
            peak_ids[current_peak_id] = p
            new_ids.append((current_peak_id,p))
            current_peak_id += 1
        else:
            index = np.abs(peak_prev_ids - p).argmin() # find closest
            if abs(peak_ids[index]-p) < peak_max_change:
                #print(p, 'update peak id', index, 'at', peak_prev_ids[index])
                peak_ids[index] = p # if within range, update the old one
                continued_ids.append((int(index),p))
            else:
                #print(p, 'make new peak')
                peak_ids[current_peak_id] = p # otherwise, make a new id
                new_ids.append((current_peak_id,p))
                current_peak_id += 1
    for i in range(len(peak_ids)):
        peak_ndx = peak_ids[i]
        if peak_ndx not in peak_indices: # when a peak disappears (or moves out of range), delete it
            peak_ids[i] = empty_id
            if peak_ndx < empty_id:
                #print(peak_ndx, 'deleted peak')
                deleted_ids.append(i)
    #print('new', new_ids, 'continued', continued_ids, 'deleted', deleted_ids)
    active_ids = new_ids
    for item in continued_ids:
        active_ids.append(item)
    peak_prev_ids = peak_id_copy
    return current_peak_id, peak_ids, peak_prev_ids, active_ids, deleted_ids

def find_center_wave(wave_1D):
    '''find center line of 1D wave'''
    length = len(wave_1D)
    center_wave = np.zeros(length)
    mean_0 = np.mean(wave_1D)
    mean_21 = np.mean(wave_1D[:int(length/2)])
    mean_22 = np.mean(wave_1D[int(length/2):])
    mean_61 = np.mean(wave_1D[:int(length/6)])
    mean_62 = np.mean(wave_1D[int(length*(1/6)):int(length*(2/6))])
    mean_63 = np.mean(wave_1D[int(length*(2/6)):int(length*(3/6))])
    mean_64 = np.mean(wave_1D[int(length*(3/6)):int(length*(4/6))])
    mean_65 = np.mean(wave_1D[int(length*(4/6)):int(length*(5/6))])
    mean_66 = np.mean(wave_1D[int(length*(5/6)):])
    center_wave += mean_0
    center_wave[:int(length/2)] += ((mean_21-mean_0)/3)
    center_wave[int(length/2):] += ((mean_22-mean_0)/3)
    center_wave[:int(length/6)] += ((mean_61-mean_0)/3)
    center_wave[int(length*(1/6)):int(length*(2/6))] += ((mean_62-mean_0)/3)
    center_wave[int(length*(2/6)):int(length*(3/6))] += ((mean_63-mean_0)/3)
    center_wave[int(length*(3/6)):int(length*(4/6))] += ((mean_64-mean_0)/3)
    center_wave[int(length*(4/6)):int(length*(5/6))] += ((mean_65-mean_0)/3)
    center_wave[int(length*(5/6)):] += ((mean_66-mean_0)/3)
    # Simple moving average kernel
    kernel_size = int(length/12)
    kernel = np.ones(kernel_size) / kernel_size
    # Apply convolution
    center_wave = np.convolve(center_wave, kernel, mode='full')[:length]#+int(kernel_size/2)]
    return center_wave

def find_center_wave_regr(wave_1D, mask_left, mask_right):
    x = np.arange(0,len(wave_1D[mask_left:mask_right]),1)
    m, c = np.polyfit(x, wave_1D[mask_left:mask_right], 1)
    #print(x, wave_1D, m,c)
    regr = np.linspace(c,c+len(wave_1D[mask_left:mask_right])*m,len(wave_1D[mask_left:mask_right]))
    centr = np.zeros(len(wave_1D))
    centr[:mask_left] = regr[0]
    centr[mask_left:mask_right] = regr
    centr[mask_right:] = regr[-1]
    return centr

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

def find_peaks(input_1D, center_wave, left_limit, right_limit, show_wavesign, wavesign_color, show_wavecenter, wavecenter_color):
    # check center value of wave_1D, let this be zero
    # for segment where wave_1d > 0, find index of max value
    # for segment where wave_1D < 0 find index of min value
    #wave_center = np.linspace(wavecenter_y_left, wavecenter_y_right, dimensions[1]) 
    sign = np.sign(input_1D-center_wave)
    for i in range(left_limit,right_limit):
        if show_wavesign:
            y = int((sign[i]*150)+center_wave[i])
            cv2.circle(wave_img, (i,y), 2, wavesign_color, 1)# display sign
        if show_wavecenter:
            cv2.circle(wave_img, (i,int(center_wave[i])), 1, wavecenter_color, 1)# display wave_center
    sign_indices = []
    signum_old = 0
    for i in range(left_limit,right_limit):
        signum = sign[i]
        if signum != signum_old:
            sign_indices.append(i)
        signum_old = signum
    peak_indices = []
    remove_one_apart = []
    sign_old = 0
    for s in sign_indices:
        if s == sign_old+1:
            remove_one_apart.append(s)
        sign_old = s
    for s in remove_one_apart:
        sign_indices.remove(s)
    for i in range(len(sign_indices)):
        if i < len(sign_indices)-1:
            if sign[sign_indices[i]] > 0:
                peak = np.argmax(wave_1D[sign_indices[i]:sign_indices[i+1]-1]-center_wave[i])+sign_indices[i]
            else:
                peak = np.argmin(wave_1D[sign_indices[i]:sign_indices[i+1]-1]-center_wave[i])+sign_indices[i]
        else:
            if sign[sign_indices[i]] > 0:
                peak = np.argmax(wave_1D[sign_indices[i]:]-center_wave[i])+sign_indices[i]
            else:
                peak = np.argmin(wave_1D[sign_indices[i]:]-center_wave[i])+sign_indices[i]
        peak_indices.append(int(peak))
    return peak_indices

def display_peaks(active_ids, center_wave, input_1D, output_img, show_peaks, peakplus_color, peaknegative_color):
    for p in active_ids:
        peak_id, x = p
        y = int(input_1D[x])
        x += 50 #ad hoc
        if show_peaks:
            if y > center_wave[x]:
                cv2.circle(output_img, (x,y),15, peakplus_color, 8)
                cv2.putText(output_img, f'{peak_id}', (x-20,y+45), cv2.FONT_HERSHEY_SIMPLEX, 1, peakplus_color, 2, cv2.LINE_AA)
            else:
                cv2.circle(output_img, (x,y),15, peaknegative_color, 8)
                cv2.putText(output_img, f'{peak_id}', (x-20,y-25), cv2.FONT_HERSHEY_SIMPLEX, 1, peaknegative_color, 2, cv2.LINE_AA) 

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
        # find centroid, disambiguation of rope trace
        centroid_1D = centroid_1D_from_img(binary_img, wave_img, show_centroid, centroid_color)
        # fill in any blanks in the wave
        filter_padding = 50
        wave_1D = np.zeros(dimensions[1]+filter_padding*2)
        wave_1D = fill_in_missing_points(wavecenter_y_left, centroid_1D, wave_1D, wave_img, show_fill_blanks, fill_blanks_color)
        # median filtering
        filter_size1 = 9
        filter_size2 = 21
        wave_1D = median_1D(wave_1D, filter_padding, filter_size1, filter_size2, wave_img, show_medianfilter, medianfilter_color)
        # lowpass
        filter_size1 = 40
        filter_size2 = 50
        wave_1D = lowpass_1D(wave_1D, wave_img, filter_padding, filter_size1, filter_size2, show_lowpassfilter, lowpass_color)
        # crop filter padding
        wave_1D = wave_1D[filter_padding:-filter_padding] 

        # find center, average over sections                
        center_wave = find_center_wave_regr(wave_1D, mask_left, mask_right)
        # find peaks and peak ids
        peak_indices = find_peaks(wave_1D, center_wave, mask_left, dimensions[1], show_wavesign, wavesign_color, show_wavecenter, wavecenter_color)
        current_peak_id, peak_ids, peak_prev_ids, active_ids, deleted_ids = peak_id_following(peak_indices, peak_ids, peak_prev_ids, current_peak_id, peak_max_change, max_n_peaks, empty_id, mask_left, mask_right)
        display_peaks(active_ids, center_wave, wave_1D, wave_img, show_peaks, peakplus_color, peaknegative_color)
        
        # peak parms and stats
        active_ids_a = np.array(active_ids)
        numpeaks = len(active_ids)
        if numpeaks > 0 :
            active_ids_sorted = active_ids_a[np.argsort(active_ids_a[:,1])] # sort by ascending x
            if numpeaks > 1:
                avg_x_distance = (active_ids_sorted[-1][1]-active_ids_sorted[0][1])/(numpeaks-1)
            else: 
                avg_x_distance = active_ids_sorted[0][1]
            #print(f'P num {numpeaks} dist {avg_x_distance}')
            # send peaks summary to Csound
            osc_msg = numpeaks, avg_x_distance
            osc_io.sendOSC('peaks_summary', osc_msg) # send OSC back to client

            x_prev = 0
            y_prev = 0 
            avg_x_movement = 0
            for p in active_ids_sorted:
                peak_id, x = p
                x_movement = x-x_prev
                avg_x_movement += x_movement
                x_prev = x
                y = (wave_1D[x]-center_wave[x])/max_amp
                peak_amp = abs(y-y_prev)
                y_prev = y
                #print(f'p {peak_id}, x {x}, xd {x_distance} amp {peak_amp}')

                # send peaks to Csound
                osc_msg = float(peak_id), float(x), float(y), float(peak_amp), float(x_movement)
                osc_io.sendOSC('active_peaks', osc_msg) # send OSC back to client
            for peak_id in deleted_ids:
                osc_msg = float(peak_id)
                osc_io.sendOSC('deleted_peaks', osc_msg) # send OSC back to client
            print('active', active_ids_sorted[:,0])
            print('delete', deleted_ids)
            # send peaks summary to Csound
            avg_x_movement /= numpeaks
            osc_msg = numpeaks, avg_x_distance, float(avg_x_movement)
            osc_io.sendOSC('peaks_summary', osc_msg) # send OSC back to client
        
        # send wave over osc to Csound
        send_counter = (send_counter+1)%8 # send only every N frame
        if send_counter == 0:
            wave_toCs = (wave_1D-center_wave)*(2/max_amp) # offset and normalize
            iscaler = len(wave_1D)/1024
            for i in range(1024):
                y = int(i*iscaler)
                osc_msg = i, wave_toCs[y]
                osc_io.sendOSC("wave_video", osc_msg) # send OSC back to client
        
        # Display result
        output = cv2.add(current_frame, wave_img)    
        if show_mask:
            polyg_show = cv2.polylines(output,pts=[pts],isClosed=True, color=(255,0,0),thickness=2)
        size_ = 640
        scale = size_/np.shape(output)[1] # data array shape is y,x
        size = (size_,int(np.shape(output)[0]*scale))
        # add labels
        v_offset = 20
        legend_x = 15
        legend_y = 15
        if show_centroid:
            cv2.circle(output, (legend_x,legend_y), 4, centroid_color, 4)
            cv2.putText(output, 'centroid', (legend_x+15,legend_y+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, centroid_color, 1, cv2.LINE_AA)
            legend_y += v_offset
        if show_fill_blanks:
            cv2.circle(output, (legend_x,legend_y), 4, fill_blanks_color, 4)
            cv2.putText(output, 'fill', (legend_x+15,legend_y+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, fill_blanks_color, 1, cv2.LINE_AA)
            legend_y += v_offset
        if show_medianfilter:
            cv2.circle(output, (legend_x,legend_y), 4, medianfilter_color, 4)
            cv2.putText(output, 'median', (legend_x+15,legend_y+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, medianfilter_color, 1, cv2.LINE_AA)
            legend_y += v_offset
        if show_lowpassfilter:
            cv2.circle(output, (legend_x,legend_y), 4, lowpass_color, 4)
            cv2.putText(output, 'lowpass', (legend_x+15,legend_y+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, lowpass_color, 1, cv2.LINE_AA)
            legend_y += v_offset
        if show_wavecenter:
            cv2.circle(output, (legend_x,legend_y), 4, wavecenter_color, 4)
            cv2.putText(output, 'centerline', (legend_x+15,legend_y+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, wavecenter_color, 1, cv2.LINE_AA)
            legend_y += v_offset
        if show_wavesign:
            cv2.circle(output, (legend_x,legend_y), 4, wavesign_color, 4)
            cv2.putText(output, 'wavesign', (legend_x+15,legend_y+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, wavesign_color, 1, cv2.LINE_AA)
            legend_y += v_offset
        output = cv2.resize(output, size)
        cv2.imshow("Rope", output)
        previous_frame = current_frame.copy()
        ret, current_frame = cap.read()
        if not ret:
            break

        # timing, frame rate
        time_now = time.time()
        processing_time = (time_now - time_start)*1000
        fps = 4
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
print('Done.')
