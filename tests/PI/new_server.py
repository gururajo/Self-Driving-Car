import socket, cv2, pickle,struct,traceback,threading
import time
from Car import Car
from tkinter import *


#GPIO stufffff
car=Car()

# tkinter stufffffff
angle = 1540
quit=False
bnfflag=True

def throttlethread():
    
    def assign_throttle(val):
        car.setthrottle(int(val))

    def bnffunc():
        global bnfflag
        if not bnfflag:
            car.brake()
            bnfflag=not bnfflag
        else:
            car.forward()
            bnfflag=not bnfflag
    
    def quitfunc():
        global quit
        car.stop()
        car.quitfunc()
        quit = True
        root.destroy()
    root = Tk()
    root.geometry('600x200')
    slider1 = Scale(root, from_=0, to=255, length=400, resolution=1,
                    orient=HORIZONTAL, command=assign_throttle, variable=angle).pack()
    quitme = Button(root, command=quitfunc, text="QUIT",
                    height=3, width=10).pack(side=LEFT, padx=100)
    pauseorresume = Button(root, command=bnffunc, text="pause/resume",
                           height=3, width=10).pack(side=RIGHT, padx=100)
    root.mainloop()


t1 = threading.Thread(target=throttlethread)
t1.start()




#socket Stufffff
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#host_ip = '192.168.29.55'
host_ip='192.168.43.34'
# host_ip='192.168.43.55'
#host_name  = socket.gethostname()
#host_ip = socket.gethostbyname(host_name)
port = 9998

print('HOST IP:',host_ip)
socket_address = (host_ip,port)
server_socket.bind(socket_address)
server_socket.listen(5)
print("LISTENING AT:",socket_address)
client_socket,addr = server_socket.accept()
print('Connection From:',addr)

# Camera Stuffffff
cam=cv2.VideoCapture(0)


while not quit:
    try:
        if not cam.isOpened():
            print("camera errror")
            break
        res,frame=cam.read()
        if not res:
            print("problem reading camera")
            break
        frame=cv2.resize(frame,(320,320))
        # cv2.imshow("frame",frame)
        # if cv2.waitKey(1) & 0xff ==27 : break
        pframe=pickle.dumps(frame)
        msg=struct.pack("Q",len(pframe))+pframe
        client_socket.sendall(msg)
        #msg_size = struct.unpack("Q",msg)[0]
        #print(msg_size)
        msg=client_socket.recv(100)
        rcvmsg=pickle.loads(msg)
        print("mesage recvd : ",rcvmsg )
        car.steer(int(rcvmsg))

    except:
        car.stop()
        print("something went wrong ")
        traceback.print_exc()
        client_socket.close()
        break

    



