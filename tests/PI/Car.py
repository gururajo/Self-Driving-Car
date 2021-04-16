# Output, value defaults to 0
# [GPIO, OUTPUT <, value >]

# Servo, value defaults to 1500, min to 1000, max to 2000
# [GPIO, SERVO <, value <, min <, max > > >]

# PWM, value defaults to 0, min to 0, max to 255
# [GPIO, PWM <, value <, min <, max > > >]
import pigpio
class Car:
    angle = 1545
    throttle = 50
    servoPIN = 15
    motorfor=22
    motorrev=27
    motorthrottle=17
    pi=pigpio.pi()


    def setthrottle(self, throtttle):
        throtttle=int(throtttle)
        if 0 <= throtttle <= 255:
            self.throttle = throtttle
            self.pi.set_PWM_dutycycle(self.motorthrottle,self.throttle)
        print(throtttle)

    def gettrottle(self):

        return self.throttle

    def steer(self, angle):
        angle=int(angle)
        if 1285 <= angle <= 1800:
            self.angle = angle
            self.pi.set_servo_pulsewidth(self.servoPIN, self.angle)
        #print("steer")
    def forward(self):
        self.pi.write(self.motorfor,1)
        self.pi.write(self.motorrev,0)
        print("forward")
    def reverse(self):
        self.pi.write(self.motorfor,0)
        self.pi.write(self.motorrev,1)
        print("reverse")
    def brake(self):
        self.pi.write(self.motorfor,0)
        self.pi.write(self.motorrev,0)
        self.pi.set_PWM_dutycycle(self.motorthrottle,50)
        print("break")
    def stop(self):
        self.pi.write(self.motorfor,0)
        self.pi.write(self.motorrev,0)
        print("stop")
    def quitfunc(self):
        self.pi.stop()
        
        


if __name__ == '__main__':
    car = Car()
    car.steer(1289)
    print(car.angle)

