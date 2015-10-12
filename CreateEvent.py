__author__ = 'John'
from tkinter import ttk
import MIS_Database_Functions
from Globals import *


class CreateEventFrameAlt(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        # for x in range(10):
        #     for y in range(10):
        #         filler = ttk.Label(self, font=("Helvetica", 10), justify="center",
        #                            text="(%d,%d)" % (x, y), border=1, padding=0, relief="groove")
        #         filler.grid(row=x, column=y, sticky="nsew")

        #####################################################
        #                  SIDE FRAME                       #
        #####################################################
        self.side_frame = ttk.Label(self, border=border_default, relief=relief_default, takefocus=False)
        self.side_frame.grid(row=4, column=0, rowspan=6, columnspan=3, sticky="nsew")

        self.logo_border = ttk.Label(self, border=border_default, relief=relief_default, takefocus=False)
        self.logo_border.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew")

        self.logo_label = ttk.Label(self, image=controller.image, takefocus=False)
        self.logo_label.image = controller.image
        self.logo_label.grid(row=0, column=0, rowspan=4, columnspan=3)

        self.frame_title = ttk.Label(self, text="EVENT CREATION", font=Superhead, takefocus=False)
        self.frame_title.grid(row=4, column=0, columnspan=3, rowspan=1)
        self.current_label = ttk.Label(self, text="", takefocus=False, font=Head)
        self.current_label.grid(row=5, column=0, columnspan=3, rowspan=2)

        self.instructions_label = ttk.Label(self, text="Use this frame to store\ndetails about your events.\n\n"
                                                       "1. Enter the Company Name\n"
                                                       "2. Enter the topic for the Event\n"
                                                       "3. Enter the date for the event\n"
                                                       "   in this format: DD/MMM/YYYY.\n"
                                                       "4. Click the submit button.", font=Body, takefocus=False)
        self.instructions_label.grid(row=7, column=0, columnspan=3, rowspan=4, sticky="nw", padx=(10, 10))

        self.content_border_label = ttk.Label(self, border=border_default, relief=relief_default)
        self.content_border_label.grid(row=0, column=3, sticky="nsew", rowspan=7, columnspan=7)
        #####################################################
        #                  MAIN CONTENTS                    #
        #####################################################
        start = 0
        self.placeholder = ttk.Label(self, text="EVENT INFORMATION", font=Head, takefocus=False)
        self.placeholder.grid(row=start, column=5, columnspan=3)

        self.company_name_label = ttk.Label(self, font=Subhead, text="Company Name: ", takefocus=False)
        self.company_name_label.grid(row=start+1, column=4, columnspan=2, sticky="ne")
        self.company_name_entry = ttk.Entry(self)
        self.company_name_entry.grid(row=start+1, column=6, columnspan=2, sticky="new")

        self.event_topic_label = ttk.Label(self, font=Subhead, text="Event Topic: ", takefocus=False)
        self.event_topic_label.grid(row=start+1, column=4, columnspan=2, sticky="se")
        self.event_topic_entry = ttk.Entry(self)
        self.event_topic_entry.grid(row=start+1, column=6, columnspan=2, sticky="sew")

        self.event_date_label = ttk.Label(self, font=Subhead, text="Date of Event: ", takefocus=False)
        self.event_date_label.grid(row=start+2, column=4, columnspan=2, sticky="e")
        self.event_date_entry = ttk.Entry(self)
        self.event_date_entry.grid(row=start+2, column=6, columnspan=2, sticky="ew")

        self.submit_button = ttk.Button(self, text="SUBMIT EVENT", command=lambda: self.create_event(), style='DataSubmitter.TButton')
        self.submit_button.bind("<Return>", lambda e: self.create_event())
        self.submit_button.grid(row=start+4, column=6, columnspan=2, sticky="new")

        self.clear_all_button = ttk.Button(self, text="CLEAR ALL", command=lambda: self.clear_all(),
                                           style="DataRemover.TButton")
        self.clear_all_button.bind("<Return>", lambda e: self.clear_all())
        self.clear_all_button.grid(row=start+4, column=6, columnspan=2, sticky="sew")

        self.feedback_label_border = ttk.Label(self, border=border_default, relief=relief_default)
        self.feedback_label_border.grid(row=7, column=3, rowspan=3, columnspan=7, sticky="nsew")
        self.feedback_label = ttk.Label(self, text="Welcome to Event Creation.\nFollow the instructions on the left.",
                                        font=Subhead)
        self.feedback_label.grid(row=7, column=3, rowspan=3, columnspan=7, pady=(5, 5), padx=(5, 5))
        self.populate_event_label()

    def set_focus(self):
        tab_order_tuple = (self.company_name_entry, self.event_topic_entry, self.event_date_entry,
                           self.submit_button, self.clear_all_button)
        for widget in tab_order_tuple:
            widget.lift()
        tab_order_tuple[0].focus()

    def clear_all(self, event=None):
        self.company_name_entry.delete(0, len(self.company_name_entry.get()))
        self.event_date_entry.delete(0, len(self.event_date_entry.get()))
        self.event_topic_entry.delete(0, len(self.event_topic_entry.get()))
        self.feedback_label.config(style="SuccessLabel.TLabel")
        self.feedback_label['text'] = "Entries Cleared."

    def create_event(self, event=None):
        event_date = self.event_date_entry.get().strip()
        company_name = self.company_name_entry.get().strip()
        event_topic = self.event_topic_entry.get().strip()

        if event_date == '' or company_name == '' or event_topic == '':
            self.feedback_label.config(style="ErrorLabel.TLabel")
            self.feedback_label['text'] = "Please provide at least some\nvalue for each field."
            return
        if len(event_date) != 11 or event_date[2] != '/' or event_date[6] != '/':
            self.feedback_label.config(style="ErrorLabel.TLabel")
            self.feedback_label['text'] = "Provide dates in format DD/MMM/YYYY\nExample: 12/AUG/2015"
            return
        semester_tag = MIS_Database_Functions.get_most_recent_semester_tag()
        month = event_date[3:6]
        if semester_tag[0] == 'F' and month not in fall_months:
            self.feedback_label.config(style="ErrorLabel.TLabel")
            self.feedback_label['text'] = "Check date.\nMonth is incorrect for current semester." \
                                          "\nYou may have forgotten to create a new semester."
            return
        elif semester_tag[0] == 'S' and month not in spring_months:
            self.feedback_label.config(style="ErrorLabel.TLabel")
            self.feedback_label['text'] = "Check date.\nMonth is incorrect for current semester." \
                                          "\nYou may have forgotten to create a new semester."
            return
        results = MIS_Database_Functions.create_event(company_name, event_topic, event_date)
        if results[0]:  # Success state
            self.feedback_label.config(style="SuccessLabel.TLabel")
            self.feedback_label['text'] = "The new event was added.\n Event ID: %s\n" \
                                          "Restart the system before checking in." % str(results[1])
        else:  # Failure state
            self.feedback_label.config(style="ErrorLabel.TLabel")
            self.feedback_label['text'] = "An error occurred:\n" + str(results[1])
        self.company_name_entry.delete(START, len(company_name))
        self.event_date_entry.delete(START, len(event_date))
        self.event_topic_entry.delete(START, len(event_topic))
        self.populate_event_label()
        self.set_focus()

    def populate_event_label(self):
        semester_tag = MIS_Database_Functions.get_most_recent_semester_tag()
        if semester_tag is None:  # Failure State
            self.current_label.config(style="ErrorLabel.TLabel")
            self.current_label['text'] = 'No semester created yet!\n' \
                                         'Create one first, then\n' \
                                         'restart this system. :)'
            return

        event_id = MIS_Database_Functions.get_most_recent_event_id()
        if event_id is not None:
            event_data = MIS_Database_Functions.get_event_data(event_id)
            self.current_label['text'] = 'Newest Event:\n%s' % (event_data['company'])
        else:
            self.feedback_label.config(style="ErrorLabel.TLabel")
            self.current_label['text'] = 'No event yet.\nCreate one here.'