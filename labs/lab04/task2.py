
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import easygopigo3 as go
#Impordib "easygopigo3" mooduli
import time
#Impordib "Time" mooduli


def main():
    #Funktsioon nimega main
    myRobot = go.EasyGoPiGo3()
    #See on klass mida kasutatakse, et kontrollida robotit
    myRobot.set_speed(500)
    #Set-ib kiiruse robotile, et kui kiiresti robot liigub, roboti kiirus on mõõdetud DPS-iga (Degrees per second) roboti ratastest
    myRobot.forward()
    #Liigutab Robotit otse
    time.sleep(1)
    #Ootab sekund
    myRobot.right()
    #Liigutab robotit paremale
    time.sleep(0.5)
    #Ootab poolsekundit
    myRobot.backward()
    #Liigutab Robotit tagurpidi
    time.sleep(1)
    #Ootab sekund
    myRobot.stop()
    #Peatab roboti liikumist
    myRobot.orbit(90, 5)
    #Juhib robotit, et ta tiirleks ümber objekti paremat pidi
    myRobot.orbit(-90, 5)
    #Teeb sama asja mida eelmine aga lihtsalt vasakut pidi
    myRobot.stop()
    #Peatab roboti liikumist


if __name__ == "__main__":
    main()
#kutsub välja main funktsiooni, kui seda faili käivitatakse
