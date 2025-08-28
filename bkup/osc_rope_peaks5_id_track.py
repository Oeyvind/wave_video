import cv2
import numpy as np 
import math
#import imutils
import osc_io

# Open the video file
cap = cv2.VideoCapture("rope_2.mp4")
ret, current_frame = cap.read()
previous_frame = current_frame
dimensions = current_frame.shape
print(dimensions)
mask = np.zeros(current_frame.shape[:2], dtype="uint8")
pts = np.array([[250,300],[1260,300],[1260,750],[250,500]], np.int32)
max_amp = np.max(pts[:,1])-np.min(pts[:,1])
pts = pts.reshape((-1,1,2))
polyg = cv2.fillPoly(mask,pts=[pts],color=255)

send_counter = 0
empty_id = 9999
max_peaks = 30
peak_ids = np.zeros(max_peaks)
peak_ids += empty_id
peak_prev_ids = np.zeros(max_peaks)
peak_prev_ids += empty_id
peak_id = 0

while(cap.isOpened()):
    current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    previous_frame_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)    

    # diff
    frame_diff = cv2.absdiff(current_frame_gray,previous_frame_gray)
    frame_diff_masked = cv2.bitwise_and(frame_diff, frame_diff, mask=mask)
    frame_diff = cv2.blur(frame_diff, (10,10))
    frame_diff_masked = cv2.blur(frame_diff_masked, (10,10))

    # Threshold the image to find white pixels (intensity > 200)
    _, binary_img = cv2.threshold(frame_diff_masked, 10, 255, cv2.THRESH_BINARY)
    
    # centroid
    for i in range(dimensions[1]):
        new = np.zeros(dimensions[0])
        y_coords = np.nonzero(binary_img[:,i])
        if len(y_coords[0]) > 0:
            y_centroid = np.mean(y_coords)        
            y_centroid = int(np.round(y_centroid))
            new[y_centroid] = 255
        binary_img[:,i] = new

    # fill in missing points
    x_prev = 0
    y_prev = 450
    savepoint = 0
    firstpoint = [] # for filling filter padding to the left
    create_line = 0
    filter_padding = 50
    wave_1D = np.zeros(dimensions[1]+filter_padding*2)
    for i in range(dimensions[1]):
        y_value = np.nonzero(binary_img[:,i])[0]
        if len(y_value) == 0:
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
                wave_1D[x_prev+filter_padding:i+filter_padding] = np.reshape(line, shape=(line_len,))
                create_line = 0
            wave_1D[i+filter_padding] = y_value[0]
            y_prev = y_value[0]
            savepoint = 0
    # fill any blank spaces at the end of the array
    for i in range(x_prev-filter_padding,dimensions[1]):
        wave_1D[i+filter_padding*2] = y_prev
    if len(firstpoint) > 0:
        wave_1D[:firstpoint[0]] = firstpoint[1]

    # median filtering
    filter_size = 5
    for i in range(dimensions[1]+(filter_padding*2)-filter_size):
        wave_1D[i+int(filter_size/2)] = np.median(wave_1D[i:i+filter_size])
    filter_size = 43
    for i in range(dimensions[1]+(filter_padding*2)-filter_size):
        wave_1D[i+int(filter_size/2)]= np.median(wave_1D[i:i+filter_size])
    # lowpass
    filter_size = 25
    for i in range(dimensions[1]+(filter_padding*2)-filter_size):
        wave_1D[i+int(filter_size/2)] = np.mean(wave_1D[i:i+filter_size])
    filter_size = 45
    for i in range(dimensions[1]+(filter_padding*2)-filter_size):
        wave_1D[i+int(filter_size/2)] = np.mean(wave_1D[i:i+filter_size])
    for i in range(dimensions[1]+(filter_padding*2)-filter_size):
        wave_1D[i+int(filter_size/2)] = np.mean(wave_1D[i:i+filter_size])
    wave_1D = wave_1D[filter_padding:-filter_padding] # crop filter padding

    # write the wave to image for display
    wave_img = binary_img.copy()
    for i in range(200,dimensions[1]):
        new = np.zeros(dimensions[0])
        new[int(wave_1D[i])] = 255
        wave_img[:,i] = new
    kernel = np.ones((5, 5),np.uint8)
    wave_img = cv2.dilate(wave_img, kernel, iterations=2)

    # convert to color, to display peaks
    wave_img_col = cv2.cvtColor(wave_img, cv2.COLOR_GRAY2BGR)
    frame_col = cv2.cvtColor(current_frame_gray, cv2.COLOR_GRAY2BGR)

    # find peaks
    # alt method
    # check center value of wave_1D, get zero
    # for segment where wave_1d > 0, find index of max value
    # for segment where wave_1D < 0 find index of min value
    # print(np.mean(wave_1D))
    wave_center = np.linspace(430, 520, dimensions[1]) 
    sign = np.sign(wave_1D-wave_center)
    for i in range(200,dimensions[1]):
        y = int((sign[i]*150)+wave_center[i])
        #print('xy',x,y)
        cv2.circle(wave_img_col, (i,y),2, (255,0,0), 1)# display sign
        cv2.circle(wave_img_col, (i,int(wave_center[i])),1, (0,255,0), 1)# display wave_center
    
    sign_indices = []
    signum_old = 0
    for i in range(200,dimensions[1]):
        signum = sign[i]
        if signum != signum_old:
            sign_indices.append(i)
        signum_old = signum
    peak_indices = []
    #print(sign_indices)
    for i in range(len(sign_indices)):
        #print('sign',sign_indices[i],sign[sign_indices[i]])
        if i < len(sign_indices)-1:
            if sign[sign_indices[i]] > 0:
                peak = np.argmax(wave_1D[sign_indices[i]:sign_indices[i+1]-1]-wave_center[i])+sign_indices[i]
            else:
                peak = np.argmin(wave_1D[sign_indices[i]:sign_indices[i+1]-1]-wave_center[i])+sign_indices[i]
        else:
            if sign[sign_indices[i]] > 0:
                peak = np.argmax(wave_1D[sign_indices[i]:]-wave_center[i])+sign_indices[i]
            else:
                peak = np.argmin(wave_1D[sign_indices[i]:]-wave_center[i])+sign_indices[i]
        #print('peak',peak,sign[sign_indices[i]])
        peak_indices.append(peak)
    #print('peak_indices', peak_indices)
    # housekeeping new, continued, and discarded ids
    deleted_ids = []
    new_ids = []
    continued_ids = []
    peak_max_change = 50
    for p in peak_indices:
        peak_id = peak_id % max_peaks
        if np.min(peak_prev_ids) == empty_id: # if no previous ids, just write new ones
            peak_ids[peak_id] = p
            new_ids.append(peak_id)
            peak_id += 1
        else:
            index = np.abs(peak_prev_ids - p).argmin() # find closest
            if abs(peak_ids[index]-p) < peak_max_change:
                peak_ids[index] = p # if within range, update the old one
                continued_ids.append(int(index))
            else:
                peak_ids[peak_id] = p # otherwise, make a new id
                new_ids.append(peak_id)
                peak_id += 1
    for i in range(len(peak_ids)):
        peak_ndx = peak_ids[i]
        if peak_ndx not in peak_indices: # when a peak disappears (or moves out of range), delete it
            peak_ids[i] = empty_id
            if peak_ndx < empty_id:
                deleted_ids.append(i)
    ##print('new', new_ids, 'continued', continued_ids, 'deleted', deleted_ids)
    peak_prev_ids = np.copy(peak_ids)
    ##for i in range(len(peak_ids)):
        ##if peak_ids[i] < empty_id:
            ##print(peak_ids[i],i)


    for p in peak_indices:
        y = int(wave_1D[p])
        #print('peak',p,y)
        if y > wave_center[p]:
            cv2.circle(wave_img_col, (p,y),15, (0,0,255), 8)
        else:
            cv2.circle(wave_img_col, (p,y),15, (0,255,0), 8)
        # send peaks to Csound
        if p < dimensions[1]-1:
            sign = -1
            if y > wave_center[p] : sign = 1
            osc_msg = int(p), sign
            osc_io.sendOSC("wave_peaks", osc_msg) # send OSC back to client
    
    # send wave over osc to Csound
    send_counter = (send_counter+1)%6 # send only every N frame
    if send_counter == 0:
        wave_toCs = (wave_1D-wave_center)*(2/max_amp) # offset and normalize
        #in_array = np.linspace(0, np.pi*2, len(wave_1D))
        #wave_toCs = np.sin(in_array)*150
        iscaler = len(wave_1D)/1024
        
        for i in range(1024):
            y = int(i*iscaler)
            osc_msg = i, wave_toCs[y]
            osc_io.sendOSC("wave_video", osc_msg) # send OSC back to client


    # Display result
    size = (1200,700) # (300,200)
    resized_image = cv2.resize(cv2.add(wave_img_col, frame_col), size)
    cv2.imshow("Rope", resized_image)
    
    key = cv2.waitKey(30)
    if key == ord('q'):
        break
    if key == ord('p'):
        cv2.waitKey(-1) #wait until any key is pressed

    previous_frame = current_frame.copy()
    ret, current_frame = cap.read()
    if not ret:
        break


cap.release()
cv2.destroyAllWindows()