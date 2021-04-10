import time
import threading
import cv2
import os
import sys
import socket
import struct
import pickle
import psutil
import random
import numpy as np
from tkinter import *


# tkinter stufffffff
angle = 1540
def throttlethread():
    global angle
    angle = 1540

    def assign_angle(val):
        global angle
        angle = val
        # print(val)
    def pnrfunc():
        global pause
        pause=not pause
    def quitfunc():
        global quit,pause
        quit=True
        pause=False
        root.destroy()
    root = Tk()
    root.geometry('600x200')
    slider1 = Scale(root, from_=1285, to=1800, length=400, resolution=1,orient=HORIZONTAL, command=assign_angle, variable=angle).pack()
    quitme=Button(root,command=quitfunc,text="QUIT",height=3,width=10).pack(side=LEFT,padx=100)
    pauseorresume=Button(root,command=pnrfunc,text="pause/resume",height=3,width=10).pack(side=RIGHT,padx=100)
    root.mainloop()

t1 = threading.Thread(target=throttlethread)
t1.start()


# socket stufffffffff
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host_ip = '169.254.250.37' # paste your server ip address here
#host_ip = '192.168.43.34'
# host_ip = '192.168.43.55'
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
port = 9999
client_socket.connect((host_ip, port))  # a tuple
payload_size = struct.calcsize("Q")
print("payload Size :", payload_size)
data = b""

# some variables used
training_data = []
balanced_data = []
datalist = sorted(os.listdir("DATA/"))
datacounter = len(datalist)+1
ramthresh = 80
countthresh=350
maxineachclass=6
minineachclass=2
pause = quit = False
# balancing stuff
anglelist = np.zeros(52, dtype='int')


while not quit:
    # print("hello")
    while pause:
        print("paused")
        time.sleep(.5)
    if quit: break
    start_t = time.time()
    while len(data) <= 8:
        # print("llllll")
        packet = client_socket.recv(1024)  # 4K
        if not packet:
            break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        # print("aaaaaa")
        data += client_socket.recv(4*1024)
    end_t = time.time()
    # print("stream delay",end_t-start_t)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)

#     frame=frame/255
    anglelist[int((1800-int(angle))/10)] += 1
#     anglei=(int(angle)-1285)/515
#     print(anglei)
#     print(1800-int(angle))
    print(len(training_data), len(balanced_data), angle)
    training_data.append([frame, angle])
    client_socket.sendall(pickle.dumps(angle))
    if psutil.virtual_memory().percent > ramthresh or len(training_data)>countthresh:
        random.shuffle(training_data)
        print(anglelist)
        if min(anglelist) > minineachclass:
            print("inside greter than")
            addedlist=[]
            anglelist = np.full(52, min(anglelist), dtype='int')
            for i in range(len(training_data)):
                # print("inside loop")
                [frame, angle]=training_data[i]
                index = int((1800-int(angle))/10)
                if anglelist[index] > 0:
                    # print("inside if")
                    frame = frame/255
                    anglei = (int(angle)-1285)/515
                    balanced_data.append([frame, anglei])
                    anglelist[index] -= 1
                else:
                    # print("inside else")
                    addedlist.append([frame,angle])
            print("outside loop")
            training_data=addedlist
            addedlist=[]
            print("copied")
            anglelist = np.zeros(52, dtype='int')
            for fna in balanced_data:
                angle=fna[1]*515+1285
                index = int((1800-int(angle))/10)
                anglelist[index]+=1
            print("balanced data anglelist",anglelist)

                
            anglelist = np.zeros(52, dtype='int')
            for fna in training_data:
                index = int((1800-int(fna[1]))/10)
                anglelist[index]+=1
            print("anglelist ready")
            pause=True
            time.sleep(.5)
            print(anglelist,len(training_data),sum(anglelist))
            if psutil.virtual_memory().percent < ramthresh and len(balanced_data)<countthresh:
                print("not enough data \n continuing")
                continue
        else:
            print("inside less than")
            temp = []
            anglelist = np.zeros(52, dtype='int')
            # print("going for loop")
            for i in range(len(training_data)):
                # print("inside loop")
                fna = training_data[i]
                index = int((1800-int(fna[1]))/10)
                # print("inside loop found index", index)
                if anglelist[index] < maxineachclass:
                    
                    # print("less than 10 so inside if")
                    temp.append(fna)
                    anglelist[index] += 1
                    # print("done apeend and increment", i)
                    if len(training_data)-5 < i:
                        break

            # print("outside looop")
            training_data = temp
            print("Alist",anglelist,sum(anglelist),len(training_data))
            # print("done copying")
            temp = []
            pause=True
            continue

        print("RAM greater than 85 saving the data")
        random.shuffle(balanced_data)
        frames=[]
        angles=[]
        for [frame,angle] in balanced_data:
            frames.append(frame)
            angles.append(angle)
        balanced_data=[]

        np.savez_compressed("DATA/data85_"+str(datacounter)+".npz",
                np.array(frames,dtype="float32"),np.array(angles,dtype="float32"))
        # datacounter += 1
        # np.save("DATA/data85_"+str(datacounter)+".npy",
        #         np.array(balanced_data[int(len(balanced_data)/2):], dtype=object))
        # # break
        datacounter += 1
        training_data = []
        balanced_data = []
        anglelist = np.zeros(52, dtype='int')
        print("Done saving press resume")

    
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xff == 27:
        break

# np.save("DATA/data85_"+str(datacounter)+".npy",np.array(training_data[:int(len(training_data)/2)],dtype=object))
else:
    print("saved data")
    print(anglelist)
    client_socket.close()
client_socket.close()
print("complted")
# root.mainloop()
