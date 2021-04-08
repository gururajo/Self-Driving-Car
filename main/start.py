from tensorflow_od_saved_model import *


camera = cv2.VideoCapture(0)
_,image_np=camera.read()
input_tensor = np.expand_dims(image_np, 0)
detections= detect_fn(input_tensor)
