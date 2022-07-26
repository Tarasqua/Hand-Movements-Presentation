import os
import tkinter.filedialog as fd


def choose_directory(title: str):
    """
    The initial window for selecting a directory with slides.
    :return: Path to directory.
    """
    directory = fd.askdirectory(title=title, initialdir=os.getcwd())
    if directory:
        return directory


def clear_space(colors: list, annotations: dict, annotation_numbers: dict, annotation_starts: dict):
    """
    Clears the slide of drawings.
    :param colors: List of pointer colors
    :param annotations: where the coordinates of each point of the drawing
           will be recorded under a specific key = color number
    Are necessary to separate the lines from each other:
    :param annotation_numbers: each line has its own number (the same key)
    :param annotation_starts: indicates that the construction of
           a particular line has ended (the same key)
    :return:
    """
    for color_number in range(len(colors)):
        annotations[color_number] = [[]]  # [[]] - To draw each line separately, independently of the previous one
        annotation_numbers[color_number] = 0
        annotation_starts[color_number] = False
    return annotations, annotation_numbers, annotation_starts