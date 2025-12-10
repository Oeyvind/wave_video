import cv2
import numpy as np
from pythonosc.udp_client import SimpleUDPClient
from scipy.signal import find_peaks
from scipy.fft import rfft, rfftfreq


# OSC-innstillinger
osc_ip = "127.0.0.1"
osc_port = 8000
osc_client = SimpleUDPClient(osc_ip, osc_port)

# Videokilde (0 = webcam, eller filsti)
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("dokkpark_2025_10.mp4")
step = False
# For optisk flyt
prev_gray = None

# For frekvensanalyse
intensity_series = []
max_series_length = 128

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Gråtone og resize for ytelse
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_small = cv2.resize(gray, (160, 120))

    # === Bølgeretning via optisk flyt ===
    if prev_gray is not None:
        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray_small, None,
                                            0.5, 3, 15, 3, 5, 1.2, 0)
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        avg_angle = np.mean(ang[mag > 1.0])  # bare sterke bevegelser
        direction_deg = np.degrees(avg_angle) % 360
    else:
        direction_deg = 0.0

    prev_gray = gray_small.copy()

    # === Bølgefrekvens via intensitet over tid ===
    roi = gray[100:110, :]  # horisontal stripe
    avg_intensity = np.mean(roi)
    intensity_series.append(avg_intensity)
 
 # FFT-basert flerbåndsanalyse
if len(intensity_series) >= max_series_length:
    signal = np.array(intensity_series) - np.mean(intensity_series)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    N = len(signal)
    yf = np.abs(rfft(signal))
    xf = rfftfreq(N, 1 / fps)

    def peak_in_band(xf, yf, fmin, fmax):
        mask = (xf >= fmin) & (xf <= fmax)
        if np.any(mask):
            idx = np.argmax(yf[mask])
            return xf[mask][idx]
        return 0.0

    freq_low = peak_in_band(xf, yf, 0.1, 0.5)
    freq_mid = peak_in_band(xf, yf, 0.5, 2.0)
    freq_high = peak_in_band(xf, yf, 2.0, 5.0)
else:
    freq_low = freq_mid = freq_high = 0.0

# Send OSC for alle tre bånd
osc_client.send_message("/wave/freq_low", float(freq_low))
osc_client.send_message("/wave/freq_mid", float(freq_mid))
osc_client.send_message("/wave/freq_high", float(freq_high))

    # === Visualisering (valgfritt) ===
    cv2.putText(frame, f"Freq: {frequency:.2f} Hz", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Dir: {direction_deg:.1f} deg", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow("Wave Analyzer", frame)

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
cap.release()
cv2.destroyAllWindows()
