import numpy as np
from scipy.fft import rfft,rfftfreq,fft, fftfreq
import matplotlib.pyplot as plt

# Generate a sample signal
N = 600  # Number of sample points
T = 1.0 / 600.0  # Sample spacing
x = np.linspace(0.0, N*T, N, endpoint=False)
y = np.sin(60 * 2.0 * np.pi * x) + 1 * np.sin(80.0 * 2.0 * np.pi * x) + 1 * np.sin(180.0 * 2.0 * np.pi * x)


# Compute the RFFT
yf = rfft(y)
yf = np.pow(2.0/N * np.abs(yf),2)
#yf += 0.1
#yf[:] = 0.5
xf = rfftfreq(N, T)

centr_ranges = [0, 150, 300]
centr1 = (np.sum(xf[centr_ranges[0]:centr_ranges[1]]*yf[centr_ranges[0]:centr_ranges[1]])/np.sum(yf[centr_ranges[0]:centr_ranges[1]]))
centr2 = (np.sum(xf[centr_ranges[1]:centr_ranges[2]]*yf[centr_ranges[1]:centr_ranges[2]])/np.sum(yf[centr_ranges[1]:centr_ranges[2]]))
print(centr1, centr2)

# Plot the magnitude of the FFT
plt.plot(xf, yf)
plt.plot(centr1, 0.9,marker='o', linestyle='')
plt.plot(centr2, 0.9,marker='o', linestyle='')
plt.grid()
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.title("FFT of a signal")
plt.show()