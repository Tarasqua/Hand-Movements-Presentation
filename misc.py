class Display:
    """Display preferences."""
    MAIN_WIDTH, MAIN_HEIGHT = 1280, 720
    EXIT_IMAGE = 'data/shutdown_window.png'
    START_IMAGE = 'data/launch_window.png'
    MAIN_IMAGE_TITLE = 'Hand Movements Presentation'
    WEBCAM_IMAGE_TITLE = 'Webcam'
    EXIT_KEY = 'e'


class ControlFingers:
    """Control fingers preferences."""
    PREVIOUS_SLIDE_FINGER = [1, 0, 0, 0, 0]  # thumb
    NEXT_SLIDE_FINGER = [0, 0, 0, 0, 1]  # pinky finger
    POINT_FINGER = [0, 1, 1, 0, 0]  # index and middle finger
    DRAW_FINGER = [0, 1, 0, 0, 0]  # index fingers
    ERASE_FINGER = [0, 1, 1, 0, 1]  # index, middle and pinky
    CHANGE_COLOR_FINGER = [1, 1, 1, 0, 0]  # index, middle and thumb
    EXIT_FINGER = [1, 1, 1, 1, 1]  # middle, ring and pinky
    EXIT_CONFIRM_FINGER = [0, 0, 1, 1, 1]  # middle, ring, pinky
    EXIT_DECLINE_FINGER = [1, 0, 0, 0, 1]  # thumb and pinky

    POINTER_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255)]  # Main pointer colors
    POINTER_THICKNESS = 8  # Main pointer thickness


class ControlLine(ControlFingers):
    """Control line preferences."""
    GESTURE_THRESHOLD_MARGIN = 350
    GESTURE_THRESHOLD_THICKNESS = 10


class Delay:
    """Delay."""
    SLIDES_DELAY = 20
    EXIT_DELAY = 50


class MessageBoxNotification:
    """Message box notifications - titles and messages."""
    ERROR_TITLE = 'Error'
    TYPE_ERROR_MESSAGE = 'Folder not selected. Try again.'
    ATTRIBUTE_ERROR_MESSAGE = 'Wrong folder selected. Try again.'
    INFO_FOLDER_TITLE = 'Attention'
    INFO_FOLDER_MESSAGE = 'Before you start the presentation, select a folder with slides.'
