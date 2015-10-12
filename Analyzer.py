__author__ = 'John'
from tkinter import ttk

from Globals import *
import MIS_Database_Functions


class AnalyzeFrameAlt(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.prev_event_data = {'classification': {}}
        self.curr_event_data = {'classification': {}}
        self.target_major = ""

        ###########################################################
        #                 SIDE FRAME                              #
        ###########################################################
        self.logo_border = ttk.Label(self, border=border_default, relief=relief_default, takefocus=False)
        self.logo_border.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew")

        self.logo_label = ttk.Label(self, image=controller.image, takefocus=False)
        self.logo_label.image = controller.image
        self.logo_label.grid(row=0, column=0, rowspan=4, columnspan=3)

        self.side_frame = ttk.Label(self, border=border_default, relief=relief_default, takefocus=False)
        self.side_frame.grid(row=4, column=0, rowspan=6, columnspan=3, sticky="nsew")

        self.frame_title = ttk.Label(self, text="DATA ANALYSIS", font=Superhead, takefocus=False)
        self.frame_title.grid(row=4, column=0, columnspan=3, rowspan=1)

        self.file_label = ttk.Label(self, text="Attendance Statistics\n"
                                               "and Trends", font=Head)
        self.file_label.grid(row=5, column=0, columnspan=3, rowspan=2)

        self.instructions = ttk.Label(self, text="This page can be used to view\n"
                                                 "aggregate data from the last \n"
                                                 "two events.\n\n"
                                                 "NOTE: There must be at least \n"
                                                 "two events in the database for\n"
                                                 "this frame to work properly.")
        self.instructions.grid(row=7, column=0, columnspan=3, rowspan=3, sticky="nw", padx=(10, 10))

        self.content_border_label = ttk.Label(self, border=border_default, relief=relief_default)
        self.content_border_label.grid(row=0, column=3, sticky="nsew", rowspan=7, columnspan=7)
        ####################################################################
        #                       MAIN CONTENTS                              #
        ####################################################################
        self.present_button = ttk.Button(self, text="DISPLAY DATA", command=lambda: self.present_data(), style="DataGetter.TButton")
        self.present_button.bind("<Return>", lambda e: self.present_data())
        self.present_button.grid(row=0, column=5, columnspan=3, sticky="ew")

        self.curr_name_label = ttk.Label(self, text="", border=.5, relief="groove", font=Head)
        self.curr_name_label.grid(row=1, column=3, sticky="nsew", columnspan=3, rowspan=1, padx=(5, 0))

        self.prev_name_label = ttk.Label(self, text="", border=.5, relief="groove", font=Head)
        self.prev_name_label.grid(row=1, column=7, sticky="nsew", columnspan=3, rowspan=1, padx=(0, 5))

        self.curr_classification_label = ttk.Label(self, text="", border=.5, relief="groove", font=Body)
        self.curr_classification_label.grid(row=2, column=3, sticky="nsew", columnspan=2, padx=(5, 0), rowspan=2)

        self.prev_classification_label = ttk.Label(self, text="", border=.5, relief="groove", font=Body)
        self.prev_classification_label.grid(row=2, column=7, sticky="nsew", columnspan=2, rowspan=2)

        self.curr_date_count_holder = ttk.Label(self, text="", border=.5, relief="groove", font=Body)
        self.curr_date_count_holder.grid(row=2, column=5, sticky="nsew", rowspan=2)

        self.prev_date_count_holder = ttk.Label(self, text="", border=.5, relief="groove", font=Body)
        self.prev_date_count_holder.grid(row=2, column=9, sticky="nsew", rowspan=2, padx=(0, 5))

        self.feedback_label_border = ttk.Label(self, border=border_default, relief=relief_default)
        self.feedback_label_border.grid(row=7, column=3, rowspan=3, columnspan=7, sticky="nsew")
        self.feedback_label = ttk.Label(self, text="Awaiting button click.",
                                        font=Subhead)
        self.feedback_label.grid(row=7, column=3, rowspan=3, columnspan=7, pady=(5, 5), padx=(5, 5))

    def gather_data(self):
        #TODO: Alias MIS_Database_Functions, these lines are way to long
        prev_event_aggregates = MIS_Database_Functions.get_event_aggregates(
            MIS_Database_Functions.get_most_recent_event_id())  # Event that just happened
        curr_event_aggregates = MIS_Database_Functions.get_event_aggregates(
            MIS_Database_Functions.get_most_recent_event_id()-1)  # Event before that
        prev_event_classifications = MIS_Database_Functions.get_event_classification_aggregates(
            MIS_Database_Functions.get_most_recent_event_id())
        curr_event_classifications = MIS_Database_Functions.get_event_classification_aggregates(
            MIS_Database_Functions.get_most_recent_event_id()-1)
        self.target_major = MIS_Database_Functions.select_config_info('target_major')
        for aggregate in prev_event_aggregates:
            self.prev_event_data[aggregate] = prev_event_aggregates[aggregate]
        for aggregate in curr_event_aggregates:
            self.curr_event_data[aggregate] = curr_event_aggregates[aggregate]
        for classification in prev_event_classifications:
            self.prev_event_data['classification'][classification] = prev_event_classifications[classification]
        for classification in curr_event_classifications:
            self.curr_event_data['classification'][classification] = curr_event_classifications[classification]
        return True

    def present_data(self, event=None):
        if self.gather_data():
            self.prev_name_label['text'] = self.prev_event_data['company']
            self.curr_name_label['text'] = self.curr_event_data['company']

            #TODO: Refactor this it's ugly...
            self.prev_classification_label['text'] = ""
            for classification in self.prev_event_data['classification']:
                if classification not in ["Sophomore", "Freshman", "Non-Degree"]:  # These words mess up the indents
                    self.prev_classification_label['text'] += classification+"\t\t"
                else:
                    self.prev_classification_label['text'] += classification+"\t"
                self.prev_classification_label['text'] += str(self.prev_event_data['classification'][classification]) + "\n"

            self.curr_classification_label['text'] = ""
            for classification in self.curr_event_data['classification']:
                if classification not in ["Sophomore", "Freshman", "Non-Degree"]:  # These words mess up the indents
                    self.curr_classification_label['text'] += classification+"\t\t"
                else:
                    self.curr_classification_label['text'] += classification+"\t"
                self.curr_classification_label['text'] += str(self.curr_event_data['classification'][classification]) + "\n"

            self.prev_date_count_holder['text'] = ""
            self.prev_date_count_holder['text'] += "Total: " + "\n"
            self.prev_date_count_holder['text'] += str(self.prev_event_data['count'])

            self.curr_date_count_holder['text'] = ""
            self.curr_date_count_holder['text'] += "Total: " + "\n"
            self.curr_date_count_holder['text'] += str(self.curr_event_data['count'])

            self.feedback_label.config(style='SuccessLabel.TLabel')
            self.feedback_label['text'] = "Aggregates are displayed above.\n" \
                                          "Use SQLite Manger to get more  \n" \
                                          "detail about the event data."
        else:
            self.feedback_label.config(style="ErrorLabel.TLabel")
            self.feedback_label['text'] = "Data is not ready to be\n" \
                                          "presented right now."

    def set_focus(self):
        self.present_button.focus()

