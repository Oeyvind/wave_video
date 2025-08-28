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
print(wavecenter_y_left, wavecenter_y_right)
mask_left = pts[0][0][0] # left top, assumes vertical left edge
mask_right = pts[1][0][0] # right top, as above

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
    #print('\npeak_indices', peak_indices)
    
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
    return current_peak_id, peak_ids, active_ids, deleted_ids

try:
    print('Starting video. Press q to exit.')
    while True:
        time_start = time.time()
        current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        previous_frame_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)    

        # diff
        frame_diff = cv2.subtract(current_frame_gray,previous_frame_gray)
        frame_diff = np.clip(frame_diff,0,255)
        frame_diff_masked = cv2.bitwise_and(frame_diff, frame_diff, mask=mask)
        frame_diff_masked = cv2.blur(frame_diff_masked, (5,5))

        # Threshold the image to find white pixels (intensity > 200)
        _, binary_img = cv2.threshold(frame_diff_masked, 5, 255, cv2.THRESH_BINARY)
        
        binary_clean = np.copy(binary_img)
        wave_img = np.zeros((dimensions[0], dimensions[1],3), np.uint8)
        
        # centroid
        centroid_1D = np.zeros(dimensions[1])
        for i in range(dimensions[1]):
            y_coords = np.nonzero(binary_img[:,i])
            if len(y_coords[0]) > 0:
                y_centroid = np.mean(y_coords)
                y_centroid = int(np.round(y_centroid))
                centroid_1D[i] = y_centroid
                if show_centroid:
                    cv2.circle(wave_img, (i,y_centroid),5, centroid_color, 1)# display centroid
        
        # fill in missing points
        x_prev = 0
        y_prev = wavecenter_y_left
        savepoint = 0
        firstpoint = [] # for filling filter padding to the left
        create_line = 0
        filter_padding = 50
        wave_1D = np.zeros(dimensions[1]+filter_padding*2)
        for i in range(dimensions[1]):
            y_value = centroid_1D[i]
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
                    wave_1D[x_prev:i] = np.reshape(line, shape=(line_len,))
                    create_line = 0
                #print('write y_value', i, y_value)
                wave_1D[i] = y_value
                y_prev = y_value
                savepoint = 0

        # fill any blank spaces at the end of the array
        for i in range(x_prev,dimensions[1]+filter_padding):
            wave_1D[i] = y_prev
        if show_fill_blanks:
            for i in range(mask_left,dimensions[1]):
                cv2.circle(wave_img, (i,int(wave_1D[i])), 3, fill_blanks_color, 1)
        
        # median filtering
        filter_size = 9
        for i in range(dimensions[1]+filter_padding-filter_size):
            wave_1D[i+int(filter_size/2)] = np.median(wave_1D[i:i+filter_size])
        filter_size = 21
        for i in range(dimensions[1]+filter_padding-filter_size):
            wave_1D[i+int(filter_size/2)]= np.median(wave_1D[i:i+filter_size])    
        if show_medianfilter:
            for i in range(mask_left,dimensions[1]):
                cv2.circle(wave_img, (i,int(wave_1D[i])), 3, medianfilter_color, 1)
        
        # lowpass
        filter_size = 50
        for i in range(dimensions[1]+(filter_padding*2)-filter_size):
            wave_1D[i+int(filter_size/2)] = np.mean(wave_1D[i:i+filter_size])
        filter_size = 50
        for i in range(dimensions[1]+(filter_padding*2)-filter_size):
            wave_1D[i+int(filter_size/2)] = np.mean(wave_1D[i:i+filter_size])
        for i in range(dimensions[1]+(filter_padding*2)-filter_size):
            wave_1D[i+int(filter_size/2)] = np.mean(wave_1D[i:i+filter_size])
        if show_lowpassfilter:
            for i in range(mask_left,dimensions[1]):
                cv2.circle(wave_img, (i,int(wave_1D[i])), 4, lowpass_color, 1)

        wave_1D = wave_1D[filter_padding:-filter_padding] # crop filter padding
                
        # find peaks
        # check center value of wave_1D, let this be zero
        # for segment where wave_1d > 0, find index of max value
        # for segment where wave_1D < 0 find index of min value
        wave_center = np.linspace(wavecenter_y_left, wavecenter_y_right, dimensions[1]) 
        sign = np.sign(wave_1D-wave_center)
        for i in range(mask_left,dimensions[1]):
            if show_wavesign:
                y = int((sign[i]*150)+wave_center[i])
                cv2.circle(wave_img, (i,y), 2, wavesign_color, 1)# display sign
            if show_wavecenter:
                cv2.circle(wave_img, (i,int(wave_center[i])), 1, wavecenter_color, 1)# display wave_center
        sign_indices = []
        signum_old = 0
        for i in range(mask_left,dimensions[1]):
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
                    # possibly must make sure that segment length is not zero here...
                    #print('segm max', sign_indices[i], sign_indices[i+1]-1, sign_indices)
                    peak = np.argmax(wave_1D[sign_indices[i]:sign_indices[i+1]-1]-wave_center[i])+sign_indices[i]
                else:
                    #print('segm min', sign_indices[i], sign_indices[i+1]-1, sign_indices)
                    peak = np.argmin(wave_1D[sign_indices[i]:sign_indices[i+1]-1]-wave_center[i])+sign_indices[i]
            else:
                if sign[sign_indices[i]] > 0:
                    peak = np.argmax(wave_1D[sign_indices[i]:]-wave_center[i])+sign_indices[i]
                else:
                    peak = np.argmin(wave_1D[sign_indices[i]:]-wave_center[i])+sign_indices[i]
            peak_indices.append(int(peak))
        
        current_peak_id, peak_ids, active_ids, deleted_ids = peak_id_following(peak_indices, peak_ids, peak_prev_ids, current_peak_id, peak_max_change, max_n_peaks, empty_id, mask_left, mask_right)
        peak_prev_ids = np.copy(peak_ids)
        
        for p in active_ids:
            peak_id, x = p
            #x = int(x)
            y = int(wave_1D[x])
            if show_peaks:
                if y > wave_center[x]:
                    cv2.circle(wave_img, (x,y),15, peakplus_color, 8)
                    cv2.putText(wave_img, f'{peak_id}', (x-20,y+45), cv2.FONT_HERSHEY_SIMPLEX, 1, peakplus_color, 2, cv2.LINE_AA)
                else:
                    cv2.circle(wave_img, (x,y),15, peaknegative_color, 8)
                    cv2.putText(wave_img, f'{peak_id}', (x-20,y-25), cv2.FONT_HERSHEY_SIMPLEX, 1, peaknegative_color, 2, cv2.LINE_AA)
                
            # send peaks to Csound
            sign = -1
            if y > wave_center[x] : sign = 1
            osc_msg = x, sign
            osc_io.sendOSC("wave_peaks", osc_msg) # send OSC back to client

        # send wave over osc to Csound
        send_counter = (send_counter+1)%4 # send only every N frame
        if send_counter == 0:
            wave_toCs = (wave_1D-wave_center)*(2/max_amp) # offset and normalize
            iscaler = len(wave_1D)/1024
            for i in range(512):
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

        # timing, frame rate
        time_now = time.time()
        processing_time = (time_now - time_start)*1000
        fps = 30
        frame_time = 1000/fps
        wait_time = int(frame_time - processing_time)
        if wait_time < 1: wait_time = 1
        #print('time', processing_time, wait_time)
        
        key = cv2.waitKey(wait_time)
        if key == ord('q'):
            break
        if key == ord('p'):
            cv2.waitKey(-1) #wait until any key is pressed

        previous_frame = current_frame.copy()
        ret, current_frame = cap.read()
        if not ret:
            break



except KeyboardInterrupt:
    cap.release()
    cv2.destroyAllWindows()
print('Done.')
print('Done.')
