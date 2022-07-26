import os
import cv2
import numpy as np
import tkinter.messagebox as mb

from cvzone.HandTrackingModule import HandDetector

from misc import Delay, Display, ControlLine, ControlFingers, MessageBoxNotification
from auxiliary_functions import clear_space, choose_directory

# Variables
# Starting color value
COLOR_NUMBER = 0
# The beginning of the presentation
IMAGE_NUMBER = 0
# Exit delay
EXIT_COUNTER = 0
# The path to the directory and to every individual image
DIRECTORY_PATH = ''
IMAGES_PATH_LIST = []

# Slides switching delay
SLIDE_SWITCHED = False
SLIDE_NUMBER = 0

# Storing and changing drawn points
ANNOTATIONS, ANNOTATION_NUMBERS, ANNOTATION_STARTS = {}, {}, {}
ANNOTATIONS, ANNOTATION_NUMBERS, ANNOTATION_STARTS = clear_space(colors=ControlFingers.POINTER_COLORS,
                                                                 annotations=ANNOTATIONS,
                                                                 annotation_numbers=ANNOTATION_NUMBERS,
                                                                 annotation_starts=ANNOTATION_STARTS)
# Start / break presentation flags and images
START_FLAG = True
START_IMG = cv2.imread(Display.START_IMAGE)
EXIT_FLAG = False
EXIT_IMG = cv2.imread(Display.EXIT_IMAGE)

# Camera setup
cap = cv2.VideoCapture(0)
cap.set(3, Display.MAIN_WIDTH)
cap.set(4, Display.MAIN_HEIGHT)

# Hand detector
detector = HandDetector(detectionCon=0.5, maxHands=1)

# Loop
while True:
    if START_FLAG:  # So that you can exit and turn on another presentation
        # Start window
        cv2.imshow(winname=Display.MAIN_IMAGE_TITLE, mat=START_IMG)
        key = cv2.waitKey(0)
        if key == ord(Display.EXIT_KEY):
            break
        else:
            # Choose main directory
            DIRECTORY_PATH = choose_directory(title=MessageBoxNotification.INFO_FOLDER_TITLE)
            # Get the list of presentation images
            IMAGES_PATH_LIST = sorted(os.listdir(DIRECTORY_PATH), key=len)  # in case we have more than 10 files
            START_FLAG = False
    else:
        # Importing images
        success, img = cap.read()
        img = cv2.flip(src=img, flipCode=1)
        try:
            full_image_path = os.path.join(DIRECTORY_PATH, IMAGES_PATH_LIST[IMAGE_NUMBER])
        except TypeError:
            mb.showerror(title=MessageBoxNotification.ERROR_TITLE,
                         message=MessageBoxNotification.TYPE_ERROR_MESSAGE)
            START_FLAG = True
            continue
        current_img = cv2.imread(full_image_path)
        hands, img = detector.findHands(img=img)
        cv2.line(img=img, pt1=(0, ControlLine.GESTURE_THRESHOLD_MARGIN),
                 pt2=(Display.MAIN_WIDTH, ControlLine.GESTURE_THRESHOLD_MARGIN),
                 # The same color as the pointer to make it easier to navigate
                 color=ControlLine.POINTER_COLORS[COLOR_NUMBER],
                 thickness=ControlLine.GESTURE_THRESHOLD_THICKNESS)

        # Gestures
        if hands and SLIDE_SWITCHED is False:
            hand = hands[0]
            fingers = detector.fingersUp(myHand=hand)
            # Check that our hand is above the line
            center_x, center_y = hand['center']  # Coordinates of the center of the hand
            landmark_list = hand['lmList']

            # Constrain values for easier drawing (converting one range to another)
            x_value = int(np.interp(x=landmark_list[8][0],
                                    xp=[Display.MAIN_WIDTH * 0.4, Display.MAIN_WIDTH * 0.8],
                                    fp=[0, Display.MAIN_WIDTH])
                          )  # landmark_list[8][0] - x index finger tip
            y_value = int(np.interp(x=landmark_list[8][1],
                                    xp=[Display.MAIN_HEIGHT * 0.25, Display.MAIN_HEIGHT * 0.75],
                                    fp=[0, Display.MAIN_HEIGHT])
                          )  # landmark_list[8][1] - y index finger tip
            index_finger = x_value, y_value

            if center_y <= ControlLine.GESTURE_THRESHOLD_MARGIN:  # if hand is at the height of the face

                # Gesture 1 - back (previous slide)
                if fingers == ControlFingers.PREVIOUS_SLIDE_FINGER:
                    if IMAGE_NUMBER > 0:
                        SLIDE_SWITCHED = True
                        # Clear the space when we move to the previous slide
                        ANNOTATIONS, ANNOTATION_NUMBERS, ANNOTATION_STARTS = \
                            clear_space(colors=ControlFingers.POINTER_COLORS, annotations=ANNOTATIONS,
                                        annotation_numbers=ANNOTATION_NUMBERS, annotation_starts=ANNOTATION_STARTS)
                        IMAGE_NUMBER -= 1

                # Gesture 2 - forward (next slide)
                if fingers == ControlFingers.NEXT_SLIDE_FINGER:
                    if IMAGE_NUMBER < len(IMAGES_PATH_LIST) - 1:
                        SLIDE_SWITCHED = True
                        # Clear the space when we move to the next slide
                        ANNOTATIONS, ANNOTATION_NUMBERS, ANNOTATION_STARTS = \
                            clear_space(colors=ControlFingers.POINTER_COLORS, annotations=ANNOTATIONS,
                                        annotation_numbers=ANNOTATION_NUMBERS, annotation_starts=ANNOTATION_STARTS)
                        IMAGE_NUMBER += 1

            # Gesture 3 - show pointer
            if fingers == ControlFingers.POINT_FINGER:
                cv2.circle(img=current_img, center=index_finger, radius=ControlFingers.POINTER_THICKNESS,
                           color=ControlFingers.POINTER_COLORS[COLOR_NUMBER], thickness=cv2.FILLED)

            # Gesture 4 - draw pointer
            if fingers == ControlFingers.DRAW_FINGER:
                # Making separate containers
                if ANNOTATION_STARTS[COLOR_NUMBER] is False:
                    ANNOTATION_STARTS[COLOR_NUMBER] = True
                    ANNOTATION_NUMBERS[COLOR_NUMBER] += 1
                    ANNOTATIONS[COLOR_NUMBER].append([])
                cv2.circle(img=current_img, center=index_finger, radius=ControlFingers.POINTER_THICKNESS,
                           color=ControlFingers.POINTER_COLORS[COLOR_NUMBER], thickness=cv2.FILLED)
                # Adding points to that container
                ANNOTATIONS[COLOR_NUMBER][ANNOTATION_NUMBERS[COLOR_NUMBER]].append(index_finger)
            else:
                # Change the container so that we can then draw a new line when the fingers are raised again
                ANNOTATION_STARTS[COLOR_NUMBER] = False

            # Gesture 5 - erase
            if fingers == ControlFingers.ERASE_FINGER:
                if ANNOTATIONS[COLOR_NUMBER] and ANNOTATION_NUMBERS[COLOR_NUMBER] >= 0:
                    ANNOTATIONS[COLOR_NUMBER].pop(-1)  # Removes the last one
                    ANNOTATION_NUMBERS[COLOR_NUMBER] -= 1
                    SLIDE_SWITCHED = True

            # Gesture 6 - change color
            if fingers == ControlFingers.CHANGE_COLOR_FINGER:
                if COLOR_NUMBER < len(ControlFingers.POINTER_COLORS) - 1:
                    COLOR_NUMBER += 1
                else:
                    COLOR_NUMBER = 0
                SLIDE_SWITCHED = True  # Making a delay

            # Gesture 7 - exit
            if fingers == ControlFingers.EXIT_FINGER:
                if EXIT_COUNTER == Delay.EXIT_DELAY:  # delay
                    # Clear the space when we want to leave (not necessarily going out)
                    ANNOTATIONS, ANNOTATION_NUMBERS, ANNOTATION_STARTS = \
                        clear_space(colors=ControlFingers.POINTER_COLORS, annotations=ANNOTATIONS,
                                    annotation_numbers=ANNOTATION_NUMBERS, annotation_starts=ANNOTATION_STARTS)
                    EXIT_FLAG = True
                else:
                    EXIT_COUNTER += 1

            # Gesture 8 - exit confirm
            if EXIT_FLAG:
                # Displaying the exit image
                current_img = cv2.imread(Display.EXIT_IMAGE)
                EXIT_COUNTER = 0
                if fingers == ControlFingers.EXIT_CONFIRM_FINGER:  # confirm
                    cv2.destroyAllWindows()
                    START_FLAG = True
                    EXIT_FLAG = False
                    continue
                elif fingers == ControlFingers.EXIT_DECLINE_FINGER:  # decline
                    current_img = cv2.imread(full_image_path)  # back to the current slide
                    EXIT_FLAG = False

        # Drawing points of all colors
        for color in range(len(ControlFingers.POINTER_COLORS)):
            for i in range(len(ANNOTATIONS[color])):
                for j in range(len(ANNOTATIONS[color][i])):
                    if j != 0:  # To avoid an error
                        cv2.line(img=current_img,
                                 pt1=ANNOTATIONS[color][i][j - 1],
                                 pt2=ANNOTATIONS[color][i][j],
                                 color=ControlFingers.POINTER_COLORS[color],
                                 thickness=ControlFingers.POINTER_THICKNESS)

        # Slide switched iterations (making delay)
        if SLIDE_SWITCHED:
            SLIDE_NUMBER += 1
            if SLIDE_NUMBER > Delay.SLIDES_DELAY:
                SLIDE_NUMBER = 0
                SLIDE_SWITCHED = False

        # Adding webcam image on the slides
        try:
            # width and height of the slides (since we don't know their dimensions)
            current_img_height, current_img_width, channel = current_img.shape
        except AttributeError:
            mb.showerror(title=MessageBoxNotification.ERROR_TITLE,
                         message=MessageBoxNotification.ATTRIBUTE_ERROR_MESSAGE)
            START_FLAG = True
            continue
        # Customize the size of the webcam window
        webcam_img = cv2.resize(img, (int(current_img_width / 5), int(current_img_height / 5)))
        # Integrating the camera on the slide (using the appropriate coordinates to insert in the upper right corner)
        current_img[0:int(current_img_height / 5), current_img_width - int(current_img_width / 5):current_img_width] \
            = webcam_img

        # Main windows
        cv2.imshow(winname=Display.WEBCAM_IMAGE_TITLE, mat=img)
        cv2.imshow(winname=Display.MAIN_IMAGE_TITLE, mat=current_img)
        cv2.waitKey(1)

cv2.destroyAllWindows()
