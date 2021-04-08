import socket,cv2, pickle,struct,time
import os
from tkinter import *

angle=0

def assign_angle(val):
        global angle
        angle=val
        print(val)

root=Tk()
root.geometry('600x200')
slider1= Scale(root, from_=-90, to=90, length=400, resolution=0.01, orient=HORIZONTAL, command=assign_angle)
slider1.pack()
l=Label(root, text='Angle = 0.00')
l.pack()
# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# host_ip = '169.254.250.37' # paste your server ip address here
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
port = 9999
client_socket.connect((host_ip,port)) # a tuple
data = b""
payload_size = struct.calcsize("Q")
print(payload_size)
cntr=0
imno=0
while True:
        
        while len(data) < payload_size:
                packet = client_socket.recv(4*1024) # 4K
                if not packet: break
                data+=packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
        
        while len(data) < msg_size:
                data += client_socket.recv(4*1024)
        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("RECEIVING VIDEO",frame)
        # time.sleep(0.8)
        cntr=cntr+1
        if(cntr==20):
                cntr=0
                path = 'E:/myPrograms/myPython/img_trans/img_data/'
                #cv2.imwrite(os.path.join(path , str(imno)+'_'+str(angle)+'.jpg'), frame)
                imno=imno+1
        key = cv2.waitKey(1) & 0xFF
        if key  == ord('q'):
                break
        l.config(text='Angle = '+str(angle)+'°')
        root.update_idletasks()
        root.update()

client_socket.close()




