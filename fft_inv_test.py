import cv2
import numpy as np
from matplotlib import pyplot as plt

size = (200,200)
downsamp = 1
output = np.zeros(size)
dimensions = output.shape
pix_size = 20
blur = 20

img1 = np.zeros(size,dtype='uint8')
cv2.circle(img1, (int(dimensions[1]*0.5), int(dimensions[0]*0.5)), 1, 255, pix_size)
#img1 = cv2.blur(img1, (blur,blur))

img2 = np.zeros(size,dtype='uint8')
cv2.circle(img2, (int(dimensions[1]*0.2), int(dimensions[0]*0.21)), 1, 255, pix_size)
#img2 = cv2.blur(img2, (blur,blur))

## ifft
f1 = np.fft.fft2(img1)
fshift1 = np.fft.fftshift(f1)
magnitude_spectrum1 = 20*np.log(np.abs(fshift1),where=np.abs(fshift1)>0)
f_ishift1 = np.fft.ifftshift(fshift1)
img_back1 = np.fft.ifft2(f_ishift1)
img_back1 = np.real(img_back1)
 
f2 = np.fft.fft2(img2)
fshift2 = np.fft.fftshift(f2)
magnitude_spectrum2 = 20*np.log(np.abs(fshift2),where=np.abs(fshift2)>0)
f_ishift2 = np.fft.ifftshift(fshift2)
img_back2 = np.fft.ifft2(f_ishift2)
img_back2 = np.real(img_back2)


# assemble image grid
mags_bgr1 = cv2.cvtColor(np.astype(magnitude_spectrum1, 'uint8'), cv2.COLOR_GRAY2RGB)
mags_bgr2 = cv2.cvtColor(np.astype(magnitude_spectrum2, 'uint8'), cv2.COLOR_GRAY2RGB)
img1 = cv2.cvtColor(np.astype(img1, 'uint8'), cv2.COLOR_GRAY2RGB)
img_back1 = cv2.cvtColor(np.astype(img_back1, 'uint8'), cv2.COLOR_GRAY2RGB)
img2 = cv2.cvtColor(np.astype(img2, 'uint8'), cv2.COLOR_GRAY2RGB)
img_back2 = cv2.cvtColor(np.astype(img_back2, 'uint8'), cv2.COLOR_GRAY2RGB)

#zoom_factor = 4
#mags_y, mags_x = np.shape(mags_bgr)[:2]
mags_bgr_zoom = cv2.resize(mags_bgr[int((mags_y/2)-((mags_y/2)/zoom_factor)):int((mags_y/2)+((mags_y/2)/zoom_factor)),
                                        int((mags_x/2)-((mags_x/2)/zoom_factor)):int((mags_x/2)+((mags_x/2)/zoom_factor))], 
                                        None, fx=zoom_factor, fy=zoom_factor)
#mags_bgr2_zoom = cv2.resize(mags_bgr2[int((mags_y/2)-((mags_y/2)/zoom_factor)):int((mags_y/2)+((mags_y/2)/zoom_factor)),
#                                        int((mags_x/2)-((mags_x/2)/zoom_factor)):int((mags_x/2)+((mags_x/2)/zoom_factor))], 
#                                        None, fx=zoom_factor, fy=zoom_factor)

h1_concat = np.concatenate((img1, mags_bgr1, img_back1), axis=1)
h2_concat = np.concatenate((img2, mags_bgr2, img_back2), axis=1)

hv_concat = np.concatenate((h1_concat, h2_concat), axis=0)
insize = np.shape(hv_concat)

output = cv2.resize(hv_concat, (int(insize[1]/downsamp), int(insize[0]/downsamp)))
cv2.imshow('frame', output)
cv2.waitKey(-1) #wait until any key is pressed
    
cv2.destroyAllWindows()
