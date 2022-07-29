"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Lab 3B - Depth Camera Cone Parking
"""

RealCar = False
# RealCar = True
# Change the line above to true when we are ready to test on the real car!
# If on the real car hold down the right bumper button to let the car drive

########################################################################################
# Imports
########################################################################################

import sys
import cv2 as cv
import numpy as np
import enum


sys.path.insert(1, "../../library")
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

########################################################################################
########################################################################################
########################################################################################
#
# Adjust the values in this section to tune how the car drives
#
# The HSV range for the color orange, stored as (hsv_min, hsv_max)
# Hint: You can use the widget in the lab2.ipynb to help tune this value
# In real-world conditions the car might see glare on the tape, washing out the colors
# We might also have a shadow making the color sometimes appear darker than others
# What is the best HSV range to only find the tape we want and avoid distractions?

hsv_lower = (160,100,170)
hsv_upper = (179,255,255)
ORANGE = (hsv_lower, hsv_upper)

# Area of the cone contour when we are the correct distance away (must be tuned)
GOAL_AREA = 27435.5

########################################################################################
########################################################################################
########################################################################################
#
# To fine-tune your car you may need to change values within this section. 
# 
# >> Constants
# The smallest contour we will recognize as a valid contour
MIN_CONTOUR_AREA = 30
# MIN_CONTOUR_AREA = 30 # Default

# Area of the cone contour when we should switch to reverse while aligning
REVERSE_AREA = GOAL_AREA * 1.25
# REVERSE_AREA = GOAL_AREA * 0.4 # Default

# Area of the cone contour when we should switch to forward while aligning
FORWARD_AREA = GOAL_AREA * 0.2
# FORWARD_AREA = GOAL_AREA * 0.2 # Default

# Speed to use in parking and aligning modes
PARK_SPEED = 0.25
# PARK_SPEED = 0.25 # Default

ALIGN_SPEED = 0.75
# ALIGN_SPEED = 0.75 # Default

# If desired speed/angle is under these thresholds, they are considered "close enough"
SPEED_THRESHOLD = 0.04
# SPEED_THRESHOLD = 0.04 # Default

ANGLE_THRESHOLD = 0.1
# ANGLE_THRESHOLD = 0.1 # Default


class Mode(enum.IntEnum):
    park = 0
    forward = 1
    reverse = 2
    
    
# >> Initialize these Variables
speed = 0.0  # The current speed of the car
angle = 0.0  # The current angle of the car's wheels
contour_center = None  # The (pixel row, pixel column) of contour
contour_area = 0  # The area of contour
cur_mode = Mode.forward

GOAL_DISTANCE = 300
########################################################################################
########################################################################################
########################################################################################
#
# To fine-tune your car you may need to change values within this section. 
# 
# >> Constants
# The smallest contour we will recognize as a valid contour
# Area of the cone contour when we should switch to reverse while aligning
REVERSE_DISTANCE = 380
# REVERSE_AREA = GOAL_AREA * 0.4 # Default

# Area of the cone contour when we should switch to forward while aligning
FORWARD_DISTANCE = 1000
# FORWARD_AREA = GOAL_AREA * 0.2 # Default

# Speed to use in parking and aligning modes
PARK_SPEED = 0.25
# PARK_SPEED = 0.25 # Default

ALIGN_SPEED = 0.75
# ALIGN_SPEED = 0.75 # Default

# If desired speed/angle is under these thresholds, they are considered "close enough"
SPEED_THRESHOLD = 0.04
# SPEED_THRESHOLD = 0.04 # Default

ANGLE_THRESHOLD = 0.1
# ANGLE_THRESHOLD = 0.1 # Default

center_distance = None

########################################################################################
# Functions
########################################################################################


def update_contour():
    """
    Finds contours in the current color image and uses them to update contour_center
    and contour_area
    """
    global contour_center
    global contour_area

    image = rc.camera.get_color_image()

    if image is None:
        contour_center = None
        contour_area = 0
    else:
        # Find all of the orange contours
        contours = rc_utils.find_contours(image, ORANGE[0], ORANGE[1])

        # Select the largest contour
        contour = rc_utils.get_largest_contour(contours, MIN_CONTOUR_AREA)

        if contour is not None:
            # Calculate contour information
            contour_center = rc_utils.get_contour_center(contour)
            contour_area = rc_utils.get_contour_area(contour)

            # Draw contour onto the image
            rc_utils.draw_contour(image, contour)
            rc_utils.draw_circle(image, contour_center)

        else:
            contour_center = None
            contour_area = 0

        # Display the image to the screen
        rc.display.show_color_image(image)


def start():
    """
    This function is run once every time the start button is pressed
    """
    global speed
    global angle

    # Initialize variables
    speed = 0
    angle = 0

    # Set initial driving speed and angle
    rc.drive.set_speed_angle(speed, angle)

    # Set update_slow to refresh every half second
    rc.set_update_slow_time(0.25)

    # Begin in "forward" mode
    cur_mode = Mode.forward

    # Print start message
    print(">> Lab 2 - Color Image Cone Driving")


def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    global speed
    global angle
    global cur_mode

    # Search for contours in the current color image
    update_contour()

    # Goal: Park the car 12 inches away from the closest orange cone
    
    # If no cone is found, stop
    if contour_center is None or contour_area == 0:
        speed = 0 # set the speed for the car to stop
        angle = 0 # set the angle for the car to stop pointing straight ahead
        
    else: # if a cone is found, run the next section of code
        # Use proportional control to set wheel angle based on contour x position
        angle = rc_utils.remap_range(contour_center[1], 0, rc.camera.get_width(), -1, 1)

        depth_image = rc.camera.get_depth_image()
        blur = cv.GaussianBlur(depth_image, (5, 5), 0)
        center_distance = blur[contour_center[0], contour_center[1]]
        #print('distance of contour center = '+str(center_distance))
        # PARK MODE: Move forward or backward until contour_area is GOAL_AREA
        if cur_mode == Mode.park:
            speed = rc_utils.remap_range(center_distance, GOAL_DISTANCE * 10, GOAL_DISTANCE, 1.0, 0.0)
            speed = rc_utils.clamp(speed, -PARK_SPEED, PARK_SPEED)

            # If speed is close to 0, round to 0 to "park" the car
            # if -SPEED_THRESHOLD < speed < SPEED_THRESHOLD:
                # speed = 0

            # If the angle is no longer correct, choose mode based on area
            if abs(angle) > ANGLE_THRESHOLD:
                cur_mode = Mode.forward if center_distance < FORWARD_DISTANCE else Mode.reverse

        
        # FORWARD MODE: Move forward until area is greater than REVERSE_AREA
        elif cur_mode == Mode.forward:
            speed = rc_utils.remap_range(center_distance, 0, REVERSE_DISTANCE, 1.0, 0.0)
            speed = rc_utils.clamp(speed, 0, ALIGN_SPEED)
            #print('Trying to move forward at speed: ',speed)

            # Once we pass REVERSE_AREA, switch to reverse mode
            if center_distance <= REVERSE_DISTANCE:
                cur_mode = Mode.reverse

            # If we are close to the correct angle, switch to park mode
            if abs(angle) < ANGLE_THRESHOLD:
                cur_mode = Mode.park

        # REVERSE MODE: move backward until area is less than FORWARD_AREA
        else:
            speed = rc_utils.remap_range(
                center_distance, REVERSE_DISTANCE, FORWARD_DISTANCE, -1.0, 0.0
            )
            speed = rc_utils.clamp(speed, -ALIGN_SPEED, 0)

            # Once we pass FORWARD_AREA, switch to forward mode
            if center_distance > FORWARD_DISTANCE:
                cur_mode = Mode.forward

            # If we are close to the correct angle, switch to park mode
            if abs(angle) < ANGLE_THRESHOLD:
                cur_mode = Mode.park

        # Reverse the angle if we are driving backward
        if speed < 0:
            angle *= -1

    # If the right button is not held down (as a kill switch)
    # 
    if rc.controller.is_down(rc.controller.Button.RB)==False and RealCar == True:
        speed = 0

    rc.drive.set_speed_angle(speed, angle)        
        
    if speed <= 0:
        speed = rc_utils.remap_range(speed,-1, 0, -1, -0.5)
    else:
        speed = rc_utils.remap_range(speed, 0, 1, 0.5, 1)
    # Print the current speed and angle when the A button (1 key) is held down
    if rc.controller.is_down(rc.controller.Button.A):
        print("Speed:", speed, "Angle:", angle)

    # Print the center and area of the largest contour when B button (2 key) is held down
    if rc.controller.is_down(rc.controller.Button.B):
        if contour_center is None:
            print("No contour found")
        else:
            print("Center:", contour_center, "Area:", contour_area, "Distance: ", center_distance)


def update_slow():
    """
    After start() is run, this function is run at a constant rate that is slower
    than update().  By default, update_slow() is run once per second
    """
    # Print a line of ascii text denoting the contour area and x position
    if rc.camera.get_color_image() is None:
        # If no image is found, print all X's and don't display an image
        print("X" * 10 + " (No image) " + "X" * 10)
    else:
        # If an image is found but no contour is found, print all dashes
        if contour_center is None:
            print("-" * 32 + " : area = " + str(contour_area))

        # Otherwise, print a line of dashes with a | indicating the contour x-position
        else:
            s = ["-"] * 32
            s[int(contour_center[1] / 20)] = "|"
            print("".join(s) + " : area = " + str(contour_area))


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()