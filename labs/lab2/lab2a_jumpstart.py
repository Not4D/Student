"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Lab 2A - Color Image Line Following
"""

########################################################################################
# Imports
########################################################################################

import sys
import cv2 as cv
import numpy as np

sys.path.insert(1, "../../library")
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# >> Constants
# The smallest contour we will recognize as a valid contour
MIN_CONTOUR_AREA = 30

# A crop window for the floor directly in front of the car
highest_row_to_keep = 360
CROP_FLOOR = ((highest_row_to_keep, 0), (rc.camera.get_height(), rc.camera.get_width()))

########################################################################################
########################################################################################
########################################################################################
# Colors, stored as a pair (hsv_min, hsv_max)
blue_hsv_min = (95,100, 85)
blue_hsv_max = (120,255, 255)
BLUE = (blue_hsv_min, blue_hsv_max)  # The HSV range for the color blue
# TODO (challenge 1): add HSV ranges for red, green, and yellow
red_hsv_min = (160, 100, 100)
red_hsv_max = (179,255, 255)
RED = (red_hsv_min, red_hsv_max)

green_hsv_min = (35, 100, 40)
green_hsv_max = (78,255, 255)
GREEN = (green_hsv_min, green_hsv_max)

yellow_hsv_min = (15, 145, 40)
yellow_hsv_max = (40,255, 255)
YELLOW = (yellow_hsv_min, yellow_hsv_max)

hsv_lower = (160,100,170)
hsv_upper = (176,255,255)

ORANGE = (hsv_lower, hsv_upper)
# >> Inialize Variables
speed = 0.0  # The current speed of the car
angle = 0.0  # The current angle of the car's wheels
contour_center = None  # The (pixel row, pixel column) of contour
contour_area = 0  # The area of contour
forwardSpeed = 0
backSpeed = 0

########################################################################################
# Functions
########################################################################################
def remap_range(
    val: float,
    old_min: float,
    old_max: float,
    new_min: float,
    new_max: float,
) -> float:
    """
    Remaps a value from one range to another range.

    Args:
        val: A number form the old range to be rescaled.
        old_min: The inclusive 'lower' bound of the old range.
        old_max: The inclusive 'upper' bound of the old range.
        new_min: The inclusive 'lower' bound of the new range.
        new_max: The inclusive 'upper' bound of the new range.

    Note:
        min need not be less than max; flipping the direction will cause the sign of
        the mapping to flip.  val does not have to be between old_min and old_max.
    """
    # TODO: remap val to the new range
    
    rangeI = old_max - old_min
    rangeF = new_max - new_min
    
    div = rangeF / rangeI
    
    val *= div
    val = new_min + val
    
    return val

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

        # Crop the image to the floor directly in front of the car
        image = rc_utils.crop(image, CROP_FLOOR[0], CROP_FLOOR[1])

########################################################################################
########################################################################################
########################################################################################

        # TODO (challenge 1): Search for multiple tape colors with a priority order
        # (currently we only search for blue)
        # Find all of the blue contours
        blue_contours = rc_utils.find_contours(image, BLUE[0], BLUE[1])
        yellow_contours = rc_utils.find_contours(image, YELLOW[0], YELLOW[1])
        red_contours = rc_utils.find_contours(image, RED[0], RED[1])
        green_contours = rc_utils.find_contours(image, GREEN[0], GREEN[1])
        # Hint: Find contours for each color
        # Check with if statements to see if we have colors in the following priority order:
        # Drive if we see blue
        # Unless we see green (higher priority)
        # or unless we see yellow (even higher priority)
        # or unless we see red (highest priority)
        # Save the highest priority set of contours as contours
        checkR = rc_utils.get_largest_contour(red_contours, MIN_CONTOUR_AREA)
        checkY = rc_utils.get_largest_contour(yellow_contours, MIN_CONTOUR_AREA)
        checkG = rc_utils.get_largest_contour(green_contours, MIN_CONTOUR_AREA)
        
        if checkR is not None:
            contours = red_contours
        elif checkY is not None:
            contours = yellow_contours
        elif checkG is not None:
            contours = green_contours
        else:
            contours = blue_contours
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
        # rc.display.show_color_image(image)


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

    # Print start message
    print(
        ">> Lab 2A - Color Image Line Following\n"
        "\n"
        "Controls:\n"
        "    Right trigger = accelerate forward\n"
        "    Left trigger = accelerate backward\n"
        "    A button = print current speed and angle\n"
        "    B button = print contour center and area"
    )


def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    global speed
    global angle

    # Search for contours in the current color image
    update_contour()

    

    # Choose an angle based on contour_center
    # If we could not find a contour, keep the previous angle
    if contour_center is not None:
########################################################################################
########################################################################################
########################################################################################

        # Current implementation: bang-bang control (very choppy)
        # TODO (warmup): Implement a smoother way to follow the line
        angle = remap_range(contour_center[1], 0, 640, -1, 1)

    # Use the triggers to control the car's speed
    forwardSpeed = rc.controller.get_trigger(rc.controller.Trigger.RIGHT)
    backSpeed = rc.controller.get_trigger(rc.controller.Trigger.LEFT)
    speed = (forwardSpeed - backSpeed) * 0.85

    if speed <= 0.4:
        remap_range(speed, 0, 0.8, 0, 1)
    
    rc.drive.set_speed_angle(speed, angle)

    # Print the current speed and angle when the A button is held down
    if rc.controller.is_down(rc.controller.Button.A):
        print("Speed:", speed, "Angle:", angle)

    # Print the center and area of the largest contour when B is held down
    if rc.controller.is_down(rc.controller.Button.B):
        if contour_center is None:
            print("No contour found")
        else:
            print("Center:", contour_center, "Area:", contour_area)


def update_slow():
    """
    After start() is run, this function is run at a constant rate that is slower
    than update().  By default, update_slow() is run once per second
    """
    # Print a line of ascii text denoting the contour area and x-position
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