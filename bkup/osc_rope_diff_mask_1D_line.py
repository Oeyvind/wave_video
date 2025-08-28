import cv2
import numpy as np 
import imutils
import osc_io

# Open the video file
cap = cv2.VideoCapture("rope_2.mp4")
ret, current_frame = cap.read()
previous_frame = current_frame
dimensions = current_frame.shape
print(dimensions)
mask = np.zeros(current_frame.shape[:2], dtype="uint8")
pts = np.array([[250,300],[1260,300],[1260,750],[250,500]], np.int32)
pts = pts.reshape((-1,1,2))
polyg = cv2.fillPoly(mask,pts=[pts],color=255)

send_counter = 0

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

    # write the wave to image for display
    wave_img = binary_img.copy()
    for i in range(200,dimensions[1]):
        new = np.zeros(dimensions[0])
        new[int(wave_1D[i+filter_padding])] = 255
        wave_img[:,i] = new
    kernel = np.ones((5, 5),np.uint8)
    wave_img = cv2.dilate(wave_img, kernel, iterations=2)

    # send wave over osc to Csound
    # manually set mask, good region from 200 to 1224
    send_counter = (send_counter+1)%4 # send only every N frame
    if send_counter == 0:
        for i in range(200,1224):
            osc_msg = i, wave_1D[i+filter_padding]
            osc_io.sendOSC("wave_video", osc_msg) # send OSC back to client


    # Display result
    resized_image = cv2.resize(cv2.add(wave_img, current_frame_gray), (300, 200))
    cv2.imshow("Rope", resized_image)
    
    key = cv2.waitKey(100)
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