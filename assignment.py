from __future__ import print_function

import time
from sr.robot import *


a_th = 2.0

d_th = 0.4 
token_list = [] # make the list for storing the code of the paired tokens

"""arena = True"""

R = Robot()
"""instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    
def turn(speed, seconds):
    """
    Function for setting an angular velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
 
def check_code(token_list,code):
    """
    Fuction to check if the token is already in list(which means the token is already paired)
    Returns:
        -1:if the token is already in list
        1:if the token isn't in list
    """
    for i in token_list:
        if (i == code):
            return -1
    return 1
    
def find_token():
    """
    Function to find the closest token

    Returns:
        dist (float): distance of the closest token (-1 if no token is detected)
        rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """
    dist = 100
    for token in R.see():
        if token.dist < dist and check_code(token_list,token.info.code) == 1:
            dist = token.dist
            rot_y = token.rot_y
            code = token.info.code
        
        
    if dist == 100:
        return -1, -1,0
    else:
        return dist, rot_y, code
        
def find_token_paired():
    """
    Fuction to find the closest token which has been already paired
    """
    dist = 100
    for token in R.see():
        if token.dist < dist and token.info.code == token_list[-2]:
            dist = token.dist
            rot_y = token.rot_y 
    if dist == 100:
        return -1,-1
    else:
        return dist, rot_y      
           

token_list.append(0)
        
while 1:
    dist, rot_y, code = find_token()  # we look for markers
    if dist == -1:
        if len(token_list) < 7:
            print("I don't see any token!!")
            turn(-10,1)  
        else:
            print("I put all the boxes together!")
            exit()
    elif dist < d_th:
        print("Found it!")
        if R.grab():  # if we are close to the token, we grab it.
            print("Gotcha!")
            token_list.append(code) # add code of the token which already grabbed
            if len(token_list) == 2:
                turn(-20,1)
                drive(20,0.5)
                R.release()
                drive(-20,0.5)
                turn(20,1)
            else:
                while 1: #loop for finding the paired tokens
                    dist_2, rot_y_2 = find_token_paired()
                    if dist_2 ==-1:
                        print("I don't see paired tokens!")
                        turn(-20,1)
                    
                    elif dist_2 < 1.5*d_th:
                        R.release()
                        drive(-20,1)
                        print("I got paired!")
                        break
                    elif -a_th <= rot_y_2 <= a_th:
                        print("Here there are!")
                        drive(20,1)
                    elif rot_y_2 < -a_th:
                        print("Left a bit...")
                        turn(-2,0.5)
                    elif rot_y_2 > a_th:
                        print("Right a bit...")
                        turn(+2,0.5)
        else:
            print("I'm not close enough")
    elif -a_th <= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
        print("Ah, here we are!.")
        drive(20, 1)
    elif rot_y < -a_th:  # if the robot is not well aligned with the token, we move it on the left or on the right
        print("Left a bit...")
        turn(-2, 0.5)
    elif rot_y > a_th:
        print("Right a bit...")
        turn(+2, 0.5)
    pass
