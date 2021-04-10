from tkinter import * 
angle=1540
def assign_angle(val):
    global angle
    print(val)
    angle = val
    # print(val)
def butted():
    print("pressed")
def quitfunc():
    print("quit")
root = Tk()
root.geometry('600x200')
slider1 = Scale(root, from_=1285, to=1800, length=400, resolution=1,orient=HORIZONTAL, command=assign_angle, variable=angle).pack()
quitme=Button(root,command=quitfunc,text="QUIT",height=3,width=10).pack(side=LEFT,padx=100)
pauseorresume=Button(root,command=butted,text="pause/resume",height=3,width=10).pack(side=RIGHT,padx=100)
root.mainloop()