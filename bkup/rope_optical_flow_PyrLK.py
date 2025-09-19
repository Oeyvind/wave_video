import cv2
import numpy as np

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


# Parameters for ShiTomasi corner detection
feature_params = dict(maxCorners = 100,
                      qualityLevel = 0.3,
                      minDistance = 7,
                      blockSize = 7)

# Parameters for Lucas-Kanade optical flow
lk_params = dict(winSize  = (15,15),
                 maxLevel = 2,
                 criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors for drawing tracks
color = np.random.randint(0, 255, (100, 3))

p0 = cv2.goodFeaturesToTrack(frame_diff_masked, mask = None, **feature_params)

# Create a mask image for drawing purposes
mask = np.zeros_like(previous_frame)

while(True):
    ret, frame = cap.read()
    if not ret:
        print('No frames grabbed!')
        break

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(previous_gray, frame_gray, p0, None, **lk_params)

    # Select good points
    if p1 is not None:
        good_new = p1[st == 1]
        good_previous = p0[st == 1]

        # Draw the tracks
        for i, (new, previous) in enumerate(zip(good_new, good_previous)):
            a, b = new.ravel()
            c, d = previous.ravel()
            #mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), color[i].tolist(), 2)
            frame = cv2.circle(frame, (int(a), int(b)), 5, color[i].tolist(), -1)
        
        img = cv2.add(frame, mask)
        cv2.imshow('frame', img)

        k = cv2.waitKey(30) & 0xff
        if k == 27: # ESC key
            break

        # Update the previous frame and previous points
        previous_gray = frame_gray.copy()
        p0 = good_new.reshape(-1, 1, 2)
    else:
        # If no good points are found, re-detect features
        p0 = cv2.goodFeaturesToTrack(frame_gray, mask = None, **feature_params)
        mask = np.zeros_like(frame) # Reset mask for new tracks

cv2.destroyAllWindows()
cap.release()