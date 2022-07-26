class Display:
    """Display preferences."""
    MAIN_WIDTH, MAIN_HEIGHT = 1280, 720
    SMALL_IMG_WIDTH, SMALL_IMG_HEIGHT = 213, 120
    EXIT_IMAGE = 'exit_image.png'
    EXIT_KEY = 'esc'
    MAIN_IMAGE_TITLE = 'Hand Movements Presentation'
    WEBCAM_IMAGE_TITLE = 'Webcam'


class ControlFingers:
    """Control fingers preferences."""
    PREVIOUS_SLIDE_FINGER = [1, 0, 0, 0, 0]  # thumb
    NEXT_SLIDE_FINGER = [0, 0, 0, 0, 1]  # pinky finger
    POINT_FINGER = [0, 1, 1, 0, 0]  # index finger
    DRAW_FINGER = [0, 1, 0, 0, 0]  # index and middle fingers
    ERASE_FINGER = [1, 1, 1, 1, 1]  # all fingers of the hand
    CHANGE_COLOR_FINGER = [0, 1, 1, 1, 0]  # index, middle and ring
    EXIT_FINGER = [0, 0, 1, 1, 1]  # middle, ring and pinky

    POINTER_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255)]  # Main pointer colors
    POINTER_THICKNESS = 8  # Main pointer thickness


class ControlLine(ControlFingers):
    """Control line preferences."""
    GESTURE_THRESHOLD_MARGIN = 350
    GESTURE_THRESHOLD_THICKNESS = 10


class Delay:
    """Delay."""
    MAIN_DELAY = 20


class MessageBoxNotification:
    """Message box notifications - titles and messages."""
    ERROR_TITLE = 'Error'
    TYPE_ERROR_MESSAGE = 'Folder not selected. Try again.'
    ATTRIBUTE_ERROR_MESSAGE = 'Wrong folder selected. Try again.'
    INFO_FOLDER_TITLE = 'Attention'
    INFO_FOLDER_MESSAGE = 'Before you start the presentation, select a folder with slides.'
