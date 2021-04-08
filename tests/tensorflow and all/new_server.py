import socket, cv2, pickle,struct,imutils

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# host_ip = '169.254.250.37'
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
port = 9999

print('HOST IP:',host_ip)
socket_address = (host_ip,port)
server_socket.bind(socket_address)
server_socket.listen(5)
print("LISTENING AT:",socket_address)
client_socket,addr = server_socket.accept()
print('Connection From:',addr)

cam=cv2.VideoCapture(0)

while True:
    if not cam.isOpened():
        print("camera errror")
        break
    res,frame=cam.read()
    if not res:
        print("problem reading camera")
        break
    frame=cv2.resize(frame,(512,512),interpolation=cv2.INTER_AREA)
    pframe=pickle.dumps(frame)
    msg=struct.pack("Q",len(pframe))+pframe
    client_socket.sendall(msg)
    msg=client_socket.recv(100)

    print("mesage recvd : ", pickle.loads(msg))

    
    

    
 
client_socket.close()
            
#client_socket.close()