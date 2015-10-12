__author__ = 'John'
from Globals import *
import MIS_Database_Functions

import tkinter as tk
from tkinter import ttk
import sqlite3


class EndOfSemesterAlt(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ######################################################
        #                   SIDE FRAME                       #
        ######################################################
        self.logo_border = ttk.Label(self, border=border_default, relief=relief_default, takefocus=False)
        self.logo_border.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew")

        self.logo_label = ttk.Label(self, image=controller.image, takefocus=False)
        self.logo_label.image = controller.image
        self.logo_label.grid(row=0, column=0, rowspan=4, columnspan=3)

        self.side_frame = ttk.Label(self, border=border_default, relief=relief_default, takefocus=False)
        self.side_frame.grid(row=4, column=0, rowspan=6, columnspan=3, sticky="nsew")

        self.frame_title = ttk.Label(self, text="END OF SEMESTER", font=Superhead, takefocus=False)
        self.frame_title.grid(row=4, column=0, columnspan=3, rowspan=1)

        self.file_label = ttk.Label(self, text="Update Member\n"
                                               "Dues Status", font=Head)
        self.file_label.grid(row=5, column=0, columnspan=3, rowspan=2)

        self.instructions = ttk.Label(self, text="If you are not the tech\n"
                                                 "director, you probably,\n"
                                                 "shouldn't be here.     \n\n"
                                                 "Click the button to the\n"
                                                 "right when the semester\n"
                                                 "is over and member dues\n"
                                                 "need to be decremented.\n\n"
                                                 "Make ABSOLUTELY SURE,  \n"
                                                 "before doing this.")
        self.instructions.grid(row=7, column=0, columnspan=3, rowspan=3, sticky="nw", padx=(10, 10))

        self.content_border_label = ttk.Label(self, border=border_default, relief=relief_default)
        self.content_border_label.grid(row=0, column=3, sticky="nsew", rowspan=7, columnspan=7)
        ###################################################
        #                 MAIN CONTENTS                   #
        ###################################################
        self.end_of_semester_button = ttk.Button(self, text="RUN END OF SEMESTER",
                                                 command=lambda: self.run_end_of_semester(),
                                                 style="DataRemover.TButton")
        self.end_of_semester_button.grid(row=2, column=6, sticky="nsew")

        self.verification_entry = ttk.Entry(self)
        self.verification_entry.grid(row=3, column=6, sticky="ew")

        self.feedback_label_border = ttk.Label(self, border=border_default, relief=relief_default)
        self.feedback_label_border.grid(row=7, column=3, rowspan=3, columnspan=7, sticky="nsew")
        self.feedback_label = ttk.Label(self, text="Awaiting Button Click",
                                        font=Subhead)
        self.feedback_label.grid(row=7, column=3, rowspan=3, columnspan=7, pady=(5, 5), padx=(5, 5))

    def run_end_of_semester(self, event=None):
        verification_code = self.verification_entry.get()
        if verification_code.lower() != "mis exec":
            self.feedback_label.config(style="ErrorLabel.TLabel")
            self.feedback_label['text'] = 'Please remember to enter the verification code.\n' \
                                          'This is to prevent accidental end of semester updates.\n' \
                                          'The verification code is <<mis exec>> without the << >>.'
        else:
            try:
                MIS_Database_Functions.run_end_of_semester()
                self.feedback_label.config(style="SuccessLabel.TLabel")
                self.feedback_label['text'] = 'End of Semester Transaction was run.\n' \
                                              'Please see the logs for more detailed information.'
            except sqlite3.DatabaseError:
                self.feedback_label.config(style="ErrorLabel.TLabel")
                self.feedback_label['text'] = 'There has been an issue with the database.\n' \
                                              'Please try again or consult the technical director.'
            except IOError:
                self.feedback_label.config(style="ErrorLabel.TLabel")
                self.feedback_label['text'] = 'There has been an IO error.\n' \
                                              'Please try again or consult the technical director.'

    def set_focus(self):
        self.verification_entry.focus()