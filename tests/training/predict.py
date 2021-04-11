import tensorflow as tf
import numpy as np
import os,pickle,cv2
import matplotlib.pyplot as plt
import time
from modell import getmodel

cam=cv2.VideoCapture(0)
model=tf.saved_model.load("model/mymodel")
while True:
    if not cam.isOpened():
        print("camera errror")
        break
    res,frame=cam.read()
    if not res:
        print("problem reading camera")
        break
    frame=cv2.resize(frame,(200,66),interpolation=cv2.INTER_AREA)
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xff == 'q': break
    # np.resize(frame,(1,66,200,3))
    frame=frame.astype("float32")
    input_tensor = np.expand_dims(frame, 0)
    predictions = model(input_tensor)
    print(predictions)