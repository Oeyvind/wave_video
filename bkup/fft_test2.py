import cv2
import numpy as np
from matplotlib import pyplot as plt

size = (200,200)
downsamp = 1
output = np.zeros(size)
dimensions = output.shape
pix_size = 50
blur = 10

line_img = np.zeros(size,dtype='uint8')
y_left = (0, 0)#int(dimensions[0]*0.5))
y_right = (int(dimensions[1]), int(dimensions[0]))#*0.5))
cv2.line(line_img,y_left,y_right,255,pix_size)
#line_img = cv2.blur(line_img, (blur,blur))

sine_img = np.zeros(size,dtype='uint8')
a = np.linspace(0, np.pi*2, num=dimensions[1])
sin = np.sin(a)
for i in range(dimensions[1]):
    for j in range(dimensions[0]):
        cv2.circle(sine_img, (i, j), 1, int(((sin[i]+1)+(sin[j]+1))*32), 1)
#cv2.circle(sine_img, (int(dimensions[1]*0.75), int(dimensions[0]*0.5)), 1, 255, pix_size)
#sine_img = cv2.blur(sine_img, (blur,blur))


## fft
f = np.fft.fft2(line_img)
fshift = np.fft.fftshift(f)
magnitude_spectrum = 20*np.log(np.abs(fshift))

f2 = np.fft.fft2(sine_img)
fshift2 = np.fft.fftshift(f2)
magnitude_spectrum2 = 20*np.log(np.abs(fshift2))


# assemble image grid
mags_bgr = cv2.cvtColor(np.astype(magnitude_spectrum, 'uint8'), cv2.COLOR_GRAY2RGB)
mags_bgr2 = cv2.cvtColor(np.astype(magnitude_spectrum2, 'uint8'), cv2.COLOR_GRAY2RGB)
line_img = cv2.cvtColor(np.astype(line_img, 'uint8'), cv2.COLOR_GRAY2RGB)
sine_img = cv2.cvtColor(np.astype(sine_img, 'uint8'), cv2.COLOR_GRAY2RGB)

zoom_factor = 4
mags_y, mags_x = np.shape(mags_bgr)[:2]
mags_bgr_zoom = cv2.resize(mags_bgr[int((mags_y/2)-((mags_y/2)/zoom_factor)):int((mags_y/2)+((mags_y/2)/zoom_factor)),
                                        int((mags_x/2)-((mags_x/2)/zoom_factor)):int((mags_x/2)+((mags_x/2)/zoom_factor))], 
                                        None, fx=zoom_factor, fy=zoom_factor)
mags_bgr2_zoom = cv2.resize(mags_bgr2[int((mags_y/2)-((mags_y/2)/zoom_factor)):int((mags_y/2)+((mags_y/2)/zoom_factor)),
                                        int((mags_x/2)-((mags_x/2)/zoom_factor)):int((mags_x/2)+((mags_x/2)/zoom_factor))], 
                                        None, fx=zoom_factor, fy=zoom_factor)

h_concat = np.concatenate((line_img, mags_bgr, mags_bgr_zoom), axis=1)
h2_concat = np.concatenate((sine_img, mags_bgr2, mags_bgr2_zoom), axis=1)

hv_concat = np.concatenate((h2_concat, h_concat), axis=0)
insize = np.shape(hv_concat)

output = cv2.resize(hv_concat, (int(insize[1]/downsamp), int(insize[0]/downsamp)))
cv2.imshow('frame', output)
cv2.waitKey(-1) #wait until any key is pressed
    
cv2.destroyAllWindows()
