import cv2
import numpy as np 
import imutils

# Open the video file
#cap = cv2.VideoCapture("Nidelv_brygger3.mp4")
cap = cv2.VideoCapture("dokkpark_2025_10.mp4")
ret, current_frame = cap.read()
dimensions = current_frame.shape
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

    current_frame_screen = screen_blend_self(current_frame_gray)
    frame_diff = cv2.subtract(current_frame_gray,previous_frame_gray) 
    frame_diff_screen = cv2.subtract(current_frame_screen,previous_frame_screen)
    previous_frame_screen =  current_frame_screen
    output = cv2.add(current_frame_gray, frame_diff_filt)#current_frame_screen#frame_diff#cv2.add(frame_diff, frame_diff_filt)

    '''
    # diff
    #frame_diff = cv2.absdiff(current_frame_gray,previous_frame_gray)
    frame_diff = cv2.subtract(current_frame_gray,previous_frame_gray) # gets lighter
    #frame_diff = cv2.subtract(previous_frame_gray,current_frame_gray) # gets darker
    #frame_diff = cv2.blur(frame_diff, (3,3))
    # adjust image balance
    alpha = 0.7  # Contrast control (1.0 for no change)
    beta = 100    # Brightness control (positive for brighter, negative for darker)
    frame_diff = cv2.convertScaleAbs(frame_diff, alpha=alpha, beta=beta)
    thresh = 50
    _, frame_diff = cv2.threshold(frame_diff, thresh, 255, cv2.THRESH_TOZERO)

    # Display result
    frame_diff_bgr = cv2.cvtColor(frame_diff, cv2.COLOR_GRAY2BGR)
    frame_diff_bgr[0:,:,:2] = 0 # keep only red
    #frame_diff_bgr[0:,:,1] = 0

    # test
    alpha = 1.2  # Contrast control (1.0 for no change)
    beta = -150    # Brightness control (positive for brighter, negative for darker)
    current_frame_dark = cv2.convertScaleAbs(current_frame, alpha=alpha, beta=beta)

    current_frame_g_bgr = cv2.cvtColor(current_frame_gray, cv2.COLOR_GRAY2BGR)
    current_frame_g_bgr[0:,:,1:] = 0 # keep only blue 

    output = current_frame#cv2.add(current_frame_g_bgr, frame_diff_bgr)
    '''
    cv2.imshow("Water", output)
    
    key = cv2.waitKey(30)
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