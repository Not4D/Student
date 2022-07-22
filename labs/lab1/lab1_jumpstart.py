"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Lab 1 - Driving in Shapes
"""

########################################################################################
# Imports
########################################################################################

import sys

sys.path.insert(1, "../../library")
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# Put any global variables here
global isCircle
global isSquare
global isEight
global isShape
global isDriving
global counter



########################################################################################
# Functions
########################################################################################


def start():
    """
    This function is run once every time the start button is pressed
    """
    # Begin at a full stop
    rc.drive.stop()
    global isCircle
    global isSquare
    global isShape
    global isEight
    global isDriving
    global counter

    counter = 0
    isCircle = False
    isSquare = False
    isShape = False
    isEight = False
    isDriving = False

    # Print start message
    # TODO : change the line explaining what the Y button does 
    # for your chosen shape
    print(
        ">> Lab 1 - Driving in Shapes\n"
        "\n"
        "Controls:\n"
        "    Right trigger = accelerate forward\n"
        "    Left trigger = accelerate backward\n"
        "    Left joystick = turn front wheels\n"
        "    1 key / A button = drive in a circle\n"
        "    2 key / B button = drive in a square\n"
        "    3 key / X button = drive in a figure eight\n"
        "    4 key / Y button = drive in a triangle\n"
    )


def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    # Tell Python we're going to use our global variables
    global isCircle
    global isSquare
    global isEight
    global isShape
    global isDriving
    global counter
    
    # Set up the sim to take commands for 
    # acceleration and steering as if a person 
    # is driving
    rc.drive.set_speed_angle(0, 0)
    
    # Left trigger is the left shift key on keyboard
    left_trigger = rc.controller.get_trigger(rc.controller.Trigger.LEFT)
    
    # Right trigger is the right shift key on keyboard
    right_trigger = rc.controller.get_trigger(rc.controller.Trigger.RIGHT)
    
    # Left joystick is the letters 'a' and 'd' on keyboard    
    left_joystick = rc.controller.get_joystick(rc.controller.Joystick.LEFT)

    speed = right_trigger - left_trigger
    angle = left_joystick[0] 
    # Check to see if the user is inputting driving commands
    if speed > 0 or speed < 0:
        isDriving = True
    if isDriving:
        # If we want to have the user drive, stop the commands for driving in a shape
        isCircle = False
        isSquare = False
        isShape = False
        isEight = False

        rc.drive.set_speed_angle(speed,angle)
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
        # Remember:
        # Valid speeds: -1 (backwards) to 1 (forward)
        # Valid angles: -1 (left) to +1 (right)
# Our work begin below this line:

    # A button (controller) is 1 key on laptop
    if rc.controller.was_pressed(rc.controller.Button.A):
        print("Driving in a circle...")
        # TODO (main challenge): Drive in a circle
        # set isCircle to True, our other globals should be False
        isCircle = True
        isDriving =  False
        isSquare = False
        isEight =  False
        isShape =  False
    if isCircle:
        speed =  1 # Change this to a number
        angle =  1 # Change this to a number
        rc.drive.set_speed_angle(speed, angle)

    # B button (controller) is 2 key on laptop
    # TODO (main challenge): Drive in a square when the B button is pressed
    if rc.controller.was_pressed(rc.controller.Button.B):
        print("Driving in a square...")
        # Which variables should be set to True
        # and which should be set to False?
        isCircle =  False# 
        isDriving =  False #
        isSquare =  True #
        isEight =  False #
        isShape =  False #
    if isSquare:
        counter += rc.get_delta_time()
        
        side_drive_time =  3 # enter a number in seconds
        turn_drive_time =  2.06 # enter a number in seconds
        
        straight_speed =  1 # enter a number for speed
        straight_angle =  0 # enter a number for angle

        turn_speed =  .25 # enter a number for speed
        turn_angle = 1 # enter a number for angle
        
        if counter < side_drive_time:
        # Drive forward at full speed for one second or more
            rc.drive.set_speed_angle(straight_speed, straight_angle)
            
        elif counter <= turn_drive_time + side_drive_time:
        # Turn left or right at full speed for the next time interval.
        # How long do you need to turn to change direction by 90 degrees?
        # Test it out in the simulator!
            rc.drive.set_speed_angle(turn_speed, turn_angle)
            
        else:
        # Reset counter back to 0 after we complete the turn
        # This will have us start over and do another straight side
            counter = 0


    # X button (controller) is 3 key on laptop
    # TODO (main challenge): Drive in a figure eight when the X button is pressed
    
    if rc.controller.was_pressed(rc.controller.Button.X):
        print("Driving in a figure eight...")
        # Which variables should be set to True
        # and which should be set to False?
        isCircle = False #
        isDriving = False #
        isSquare = False #
        isEight = True #
        isShape = False #
    if isEight:
        counter += rc.get_delta_time()
        
        turn_drive_time_1 = 5 # # enter a number in seconds
        turn_drive_time_2 = 5 # # enter a number in seconds

        turn_speed_1 = 1 # # enter a number for speed
        turn_angle_1 = 1 # # enter a number for angle

        turn_speed_2 = 1 # # enter a number for speed
        turn_angle_2 = -1 # # enter a number for angle`
        
        if counter < turn_drive_time_1:
        # Drive a full circle in one direction
         # How long do we need to turn to make one full circle?
            rc.drive.set_speed_angle(turn_speed_1, turn_angle_1)
            
        elif counter <= turn_drive_time_2 + turn_drive_time_1:
        # Turn left or right at full speed for the next time interval.
        # How long do you need to turn to change direction by 90 degrees?
        # Test it out in the simulator!
            rc.drive.set_speed_angle(turn_speed_2, turn_angle_2)
            
        else:
        # Reset counter back to 0 after we complete the second turn
        # This will have us start over and do another loop in the first direction
            counter = 0



    # Y button (controller) is 4 key on laptop
    # TODO (main challenge): Drive in a shape of your choice 
    # when the Y button is pressed
    # 
    # Hint: you can copy and paste the code from a shape above 
    # to use as a starting point!
    # Think together as a team about what shape you want to make and 
    # draw it up in 'pseudocode' before you put it into python syntax
    if rc.controller.was_pressed(rc.controller.Button.Y):
        print("Driving in a square...")
        # Which variables should be set to True
        # and which should be set to False?
        isCircle =  False# 
        isDriving =  False #
        isSquare =  False #
        isEight =  False #
        isShape =  True #
        if isShape:
            counter += rc.get_delta_time()
        

            side_drive_time =  2 # enter a number in seconds
            turn_drive_time =  3.1 # enter a number in seconds
        
            straight_speed =  1 # enter a number for speed
            straight_angle =  0 # enter a number for angle

            turn_speed =  .25 # enter a number for speed
            turn_angle = 1 # enter a number for angle
        
        if counter < side_drive_time:
        # Drive forward at full speed for one second or more
            rc.drive.set_speed_angle(straight_speed, straight_angle)
            
        elif counter <= turn_drive_time + side_drive_time:
        # Turn left or right at full speed for the next time interval.
        # How long do you need to turn to change direction by 90 degrees?
        # Test it out in the simulator!
            rc.drive.set_speed_angle(turn_speed, turn_angle)
            
        else:
        # Reset counter back to 0 after we complete the turn
        # This will have us start over and do another straight side
            counter = 0
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update)
    rc.go()
