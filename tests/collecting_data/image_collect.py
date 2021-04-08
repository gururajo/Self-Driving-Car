import time,threading
import cv2,os,sys,socket,struct,pickle
import numpy as np
from tkinter import *

angle=7.45
#tkinter stufffffff
def throttlethread():
        global angle
        angle=1540
        def assign_angle(val):
                global angle
                angle=val
                # print(val)
        root=Tk()
        root.geometry('600x200')
        slider1= Scale(root, from_=1285, to=1800, length=400, resolution=1, orient=HORIZONTAL, command=assign_angle,variable=angle)
        slider1.pack()
        root.mainloop()

t1=threading.Thread(target=throttlethread)
t1.start()

# socket stufffffffff
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#host_ip = '169.254.250.37' # paste your server ip address here
host_ip = '192.168.43.34' 
# host_name  = socket.gethostname()
# host_ip = socket.gethostbyname(host_name)
port = 9999
client_socket.connect((host_ip,port)) # a tuple
payload_size = struct.calcsize("Q")
print("payload Size :",payload_size)
data = b""

# some variables used
training_data=[]
while True:
    start_t=time.time()
    while len(data) <= 8:
            packet = client_socket.recv(1024) # 4K
            if not packet: break
            data+=packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    print(packed_msg_size)
#     time.sleep(.05)
#     continue
    msg_size = struct.unpack("Q",packed_msg_size)[0]
#     print(msg_size)
#     break
    while len(data) < msg_size:
            data += client_socket.recv(4*1024)
    end_t=time.time()
    # print("stream delay",end_t-start_t)
    frame_data = data[:msg_size]
    data  = data[msg_size:]
    frame = pickle.loads(frame_data)

    training_data.append([frame,angle])
    if len(training_data)>=20:
        training_data=[]
        # break

    client_socket.sendall(pickle.dumps(angle))
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xff ==27 : break

np.save("training_data.npy",np.array(training_data,dtype=object))
print("saved data")
client_socket.close()
# root.mainloop()