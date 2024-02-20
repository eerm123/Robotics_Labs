import easygopigo3 as go
import time

myRobot = go.EasyGoPiGo3()

def move_forward_seconds(t):
    myRobot.forward()
    myRobot.led_on(2)
    time.sleep(t)
    myRobot.led_off(2)
    myRobot.stop()

def orbit_right():
    myRobot.orbit(60, 5)
    myRobot.led_on(0)
    myRobot.stop()
    myRobot.led_off(0)

def orbit_little_right():
    myRobot.orbit(50, 5)
    myRobot.led_on(0)
    myRobot.stop()
    myRobot.led_off(0)
    
def main():
    move_forward_seconds(1)
    orbit_right()
    move_forward_seconds(0.7)
    orbit_little_right()
    move_forward_seconds(3.5)
    orbit_right()
    move_forward_seconds(0.7)
    orbit_little_right()
    move_forward_seconds(1.5)
    

"""    
    for i in range(1):            
        myRobot = go.EasyGoPiGo3()
        
        myRobot.set_speed(600)
        myRobot.forward()
        myRobot.led_on(0,1)
        time.sleep(0.5)
        myRobot.stop()
        myRobot.orbit(60, 5)
        myRobot.led_on(0)
        myRobot.forward()
        myRobot.led_on(0,1)
        time.sleep(0.5)
        myRobot.orbit(50, 5)
        myRobot.led_on(0)
        myRobot.forward()
        myRobot.led_on(0,1)
        time.sleep(1.85)
        myRobot.orbit(60, 5)
        myRobot.led_on(0)
        myRobot.forward()
        myRobot.led_on(0,1)
        time.sleep(0.5)
        myRobot.orbit(50, 5)
        myRobot.led_on(0)
        myRobot.forward()
        time.sleep(0.5)
        myRobot.stop()
"""        

if __name__ == "__main__":
    main()