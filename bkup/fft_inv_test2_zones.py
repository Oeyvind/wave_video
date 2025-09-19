import cv2
import numpy as np
from matplotlib import pyplot as plt

size = (256,256)
downsamp = 1
output = np.zeros(size)
dimensions = output.shape
pix_size = 1

img1 = np.zeros(size,dtype='uint8')
cv2.circle(img1, (int(dimensions[1]/16), int(dimensions[0]/16)), 1, 255, pix_size)
img2 = np.zeros(size,dtype='uint8')
#cv2.circle(img2, (int(dimensions[1]*5/16), int(dimensions[0]*5/16)), 1, 255, pix_size)
cv2.circle(img2, (0, int(dimensions[0]*1/16)), 1, 255, pix_size)
##cv2.circle(img2, (0, int(dimensions[0]*3/16)), 1, 255, pix_size)
##cv2.circle(img2, (0, int(dimensions[0]*11/16)), 1, 255, pix_size)
##cv2.circle(img2, (0, int(dimensions[0]*4/16)), 1, 255, pix_size)

cv2.circle(img2, (int(dimensions[1]*1/16),0), 1, 255, pix_size)
##cv2.circle(img2, (int(dimensions[1]*3/16),0), 1, 255, pix_size)
##cv2.circle(img2, (int(dimensions[1]*11/16),0), 1, 255, pix_size)
##cv2.circle(img2, (int(dimensions[1]*4/16),0), 1, 255, pix_size)

#cv2.circle(img2, (0, int(16/np.sqrt(0.5))), 1, 255, pix_size)
#cv2.circle(img2, (int(16/np.sqrt(0.5)), 0), 1, 255, pix_size)
#cv2.circle(img2, (22, 22), 1, 255, pix_size)
img3 = np.zeros(size,dtype='uint8')
#cv2.circle(img3, (int(dimensions[1]*1/16), int(dimensions[0]*1/16)), 1, 255, pix_size)
#cv2.circle(img3, (int(dimensions[1]*3/16), int(dimensions[0]*3/16)), 1, 255, pix_size)
#cv2.circle(img3, (int(dimensions[1]*5/16), int(dimensions[0]*5/16)), 1, 255, pix_size)
#cv2.circle(img3, (int(dimensions[1]*7/16), int(dimensions[0]*7/16)), 1, 255, pix_size)
cv2.circle(img3, (int(dimensions[1]*9/16), int(dimensions[0]*9/16)), 1, 255, pix_size)
#cv2.circle(img3, (int(dimensions[1]*11/16), int(dimensions[0]*11/16)), 1, 255, pix_size)
cv2.circle(img3, (int(dimensions[1]*13/16), int(dimensions[0]*13/16)), 1, 255, pix_size)
#cv2.circle(img3, (int(dimensions[1]*15/16), int(dimensions[0]*15/16)), 1, 255, pix_size)


## ifft
img_back1 = np.fft.ifft2(img1.astype(complex))
img_back1 = np.real(img_back1)*100
img_back2 = np.fft.ifft2(img2.astype(complex))
img_back2 = np.real(img_back2)*100
img_back3 = np.fft.ifft2(img3.astype(complex))
img_back3 = np.real(img_back3)*100

# zoom
zoom_factor = 4
size_x, size_y = dimensions[:2]
img_back1z = cv2.resize(img_back1[int(size_y/2):int((size_y/2)+(size_y/zoom_factor)),
                                  int(size_x/2):int((size_x/2)+(size_x/zoom_factor))],
                                  None, fx=zoom_factor, fy=zoom_factor)
img_back2z = cv2.resize(img_back2[int(size_y/2):int((size_y/2)+(size_y/zoom_factor)),
                                  int(size_x/2):int((size_x/2)+(size_x/zoom_factor))],
                                  None, fx=zoom_factor, fy=zoom_factor)
img_back3z = cv2.resize(img_back3[int(size_y/2):int((size_y/2)+(size_y/zoom_factor)),
                                  int(size_x/2):int((size_x/2)+(size_x/zoom_factor))],
                                  None, fx=zoom_factor, fy=zoom_factor)


# assemble image grid
img1 = cv2.cvtColor(np.astype(img1, 'uint8'), cv2.COLOR_GRAY2RGB)
img2 = cv2.cvtColor(np.astype(img2, 'uint8'), cv2.COLOR_GRAY2RGB)
img3 = cv2.cvtColor(np.astype(img3, 'uint8'), cv2.COLOR_GRAY2RGB)
img_back1 = cv2.cvtColor(np.astype(img_back1, 'uint8'), cv2.COLOR_GRAY2RGB)
img_back2 = cv2.cvtColor(np.astype(img_back2, 'uint8'), cv2.COLOR_GRAY2RGB)
img_back3 = cv2.cvtColor(np.astype(img_back3, 'uint8'), cv2.COLOR_GRAY2RGB)
img_back1z = cv2.cvtColor(np.astype(img_back1z, 'uint8'), cv2.COLOR_GRAY2RGB)
img_back2z = cv2.cvtColor(np.astype(img_back2z, 'uint8'), cv2.COLOR_GRAY2RGB)
img_back3z = cv2.cvtColor(np.astype(img_back3z, 'uint8'), cv2.COLOR_GRAY2RGB)

h1_concat = np.concatenate((img1, img_back1, img_back1z), axis=1)
h2_concat = np.concatenate((img2, img_back2, img_back2z), axis=1)
h3_concat = np.concatenate((img3, img_back3, img_back3z), axis=1)

hv_concat = np.concatenate((h1_concat, h2_concat, h3_concat), axis=0)
insize = np.shape(hv_concat)

output = cv2.resize(hv_concat, (int(insize[1]/downsamp), int(insize[0]/downsamp)))
cv2.imshow('frame', output)
cv2.waitKey(-1) #wait until any key is pressed
    
cv2.destroyAllWindows()
