import socket,cv2, pickle,struct,time
import os
from tkinter import *

#tkinter stufffffff
angle=0.0
def assign_angle(val):
        global angle
        angle=val
        # print(val)

root=Tk()
root.geometry('600x200')
slider1= Scale(root, from_=-90, to=90, length=400, resolution=0.01, orient=HORIZONTAL, command=assign_angle)
slider1.pack()
l=Label(root, text='Angle = 0.00')
l.pack()


# socket stufffffffff
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '169.254.250.37' # paste your server ip address here
host_ip = '192.168.43.34' 
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
port = 9998
client_socket.connect((host_ip,port)) # a tuple
data = b""
payload_size = struct.calcsize("Q")
print("payload Size :",payload_size)

#receive dataa
while True:
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
        cv2.imshow("RECEIVING VIDEO",frame)
         
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        time.sleep(0.1)
        l.config(text='Angle = '+str(angle)+'°')
        root.update_idletasks()
        root.update()
        client_socket.sendall(pickle.dumps(angle))

        
        
client_socket.close()
