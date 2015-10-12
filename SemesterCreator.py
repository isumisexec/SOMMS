__author__ = 'John'

from tkinter import ttk
from Globals import *
import MIS_Database_Functions


class SemesterCreatorAlt(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        ##############################################################
        #                      SIDE FRAME                            #
        ##############################################################
        self.logo_border = ttk.Label(self, border=border_default, relief=relief_default, takefocus=False)
        self.logo_border.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew")

        self.logo_label = ttk.Label(self, image=controller.image, takefocus=False)
        self.logo_label.image = controller.image
        self.logo_label.grid(row=0, column=0, rowspan=4, columnspan=3)

        self.side_frame = ttk.Label(self, border=border_default, relief=relief_default, takefocus=False)
        self.side_frame.grid(row=4, column=0, rowspan=6, columnspan=3, sticky="nsew")

        self.frame_title = ttk.Label(self, text="SEMESTER CREATION", font=Superhead, takefocus=False)
        self.frame_title.grid(row=4, column=0, columnspan=3, rowspan=1)

        current_sem_tag = MIS_Database_Functions.get_most_recent_semester_tag()
        if current_sem_tag is not None:
            self.currency_label = ttk.Label(self, text="Current Semester: %s" % current_sem_tag, font=Head)
        else:
            self.currency_label = ttk.Label(self, text="No Semester Created!\n"
                                                       "Create one then restart\n"
                                                       "this system.", font=Head)
            self.currency_label.config(style="ErrorLabel.TLabel")
        self.currency_label.grid(row=5, column=0, columnspan=3, rowspan=2)

        self.instructions = ttk.Label(self, text="At the beginning of each semester\n"
                                                 "come here and create a new entry \n"
                                                 "for the database. This is needed \n"
                                                 "for data verification, and makes \n"
                                                 "aggregating much easier.")
        self.instructions.grid(row=7, column=0, columnspan=3, rowspan=3, sticky="nw", padx=(10, 10))

        self.content_border_label = ttk.Label(self, border=border_default, relief=relief_default)
        self.content_border_label.grid(row=0, column=3, sticky="nsew", rowspan=7, columnspan=7)
        #############################################################
        #                     MAIN CONTENTS                         #
        #############################################################
        self.big_label = ttk.Label(self, text="NEW SEMESTER DATES", font=Head)
        self.big_label.grid(row=0, column=5, columnspan=3)

        self.semester_start_label = ttk.Label(self, text="Semester Start:", font=Subhead)
        self.semester_start_label.grid(row=1, column=3, columnspan=2, sticky="n")
        self.semester_start_entry = ttk.Entry(self)
        self.semester_start_entry.grid(row=1, column=5, sticky="new", columnspan=2)

        self.semester_end_label = ttk.Label(self, text="End of Semester:", font=Subhead)
        self.semester_end_label.grid(row=1, column=3, columnspan=2, sticky="s")
        self.semester_end_entry = ttk.Entry(self)
        self.semester_end_entry.grid(row=1, column=5, sticky="sew", columnspan=2)

        self.feedback_label_border = ttk.Label(self, border=border_default, relief=relief_default)
        self.feedback_label_border.grid(row=7, column=3, rowspan=3, columnspan=7, sticky="nsew")
        self.feedback_label = ttk.Label(self, text="Awaiting new semester entry.",
                                        font=Subhead)
        self.feedback_label.grid(row=7, column=3, rowspan=3, columnspan=7, pady=(5, 5), padx=(5, 5))
        self.semester_submitter_button = ttk.Button(self, text="Submit Semester",
                                                    command=lambda: self.create_semester(),
                                                    style="DataSubmitter.TButton")
        self.semester_submitter_button.bind("<Return>", lambda e: self.create_semester())
        self.semester_submitter_button.grid(row=3, column=5, sticky="ew", columnspan=2)

        # This code only matters for systems whose databases do not have any semesters in them
        if current_sem_tag is None:
            self.semester_tag_label = ttk.Label(self, text="Semester Tag:", font=Subhead)
            self.semester_tag_label.grid(row=2, column=3, sticky="n", columnspan=2, pady=(10, 0))

            self.semester_tag_entry = ttk.Entry(self)
            self.semester_tag_entry.grid(row=2, column=5, sticky="new", columnspan=2, pady=(10, 0))
            self.feedback_label['text'] = 'Only for this semester you will need\n' \
                                          'to provide a semester tag in the format\n' \
                                          'F## where F is either F or S (fall or\n ' \
                                          'spring), and ## is the year. In the \n' \
                                          'future this will be automatic.'
            self.semester_submitter_button.bind("<Return>", lambda e: self.create_semester(
                semester_tag=self.semester_tag_entry.get()))
            self.semester_submitter_button.config(command=lambda: self.create_semester(
                semester_tag=self.semester_tag_entry.get()))

    def set_focus(self):
        if not hasattr(self, 'semester_tag_entry'):
            tab_order_tuple = (self.semester_start_entry, self.semester_end_entry, self.semester_submitter_button)
            for tab in tab_order_tuple:
                tab.tkraise()
        else:
            tab_order_tuple = (self.semester_start_entry, self.semester_end_entry,
                               self.semester_tag_entry, self.semester_submitter_button)
            for tab in tab_order_tuple:
                tab.tkraise()
        self.semester_start_entry.focus()
        return

    def create_semester(self, event=None, semester_tag=None):
        start = self.semester_start_entry.get().strip()
        end = self.semester_end_entry.get().strip()
        if len(start) != 11 or len(end) != 11 or start[2] != '/' or end[2] != '/':
            self.feedback_label.config(style='ErrorLabel.TLabel')
            self.feedback_label['text'] = "Please enter dates in the format:\n" \
                                          "DD/MMM/YYYY.\n" \
                                          "Example: 12/AUG/2015"
            return  # Failure state

        # Normal Semester Creation with automated Semester Tag generation
        if not hasattr(self, 'semester_tag_entry'):
            start_month = start[3:6]
            end_month = end[3:6]
            previous_semester_tag = MIS_Database_Functions.get_most_recent_semester_tag()
            try:
                previous_semester_tag_year = int(previous_semester_tag[1:])
            except ValueError:
                self.feedback_label.config(style='ErrorLabel.TLabel')
                self.feedback_label['text'] = "The previous semester's tag is incorrect.\n" \
                                              "Have the technical director correct this issue before proceeding."
                return
            if previous_semester_tag[0] == 'F':
                new_semester_tag_year = previous_semester_tag_year + 1
                new_semester_tag = 'S'
            else:
                new_semester_tag = 'F'
                new_semester_tag_year = previous_semester_tag_year
            new_semester_tag += str(new_semester_tag_year)
            # Checks to make sure the start and end dates are in the right months for the new Semester
            if start_month not in months or end_month not in months:
                self.feedback_label.config(style='ErrorLabel.TLabel')
                self.feedback_label['text'] = "The month in at least one of the dates\n" \
                                              "is not correct for semester  %s." % new_semester_tag
            if new_semester_tag[0] == 'F' and (start_month not in fall_months or end_month not in fall_months):
                self.feedback_label.config(style='ErrorLabel.TLabel')
                self.feedback_label['text'] = "The month in at least one of the dates\n" \
                                              "is not correct for semester  %s." % new_semester_tag
                return
            if new_semester_tag[0] == 'S' and (start_month not in spring_months or end_month not in spring_months):
                self.feedback_label.config(style='ErrorLabel.TLabel')
                self.feedback_label['text'] = "The month in at least one of the dates\n" \
                                              "is not correct for semester  %s." % new_semester_tag
                return
            start_year = int(start[9:])
            end_year = int(end[9:])
            if start_year != new_semester_tag_year or end_year != new_semester_tag_year:
                self.feedback_label.config(style='ErrorLabel.TLabel')
                self.feedback_label['text'] = 'Incorrect year. It should be \'%s' \
                                              % str(new_semester_tag_year)
                return
            self.feedback_label.config(style="SuccessLabel.TLabel")
            self.feedback_label['text'] = "Semester created successfully.\n" \
                                          " You are ready to create events and check in members."
            MIS_Database_Functions.create_semester(new_semester_tag, start, end)
            self.semester_end_entry.delete(0, len(self.semester_end_entry.get()))
            self.semester_start_entry.delete(0, len(self.semester_start_entry.get()))

        # Semester Creation from the blank slate
        else:
            MIS_Database_Functions.create_semester(semester_tag, start, end)
            self.feedback_label.config(style="SuccessLabel.TLabel")
            self.feedback_label['text'] = "Semester created successfully.\n" \
                                          "You are ready to create events."