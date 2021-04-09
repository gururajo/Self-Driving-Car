import time,threading
import cv2,os,sys,socket,struct,pickle,psutil
import numpy as np
from tkinter import *
anglelist = np.zeros(52, dtype='int')
datalist=sorted(os.listdir('DATA/'))
datacounter=len(datalist)+1
for i in range(len(datalist)):
    data=np.load("DATA/"+datalist[i],allow_pickle=True)
    print("diving this",datalist[i])
    
    for fna in data:
        angle=fna[1]*515+1285
        index = int((1800-int(angle))/10)
        anglelist[index]+=1
    print(anglelist,len(data))
    data=0
print(np.average(anglelist),max(anglelist),min(anglelist))