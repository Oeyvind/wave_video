import cv2
import numpy as np 
import osc_io

# Open the video file
#cap = cv2.VideoCapture("Nidelv_brygger3.mp4")
cap = cv2.VideoCapture("dokkpark_2025_10.mp4")
ret, current_frame = cap.read()
dimensions = current_frame.shape
print('dimensions input', dimensions)
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
    alpha = 0.02
    filtered_frame_display, prev_frame_float = lowpass_over_time(current_frame_gray, alpha, prev_frame_float)
    frame_diff_filt = cv2.subtract(current_frame_gray,filtered_frame_display) 

    # contrast, brightness
    alpha = 0.8  # Contrast control (1.0 for no change)
    beta = -50    # Brightness control (positive for brighter, negative for darker)
    current_frame_dark = cv2.convertScaleAbs(current_frame_gray, alpha=alpha, beta=beta)
    current_frame_dark = screen_blend_self(current_frame_dark)

    current_frame_screen = screen_blend_self(current_frame_gray)
    frame_diff = cv2.subtract(current_frame_gray,previous_frame_gray) 
    frame_diff_screen = cv2.subtract(current_frame_screen,previous_frame_screen)
    previous_frame_screen =  current_frame_screen
    output = cv2.add(current_frame_dark, frame_diff_filt)
    output_bgr = cv2.cvtColor(output, cv2.COLOR_GRAY2BGR)

    # slit
    y_first = 0.4
    y_offset = 0.115
    wave_height = dimensions[0]* 0.08
    y_pos1 = int(dimensions[0]* y_first)
    y_pos2 = int(dimensions[0]* (y_first+(y_offset)))
    y_pos3 = int(dimensions[0]* (y_first+(y_offset*2)))
    y_pos4 = int(dimensions[0]* (y_first+(y_offset*3)))
    y_pos5 = int(dimensions[0]* (y_first+(y_offset*4)))
    y_pos6 = int(dimensions[0]* (y_first+(y_offset*5)))
    y_poses = [y_pos1,y_pos2,y_pos3,y_pos4,y_pos5,y_pos6]
    
    show_mask = True
    show_wave = True
    if show_mask:
        for y_pos in y_poses:
            pts = np.array([[0,y_pos-2], [dimensions[1],y_pos-2],
                            [dimensions[1],y_pos+2],[0,y_pos+2]], np.int32)
            pts = pts.reshape((-1,1,2))
            polyg_show = cv2.polylines(output_bgr,pts=[pts],isClosed=True, color=(255,0,0), thickness=1)
    if show_wave:
        wave_color = (0,128,255) # orange
        slitnum = 1
        for y_pos in y_poses:
            slit = output[y_pos,:]
            for i in range(len(slit)):
                cv2.circle(output_bgr, (i,int(y_pos-3-((slit[i]/255)*wave_height))),1, wave_color, 1)# display wave
                if slitnum == 1:
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
    if not ret:
        break


cap.release()
cv2.destroyAllWindows()