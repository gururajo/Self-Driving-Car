import time,threading
import cv2,os,sys,socket,struct,pickle,psutil
import numpy as np
from tkinter import *

datalist=sorted(os.listdir('DATA/'))
datacounter=len(datalist)+1
for i in range(len(datalist)):
    data=np.load("DATA/"+datalist[i],allow_pickle=True)
    print("diving this",datalist[i])
    np.save("DATA/data85_"+str(datacounter)+".npy",np.array(data[:int(len(data)/2)], dtype=object))
    datacounter += 1
    np.save("DATA/data85_"+str(datacounter)+".npy",np.array(data[int(len(data)/2):], dtype=object))
    datacounter+=1
    print("divided as ",datacounter-1,datacounter-2)
    time.sleep(100)
    data=0