import cv2
import numpy as np
from matplotlib import pyplot as plt

# Create a video capture object (0 for webcam, or specify video file path)
#cap = cv2.VideoCapture("inderoy_pool_2.mp4")#Nidelv_brygger3.mp4")
cap = cv2.VideoCapture("rope_2.mp4")#rope_ximea_1.mp4")

# Take diff between two first frames and find corners in it
ret, current_frame = cap.read()

ret, previous_frame = cap.read()
if not ret:
    print("Failed to grab first frame.")
    exit()

mask1 = np.zeros(current_frame.shape[:2], dtype="uint8")
pts = np.array([[250,300],[1260,300],[1260,750],[250,500]], np.int32)
pts = pts.reshape((-1,1,2))
polyg = cv2.fillPoly(mask1,pts=[pts],color=255)

current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
previous_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
frame_diff = cv2.absdiff(current_gray,previous_gray)
frame_diff_masked = cv2.bitwise_and(frame_diff, frame_diff, mask=mask1)

# Create an image for drawing purposes
canvas = np.zeros_like(previous_frame)


while(True):
    ret, frame = cap.read()
    if not ret:
        print('No frames grabbed!')
        break

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    f = np.fft.fft2(frame_gray)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20*np.log(np.abs(fshift))
        
    mags_bgr = cv2.cvtColor(np.astype(magnitude_spectrum, 'uint8'), cv2.COLOR_GRAY2RGB)
    horizontal_concat = np.concatenate((frame, mags_bgr), axis=1)
    insize = np.shape(horizontal_concat)
    downsamp = 3
    output = cv2.resize(horizontal_concat, (int(insize[1]/downsamp), int(insize[0]/downsamp)))
    cv2.imshow('frame', output)
    k = cv2.waitKey(30) & 0xff
    if k == ord('q'): # ESC key
        break
    # Update the previous frame and previous points
    previous_gray = frame_gray.copy()
    canvas = np.zeros_like(frame) # Reset mask for new tracks

cv2.destroyAllWindows()
cap.release()