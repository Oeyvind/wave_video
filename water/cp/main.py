import cv2
from video_capture import get_frame
from wave_analysis import analyze_direction, analyze_frequencies
from osc_sender import send_wave_data
from spectrum_plot import init_plot, update_plot

#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("../dokkpark_2025_10.mp4")
step = False

fps = cap.get(cv2.CAP_PROP_FPS) or 30
prev_gray = None
intensity_series = []
max_len = 128

fig, ax, line = init_plot()

while True:
    result = get_frame(cap)
    if result is None:
        break
    frame, gray = result
    gray_small = cv2.resize(gray, (160, 120))

    roi = gray[100:110, :]
    avg_intensity = roi.mean()
    intensity_series.append(avg_intensity)
    if len(intensity_series) > max_len:
        intensity_series.pop(0)

    if prev_gray is not None and len(intensity_series) >= max_len:
        direction = analyze_direction(prev_gray, gray_small)
        freqs = analyze_frequencies(intensity_series, fps)
        send_wave_data(freqs, direction)
        update_plot(ax, line, freqs["xf"], freqs["yf"])

    prev_gray = gray_small.copy()
    cv2.imshow("Wave Analyzer", frame)
    
    #frame_time = int(1000/fps)
    #key = cv2.waitKey(frame_time)
    key = cv2.waitKey(1)
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

cap.release()
cv2.destroyAllWindows()