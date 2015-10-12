__author__ = 'John'
from tkinter import ttk
import os

import email_functions
import MIS_Database_Functions
from FrameHelpers import open_file_with_default_program
from Globals import *


class ReportGeneratorFrameAlt(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        event_date = MIS_Database_Functions.get_most_recent_event_date()
        if event_date is not None:
            self.filename = str(os.getcwd()) + "\\Reports\\" \
                + event_date + "_Attendance_Report.csv"
        else:
            self.filename = ""

        #####################################################
        #                  SIDE FRAME                       #
        #####################################################
        self.logo_border = ttk.Label(self, border=border_default, relief=relief_default, takefocus=False)
        self.logo_border.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew")

        self.logo_label = ttk.Label(self, image=controller.image, takefocus=False)
        self.logo_label.image = controller.image
        self.logo_label.grid(row=0, column=0, rowspan=4, columnspan=3)

        self.side_frame = ttk.Label(self, border=border_default, relief=relief_default, takefocus=False)
        self.side_frame.grid(row=4, column=0, rowspan=6, columnspan=3, sticky="nsew")

        self.frame_title = ttk.Label(self, text="REPORTS", font=Superhead, takefocus=False)
        self.frame_title.grid(row=4, column=0, columnspan=3, rowspan=1)

        self.file_label = ttk.Label(self, text="Data Administration", font=Head)
        self.file_label.grid(row=5, column=0, columnspan=3, rowspan=2)

        self.instructions = ttk.Label(self, text="Use the buttons to manage reports.\n\n"
                                                 "1) Create the report.\n"
                                                 "2) Review it with Excel.\n"
                                                 "3) Email it")
        self.instructions.grid(row=7, column=0, columnspan=3, rowspan=3, sticky="nw", padx=(10, 10))

        #####################################################
        #                  MAIN CONTENTS                    #
        #####################################################
        self.content_border_label = ttk.Label(self, border=border_default, relief=relief_default, takefocus=False)
        self.content_border_label.grid(row=0, column=3, sticky="nsew", rowspan=7, columnspan=7)

        self.generate_label = ttk.Label(self, text="REPORT GENERATION", font=Head, takefocus=False)
        self.generate_label.grid(row=0, column=5, columnspan=3, sticky="n", pady=(10, 0))
        self.generate_report_button = ttk.Button(self, text="CREATE REPORT",
                                                 command=lambda: self.create_report_and_update_filename(),
                                                 style='DataSubmitter.TButton')
        self.generate_report_button.bind("<Return>", lambda e: self.create_report_and_update_filename())
        self.generate_report_button.grid(row=0, column=5, columnspan=3, sticky="sew")

        self.review_label = ttk.Label(self, text="REVIEW REPORTS", font=Head, takefocus=False)
        self.review_label.grid(row=2, column=5, columnspan=3, sticky="n", pady=(10, 0))
        self.review_button = ttk.Button(self, text="REVIEW", command=lambda: self.review_report(),
                                        style='DataGetter.TButton')
        self.review_button.bind("<Return>", lambda e: self.review_report())
        self.review_button.grid(row=2, column=5, columnspan=3, sticky="sew")

        self.email_label = ttk.Label(self, text="EMAIL REPORTS", font=Head, takefocus=False)
        self.email_label.grid(row=4, column=5, columnspan=3, sticky="n", pady=(10, 0))
        self.email_button = ttk.Button(self, text="EMAIL", command=lambda: self.email_report(),
                                       style="DataSubmitter.TButton")
        self.email_button.bind("<Return>", lambda e: self.email_report())
        self.email_button.grid(row=4, column=5, columnspan=3, sticky="sew")

        self.feedback_label_border = ttk.Label(self, border=border_default, relief=relief_default, takefocus=False)
        self.feedback_label_border.grid(row=7, column=3, rowspan=3, columnspan=7, sticky="nsew")
        self.feedback_label = ttk.Label(self, text="Use the buttons above to\n"
                                                   "generate, open, and email reports.\n"
                                                   "Please note you can also find these\n"
                                                   "CSV files in the Reports directory.",
                                        font=Subhead, takefocus=False)
        self.feedback_label.grid(row=7, column=3, rowspan=3, columnspan=7, pady=(5, 5), padx=(5, 5))

    def create_report_and_update_filename(self, event=None):
        try:
            MIS_Database_Functions.generate_csv_report()
            self.filename = str(os.getcwd()) + "\\Reports\\" \
                + MIS_Database_Functions.get_most_recent_event_date() + "_Attendance_Report.csv"
            self.feedback_label.config(style="SuccessLabel.TLabel")
            self.feedback_label['text'] = "Report File Created Successfully.\nReview for accuracy."
        except PermissionError:
            self.feedback_label.config(style="ErrorLabel.TLabel")
            self.feedback_label['text'] = "There is an issue with file permissions.\n" \
                                          "Make sure the file is not open.\n" \
                                          "If the problem persistsContact the Tech Director."
        except OSError:
            self.feedback_label.config(style="ErrorLabel.TLabel")
            self.feedback_label['text'] = "There was an issue with the operating system call.\n" \
                                          "Try again or contact the Technical Director."
        except TypeError:
            self.feedback_label.config(style="ErrorLabel.TLabel")
            self.feedback_label['text'] = "The file was not created, likely because there was\n" \
                                          "no data to put into the report."

    def review_report(self, event=None):
        try:
            self.feedback_label['text'] = 'Opening report.\nThis may take several seconds.'
            if self.filename:
                open_file_with_default_program(self.filename)
            else:
                self.feedback_label.config(style="ErrorLabel.TLabel")
                self.feedback_label['text'] = "There isn't a file to open yet."
        except FileNotFoundError:
            self.feedback_label['text'] = "The file does not seem to exist.\nMake sure you have generated it.\n" \
                                          "If the problem persists,\ncontact the tech director."
        except PermissionError:
            self.feedback_label['text'] = "There is an issue with file permissions.\n" \
                                          "First make sure the file is not open and try again.\n" \
                                          "If problem persistsContact the Tech Director."
        except OSError:
            self.feedback_label['text'] = "There was an error opening the file.\n" \
                                          "Try again or contact the technical director"

    def email_report(self, event=None):
        try:
            if self.filename:
                email_functions.email_attendance_report(self.filename)
                self.feedback_label.config(style="SuccessLabel.TLabel")
                self.feedback_label['text'] = "Report was emailed to current targets"
            else:
                self.feedback_label.config(style="ErrorLabel.TLabel")
                self.feedback_label['text'] = "There is not yet a file to email."
        except ConnectionError:
            self.feedback_label['text'] = "There was a network error.\n Try again when connection improves."
        except PermissionError:
            self.feedback_label['text'] = "There is an issue with file permissions.\n" \
                                          "First make sure the file is not open and try again.\n" \
                                          "If problem persistsContact the Tech Director."

    def set_focus(self):
        tab_order_tuple = (self.generate_report_button, self.review_button, self.email_button)
        for tab in tab_order_tuple:
            tab.tkraise()
        self.generate_report_button.focus()
        return