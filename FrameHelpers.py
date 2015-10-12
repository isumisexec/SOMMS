__author__ = 'John'
import os
import subprocess

"""
    This script contains functions to be used by multiple frame classes.
    This is both necessary to prevent circular dependencies and to provide another layer of abstraction.
    At time of writing the following functions were included:
            * Key bindings
            * Opening files with default programs
"""


def open_file_with_default_program(filename):
    """
        Attempts to open a file using the default program (e.g. open with Excel for a .csv, Word for a .docx).

        :param filename: The absolute path the file to be opened.
        :return: None
        """
    try:
        os.startfile(filename)  # Not sure if this will work cross platform. Try on Linux VM and Mac machine
    except AttributeError as e:
        subprocess.call(['open', filename])


def bind_keys(controller, widget_to_bind):
    # Recursive case ==> widget has children, pass each child back into recursive function
    if hasattr(widget_to_bind, 'children'):
        for widget in widget_to_bind.children:
            bind_keys(controller, widget_to_bind.children[widget])
    # Base Case ==> Bind keys to childless widget
    widget_to_bind.bind("<F1>", lambda e: controller.show_frame(controller.frame_set[1]))
    widget_to_bind.bind("<F2>", lambda e: controller.show_frame(controller.frame_set[2]))
    widget_to_bind.bind("<F3>", lambda e: controller.show_frame(controller.frame_set[3]))
    widget_to_bind.bind("<F4>", lambda e: controller.show_frame(controller.frame_set[4]))
    widget_to_bind.bind("<F5>", lambda e: controller.show_frame(controller.frame_set[5]))
    widget_to_bind.bind("<F6>", lambda e: controller.show_frame(controller.frame_set[6]))
    widget_to_bind.bind("<F7>", lambda e: controller.show_frame(controller.frame_set[7]))
    widget_to_bind.bind("<~>", lambda e: controller.show_frame(controller.frame_set[0]))
