import threading 
import time


numli=[1,2,3,4,5]
def add():
    global num,s1,s2
    for numbur in numli:
        print(threading.currentThread(),"waiting for s1")
        s1.acquire()
        num=numbur
        
        
        print(threading.currentThread(),"got s1")
        #num= int(input())
        num+=3
        print(threading.currentThread(),"  num= ",num)
        s2.release()
        # time.sleep(10)

def mul(bt):
    print("inside mul")
    global num,s1,s2,s3,num2
    while True:
        # bt.join()
        print(threading.currentThread(),"waiting for s2")
        s2.acquire()
        print(threading.currentThread(),"got s2")
        print(threading.currentThread(),"waiting for s3")
        s3.acquire()
        print(threading.currentThread(),"got s3")
        temp=num
        s1.release()
        print(threading.currentThread(),"read num as",num)
        temp*=10
        time.sleep(1.8)
        print(threading.currentThread(),"  num= ",temp)
        num2=temp
        s4.release()
        # time.sleep(10)

def sub(bt):
    print("inside sub")
    global num,s3,s4,num2
    # bt.join()
    while True:
        print(threading.currentThread(),"waiting for s4")
        s4.acquire()
        print(threading.currentThread(),"got s4")
        temp=num2
        s3.release()
        temp/=10
        print(threading.currentThread(),"  num= ",temp)
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

