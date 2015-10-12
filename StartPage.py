__author__ = 'John'
from tkinter import ttk
from Globals import *


class StartPageAlt(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.container = ttk.Frame(self)
        self.container.pack(padx=padx_default, pady=pady_default)
        self.logo_label = ttk.Label(self.container, image=controller.image, takefocus=False)
        self.logo_label.image = controller.image
        # Apparently have to do this to prevent the image from being garbage collected
        self.logo_label.pack(padx=5, pady=5)

        self.intro_text_logo = ttk.Label(self.container,
                                         text="Welcome to the Student Organization Membership Management System V3.1",
                                         font=Superhead)
        self.intro_text_logo.pack(padx=5, pady=5)

        self.creator_plug = ttk.Label(self.container, text="Brought to you by John Rolf and the MIS Club",
                                      font=Superhead)
        self.creator_plug.pack(padx=5, pady=5)

        self.directions_label = ttk.Label(self.container, text="Use the file menu in the top left or the "
                                          "keyboard commands to navigate.", font=Head)
        self.directions_label.pack(padx=5, pady=5)

        self.other_directions__label = ttk.Label(self.container, text="F1\t Start Checking in\n"
                                                 "F2\t Create an event\n"
                                                 "F3\t Report Handling\n"
                                                 "F4\t Data Analysis\n"
                                                 "F5\t Email Management\n"
                                                 "F6\t Start of Semester\n"
                                                 "F7\t End of Semester\n"
                                                 "~\t Start Page\n"
                                                 "Esc\t Quit",
                                                 font=Subhead)
        self.other_directions__label.pack(padx=5, pady=5)

    def set_focus(self):
        self.directions_label.focus()
        return