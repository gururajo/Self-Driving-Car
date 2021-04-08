import threading 
import time
from tensorflow_od_saved_model import *
import cv2,os,sys

import numpy as np
sys.path.append(os.path.join(os.getcwd(), r"models\research"))


from object_detection.utils import visualization_utils as viz_utils

numli=[1,2,3,4,5]
camera = cv2.VideoCapture(0)
_,frame = camera.read()
detectionss=input_tensor=0
def add():
    global frame,s1,s2
    while True:
        print(threading.currentThread(),"waiting for s1")
        s1.acquire()
        print(threading.currentThread(),"got s1")

        #num= int(input())
        # num+=3
        res, image_np = camera.read()
        if not res:
            print("error accessing camera")
            break
        input_tensor = np.expand_dims(image_np, 0)
        # print(threading.currentThread(),"  num= ",num)

        s2.release()
        # time.sleep(10)

def mul(bt):
    print("inside mul")
    global input_tensor,detectionss,s1,s2,s3,num2
    while True:
        # bt.join()
        print(threading.currentThread(),"waiting for s2")
        s2.acquire()
        print(threading.currentThread(),"got s2")
        print(threading.currentThread(),"waiting for s3")
        s3.acquire()
        print(threading.currentThread(),"got s3")
        temp=input_tensor
        s1.release()
        detectionss = detect_fn(temp)
        # print(threading.currentThread(),"read num as",num)
        # temp*=10
        # time.sleep(1.8)
        # print(threading.currentThread(),"  num= ",temp)
        # num2=temp
        s4.release()
        # time.sleep(10)

def sub(bt):
    print("inside sub")
    global detectionss,s3,s4,num2
    # bt.join()
    while True:
        print(threading.currentThread(),"waiting for s4")
        s4.acquire()
        print(threading.currentThread(),"got s4")
        detections=detectionss
        s3.release()
        print("3rd thread doing sftuff")
        #cv2.imshow("detection",image_np_with_detections )
 

        #if cv2.waitKey(1) & 0xff == 27:
        #          break
        # temp/=10
        # print(threading.currentThread(),"  num= ",temp)
        # time.sleep(10)

start_t=time.time()
num2=num=0
s1=threading.Semaphore(value=1)
s2=threading.Semaphore(value=0)
s3=threading.Semaphore(value=1)
s4=threading.Semaphore(value=0)

t1=threading.Thread(target=add)
t2=threading.Thread(target=mul,args=[t1])
t3=threading.Thread(target=sub,args=[t2])

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

# threading.excepthook(args=[])
end_t=time.time()
print(end_t-start_t)

