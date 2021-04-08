import threading 
import time
import cv2,os,sys,socket,struct,pickle
import numpy as np
from tkinter import *


#globals
tempf=np.zeros((0,0))
start_time=time.time()
endme=False

#tkinter stufffffff
angle=0.0
def assign_angle(val):
        global angle
        angle=val
        # print(val)
root=Tk()
root.geometry('600x400')
slider1= Scale(root, from_=-90, to=90, length=400, resolution=0.1, orient=HORIZONTAL, command=assign_angle)
slider1.pack()
l=Label(root, text='Angle = 0.00')
l.pack()


# socket stufffffffff
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '169.254.250.37' # paste your server ip address here
#host_ip = '192.168.43.34' 
# host_name  = socket.gethostname()
# host_ip = socket.gethostbyname(host_name)
port = 9999
client_socket.connect((host_ip,port)) # a tuple

payload_size = struct.calcsize("Q")
print("payload Size :",payload_size)


from tensorflow_od_saved_model import *

# camera stuffff
camera = cv2.VideoCapture(0)
_,image_np=camera.read()
input_tensor = np.expand_dims(image_np, 0)
detections= detect_fn(input_tensor)
camera.release()
print("captured first image\n Everything seems fine",detections)



# All thread functions
def add():
    global frame,s1,s2,l,root,angle,endme
    data = b""
    while not endme:
        print(threading.currentThread(),"waiting for s1")
        s1.acquire()
        print(threading.currentThread(),"got s1")

        start_t=time.time()
        while len(data) < 8:
                packet = client_socket.recv(1024) # 4K
                if not packet: break
                data+=packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
        
        while len(data) < msg_size:
                data += client_socket.recv(4*1024)
        end_t=time.time()
        print("stream delay",end_t-start_t)
        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = pickle.loads(frame_data)
        # cv2.imshow("RECEIVING VIDEO",frame)
         
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break
        
        # time.sleep(0.1)
        #l.config(text='Angle = '+str(angle)+'°')
        #root.update_idletasks()
        #root.update()
        client_socket.sendall(pickle.dumps(angle))

        
        s2.release()
        # time.sleep(10)
    else:
        s2.release()

def mul(bt):
    print("inside mul")
    global frame,detectionss,tempf,s1,s2,s3,endme
    while not endme:
        # bt.join()
        print(threading.currentThread(),"waiting for s2")
        s2.acquire()
        print(threading.currentThread(),"got s2")
        print(threading.currentThread(),"waiting for s3")
        s3.acquire()
        print(threading.currentThread(),"got s3")
        frame=cv2.rotate(frame,cv2.ROTATE_180)
        tempf=frame
        s1.release()
        input_tensor = np.expand_dims(tempf, 0)
        detectionss = detect_fn(input_tensor)
        # print(threading.currentThread(),"read num as",num)
        # temp*=10
        # time.sleep(1.8)
        # print(threading.currentThread(),"  num= ",temp)
        # num2=temp
        s4.release()
        # time.sleep(10)
    else:
        s4.release()
        s1.release()

def sub(bt):
    print("inside sub")
    fps=0	
    global detectionss,s3,s4,tempf,start_time,endme
    # bt.join()
    while not endme:
        print(threading.currentThread(),"waiting for s4")
        start_t=time.time()
        s4.acquire()
        print(threading.currentThread(),"got s4")
        detections=detectionss
        tempframe=tempf
        s3.release()

        
        label_id_offset = 1
        image_np_with_detections = tempframe.copy()
        viz_utils.visualize_boxes_and_labels_on_image_array(
           image_np_with_detections,
           detections['detection_boxes'][0].numpy(),
           detections['detection_classes'][0].numpy().astype(np.int32),
           detections['detection_scores'][0].numpy(),
           category_index,
           use_normalized_coordinates=True,
           max_boxes_to_draw=5,
           min_score_thresh=.60,
           agnostic_mode=False)
        cv2.imshow("detection",image_np_with_detections )
        
        end_time=time.time()
        print("time for 1 frame",end_time-start_t)
        if end_time-start_time>=1 :
            print("No of frames",fps)
            fps=0
            start_time=time.time()
        else:
            fps+=1
         
        if cv2.waitKey(1) & 0xff == 27:   break
    else:
        s3.release()


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
while True:
    time.sleep(1)
    key=input()
    if key=='q' or key == 'Q':
       endme=True
       break
t1.join()
t2.join()
t3.join()

# threading.excepthook(args=[])
end_t=time.time()
print(end_t-start_t)

