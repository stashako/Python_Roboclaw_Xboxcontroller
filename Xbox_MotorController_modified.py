from roboclaw import Roboclaw

import pygame
pygame.init()

rc = Roboclaw("/dev/ttyACM0",115200)
rc.Open()
address = 0x80


def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def main():
    throttle = 0
    direction = 0
    leftMotor = 0
    rightMotor = 0
    maxMotorScale = 0
    leftMotorScaled = 0
    rightMotorScaled = 0
    deadzone = 0.05

    joysticks = []
    clock = pygame.time.Clock()
    keepPlaying = True
 
    # for al the connected joysticks
    for i in range(0, pygame.joystick.get_count()):
        # create an Joystick object in our list
        joysticks.append(pygame.joystick.Joystick(i))
        # initialize them all (-1 means loop forever)
        joysticks[-1].init()
        # print a statement telling what the name of the controller is
        print "Detected joystick '",joysticks[-1].get_name(),"'"
    while keepPlaying:
          throttle = 0
          direction = 0
        
        for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONUP:
                    print "Received event 'Quit', exiting."
                    rc.ForwardM1(address,0)
                    rc.ForwardM2(address,0)
                    keepPlaying = False
                elif event.type == pygame.JOYAXISMOTION:
                    print "Joystick '",joysticks[event.joy].get_name(),"' axis:",event.axis,"' Val:",event.value 
                    if event.axis == 0:
                        throttle = event.value
                    if event.axis == 1:
                        direction = event.value
                    leftMotor = throttle-direction
                    rightMotor = throttle+direction
                    maxMotorScale = max(leftMotor,rightMotor)
                    maxMotorScale = max(1,maxMotorScale)
                    leftMotorScaled = constrain(leftMotor/maxMotorScale,-1,1)
                    rightMotorScaled = constrain(rightMotor/maxMotorScale,-1,1)
        
                        
                    if leftMotorScaled <= -1 * deadzone:
                          rc.ForwardM2(address,int(abs(leftMotorScaled)*88))
                    elif leftMotorScaled >= deadzone:
                            rc.BackwardM2(address,int(abs(leftMotorScaled)*88))
                    elif leftMotorScaled == 0:
                            rc.ForwardM2(address,0)
                            
                    if rightMotorScaled <= -1 * deadzone:
                          rc.ForwardM1(address,int(abs(rightMotorScaled)*88))
                    elif rightMotorScaled >= deadzone:
                            rc.BackwardM1(address,int(abs(rightMotorScaled)*88))
                    elif rightMotorScaled == 0:
                            rc.ForwardM1(address,0)                       
                        

main()
pygame.quit()
