import flycapture2 as fc2
    
# Initialize the camera system
system = fc2.System()
system.detect_cameras()
num_cameras = system.get_num_cameras()
if num_cameras == 0:
  raise Exception("No cameras detected.")

cam = system.get_camera_from_index(0)
cam.connect()

# Set camera parameters (exposure, etc.)
cam.set_property(fc2.PROPERTY_TYPE.EXPOSURE, 30.0) 

# Capture a frame
image = cam.retrieve_buffer()

# Disconnect the camera
cam.disconnect()