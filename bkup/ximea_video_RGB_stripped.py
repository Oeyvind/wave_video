from ximea import xiapi
import numpy as np
import cv2

# open camera 
cam = xiapi.Camera()
cam.open_device()
cam.set_imgdataformat('XI_RGB24')
cam.set_exposure(20000)
#create instance of Image to store image data and metadata
img = xiapi.Image()
#print('Starting data acquisition...')
cam.start_acquisition()

try:
    print('Starting video. Press ESC to exit.')
    while True:
        cam.get_image(img)
        data = img.get_image_data_numpy()
        print(np.shape(data))
        size_ = 640
        scale = size_/np.shape(data)[1] # data array shape is y,x
        size = (size_,int(np.shape(data)[0]*scale))
        print(scale, size)
        output = cv2.resize(data, size)
        cv2.imshow('XiCAM example', output)

        key = cv2.waitKey(1)
        if key == 27:
            break
        
except KeyboardInterrupt:
    cv2.destroyAllWindows()

print('Stopping acquisition...')
cam.stop_acquisition()
#stop communication
cam.close_device()
print('Done.')
