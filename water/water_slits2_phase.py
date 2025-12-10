import cv2
import numpy as np 
from scipy.fft import rfft,rfftfreq
import osc_io

# Open the video file
#cap = cv2.VideoCapture("Nidelv_brygger3.mp4")
cap = cv2.VideoCapture("dokkpark_2025_10.mp4")
ret, current_frame = cap.read()
dimensions = current_frame.shape
size_ = 512
scale = size_/np.shape(current_frame)[1] # data array shape is y,x
size = (int(np.shape(current_frame)[0]*scale), size_)
rsize = (size[1],size[0])
current_frame = cv2.resize(current_frame, rsize)
print('dimensions input', dimensions, 'size', size)
previous_frame = current_frame
previous_frame_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)    
previous_frame_screen = np.copy(previous_frame_gray)
prev_frame_float = previous_frame_gray.astype(np.float32)
step = False

def screen_blend_self(base_img):
    base_float = base_img.astype(np.float32) / 255.0
    result_float = 1 - ((1 - base_float) * (1 - base_float))
    result_img = (result_float * 255).astype(np.uint8)
    return result_img

def lowpass_over_time(current_frame, alpha, prev_frame_float):
    # lowpass video over time, alpha is lowpass coefficient (low=long)
    current_frame_float = current_frame.astype(np.float32)
    filtered_frame_float = alpha * current_frame_float + (1 - alpha) * prev_frame_float
    filtered_frame_display = filtered_frame_float.astype(np.uint8)
    prev_frame_float = filtered_frame_float
    return filtered_frame_display, prev_frame_float

while(cap.isOpened()):
    current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

    # Lowpass over time
    current_frame_gray = cv2.blur(current_frame_gray, (6,6))
    current_frame_screen = screen_blend_self(current_frame_gray)
    alpha = 0.02
    filtered_frame_display, prev_frame_float = lowpass_over_time(current_frame_gray, alpha, prev_frame_float)
    frame_diff_filt = cv2.subtract(current_frame_gray,filtered_frame_display) 

    # contrast, brightness
    #alpha = 0.8  # Contrast control (1.0 for no change)
    #beta = -50    # Brightness control (positive for brighter, negative for darker)
    #current_frame_dark = cv2.convertScaleAbs(current_frame_gray, alpha=alpha, beta=beta)
    #current_frame_dark = screen_blend_self(current_frame_dark)

    #current_frame_screen = screen_blend_self(current_frame_gray)
    #frame_diff = cv2.subtract(current_frame_gray,previous_frame_gray) 
    #frame_diff_screen = cv2.subtract(current_frame_screen,previous_frame_screen)
    #previous_frame_screen =  current_frame_screen
    output = frame_diff_filt#cv2.add(current_frame_dark, frame_diff_filt)
    output_bgr = cv2.cvtColor(output, cv2.COLOR_GRAY2BGR)

    # slit
    y_first = 0.5
    wave_height = size[0]* 0.2
    y_pos = int(size[0]* y_first)
    slit = output[y_pos,:]
    
    # FFT
    fft_size = size[1]
    fft_sr = 1/fft_size
    yf = rfft(slit)
    angles = np.angle(yf)
    yf = np.pow(2.0/fft_size * np.abs(yf),2)
    xf = rfftfreq(fft_size, fft_sr)
    
    centr_range1 = [1, 5] # skip DC
    centr_range2 = [4, 25]
    centr_range3 = [25, 50]
    centr_range4 = [40, 100]
    #centr_sumamp = np.sum(yf[centr_range1[0]:centr_range4[1]])
    centr_maxamp = np.max(yf[centr_range1[0]:centr_range4[1]])
    centr1_maxamp = np.max(yf[centr_range1[0]:centr_range1[1]])/centr_maxamp
    centr2_maxamp = np.max(yf[centr_range2[0]:centr_range2[1]])/centr_maxamp
    centr3_maxamp = np.max(yf[centr_range3[0]:centr_range3[1]])/centr_maxamp
    centr4_maxamp = np.max(yf[centr_range4[0]:centr_range4[1]])/centr_maxamp
    
    centr1 = (np.sum(xf[centr_range1[0]:centr_range1[1]]*yf[centr_range1[0]:centr_range1[1]])/np.sum(yf[centr_range1[0]:centr_range1[1]]))
    centr2 = (np.sum(xf[centr_range2[0]:centr_range2[1]]*yf[centr_range2[0]:centr_range2[1]])/np.sum(yf[centr_range2[0]:centr_range2[1]]))
    centr3 = (np.sum(xf[centr_range3[0]:centr_range3[1]]*yf[centr_range3[0]:centr_range3[1]])/np.sum(yf[centr_range3[0]:centr_range3[1]]))
    centr4 = (np.sum(xf[centr_range4[0]:centr_range4[1]]*yf[centr_range4[0]:centr_range4[1]])/np.sum(yf[centr_range4[0]:centr_range4[1]]))
    #print(centr1, centr2)

    angle2_maxbin = angles[np.argmax(xf[centr_range2[0]:centr_range2[1]])+centr_range2[0]]
    angle2_avg = np.sum(angles[centr_range2[0]:centr_range2[1]])

    show_mask = True
    show_wave = True
    show_fft = True
    send_wave = True
    if show_mask:
        pts = np.array([[0,y_pos-2], [size[1],y_pos-2],
                        [size[1],y_pos+2],[0,y_pos+2]], np.int32)
        pts = pts.reshape((-1,1,2))
        polyg_show = cv2.polylines(output_bgr,pts=[pts],isClosed=True, color=(255,0,0), thickness=1)
    if show_fft:
        txt_color = (0,255,255)
        legend_x = 10
        legend_y = 15
        cv2.rectangle(output_bgr, (legend_x-5,legend_y-20), (legend_x+250,legend_y+80), (0,0,0), cv2.FILLED)        
        cv2.putText(output_bgr, f'centr_Lo: {centr1:.2f} amp {centr1_maxamp:.2f}', (legend_x,legend_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, txt_color, 1, cv2.LINE_AA)
        legend_y += 25
        cv2.putText(output_bgr, f'centr_Mid: {centr2:.2f} amp {centr2_maxamp:.2f} angmax {angle2_maxbin:.2f} angavg {angle2_avg:.2f}', (legend_x,legend_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, txt_color, 1, cv2.LINE_AA)
        legend_y += 25
        cv2.putText(output_bgr, f'centr_Ripple: {centr3:.2f} amp {centr3_maxamp:.2f}', (legend_x,legend_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, txt_color, 1, cv2.LINE_AA)
        legend_y += 25
        cv2.putText(output_bgr, f'centr_Nois: {centr4:.2f} amp {centr4_maxamp:.2f}', (legend_x,legend_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, txt_color, 1, cv2.LINE_AA)

    if show_wave:
        wave_color = (0,128,255) # orange
        for i in range(len(slit)):
            cv2.circle(output_bgr, (i,int(y_pos-3-((slit[i]/255)*wave_height))),1, wave_color, 1)# display wave
    if send_wave:
        for i in range(len(slit)):
            osc_msg = float(1), float(i), float(slit[i]/255)
            osc_io.sendOSC('wave', osc_msg) # send OSC back to client
    
    cv2.imshow("Water", output_bgr)
    fps = 30
    frame_time = int(1000/fps)
    key = cv2.waitKey(frame_time)
    if key == ord('q'):
        break
    if key == ord('p'): # pause
        cv2.waitKey(-1) # any key release pause
    if key == ord('s'): # step frame by frame
        step = True
    if step:
        key = cv2.waitKey(-1) 
        if key != ord('s'): # use 's' to step, any key other than 's' releases step freeze
            step = False

    previous_frame_gray = current_frame_gray.copy()
    ret, current_frame = cap.read()
    current_frame = cv2.resize(current_frame, rsize)

    if not ret:
        break


cap.release()
cv2.destroyAllWindows()