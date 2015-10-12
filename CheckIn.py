__author__ = 'John'
from tkinter import ttk
from urllib.error import URLError

import tkinter as tk
import MIS_Database_Functions
import Info_IaState_Scraper
import Logger
from Globals import *


class CheckInFrameAlt(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        ##############################################
        #        TITLE AND INSTRUCTIONS              #
        ##############################################
        self.side_frame = ttk.Label(self, border=border_default, relief=relief_default, takefocus=False)
        self.side_frame.grid(row=4, column=0, rowspan=6, columnspan=3, sticky="nsew")

        self.logo_border = ttk.Label(self, border=border_default, relief=relief_default, takefocus=False)
        self.logo_border.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew")

        self.logo_label = ttk.Label(self, image=controller.image, takefocus=False)
        self.logo_label.image = controller.image
        self.logo_label.grid(row=0, column=0, rowspan=4, columnspan=3)

        self.frame_title = ttk.Label(self, text="EVENT CHECK IN", font=Superhead, takefocus=False)
        self.frame_title.grid(row=4, column=0, columnspan=3, rowspan=1)

        self.currency_label = ttk.Label(self, text="", font=Head, takefocus=False)
        self.currency_label.grid(row=5, column=0, columnspan=3, rowspan=2)

        self.instructions_label = ttk.Label(self, text="Basic Steps for Usage:\n\n"
                                                       "1. User enters net id.\n"
                                                       "2. Click get data.\n"
                                                       "3. Verify correctness of data.\n"
                                                       "4. Click submit.\n"
                                                       "5. Repeat until finished.", font=Body, takefocus=False)
        self.instructions_label.grid(row=7, column=0, columnspan=3, rowspan=4, sticky="nw", padx=(10, 10))

        self.content_border_label = ttk.Label(self, border=border_default, relief=relief_default)
        self.content_border_label.grid(row=0, column=3, sticky="nsew", rowspan=7, columnspan=7)
        ########################################
        #   RADIOBUTTONS ENTRIES AND LABELS    #
        ########################################
        self.placeholder = ttk.Label(self, text="STUDENT INFORMATION", font=Head)
        self.placeholder.grid(row=0, column=5, columnspan=3)

        self.net_id_label = ttk.Label(self, text="Net ID:", takefocus=False, font=Subhead)
        self.net_id_label.grid(row=1, column=4, columnspan=2, sticky="ne")
        self.net_id_entry = ttk.Entry(self)
        self.net_id_entry.grid(row=1, column=6, sticky="new", columnspan=3)

        self.name_label = ttk.Label(self, text="Name:", takefocus=False, font=Subhead)
        self.name_label.grid(row=1, column=4, columnspan=2, sticky="se", pady=(0, 5))
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=1, column=6, columnspan=3, sticky="sew", pady=(0, 5))

        self.major_label = ttk.Label(self, text="Major:", takefocus=False, font=Subhead)
        self.major_label.grid(row=2, column=4, columnspan=2, sticky="ne", pady=(5, 0))
        self.major_entry = ttk.Entry(self)
        self.major_entry.grid(row=2, column=6, columnspan=3, sticky="new", pady=(5, 0))

        self.classification_label = ttk.Label(self, text="Classification:", takefocus=False, font=Subhead)
        self.classification_label.grid(row=2, column=4, columnspan=2, sticky="se", pady=(0, 5))
        self.classification_entry = ttk.Entry(self)
        self.classification_entry.grid(row=2, column=6, columnspan=3, sticky="sew", pady=(0, 5))

        self.dues = tk.StringVar()
        self.payment_label = ttk.Label(self, text="PAYMENT INFORMATION", font=Subhead)
        self.payment_label.grid(row=3, column=5, columnspan=3, sticky="s", pady=(0, 10))
        self.trial = ttk.Radiobutton(self, variable=self.dues, value="trial", takefocus=False,
                                     text="Trial: 1 Free Meeting")
        self.trial.grid(row=4, column=5, columnspan=3, sticky="new")
        self.one_semester = ttk.Radiobutton(self, variable=self.dues, value="one", takefocus=False,
                                            text="One Semester: $15")
        self.one_semester.grid(row=4, column=5, columnspan=3, sticky="ew")
        self.two_semesters = ttk.Radiobutton(self, variable=self.dues, value="two", takefocus=False,
                                             text="Two Semesters: $20")
        self.two_semesters.grid(row=4, column=5, columnspan=3, sticky="sew")
        self.trial.invoke()

        self.payment_made = tk.IntVar()
        self.payment_collected_checkbox = ttk.Checkbutton(self, text="Payment Collected", takefocus=False, onvalue=1,
                                                          offvalue=0, variable=self.payment_made)
        self.payment_collected_checkbox.grid(row=4, column=7)
        self.payment_collected_checkbox.invoke()

        ########################################
        #          BUTTONS AND EVENTS          #
        ########################################
        self.get_data_button = ttk.Button(self, text="GET DATA", command=lambda: self.get_data(self.net_id_entry.get()),
                                          style='DataGetter.TButton')
        self.get_data_button.bind("<Return>", lambda e: self.get_data(self.net_id_entry.get()))
        self.get_data_button.grid(row=5, column=4, columnspan=2, sticky="sew")
        self.verify_button = ttk.Button(self, text="VERIFY", command=lambda: self.check_web(),
                                        style='DataGetter.TButton')
        self.verify_button.bind("<Return>", lambda e: self.check_web())
        self.verify_button.grid(row=6, column=4, columnspan=2, sticky="new", pady=(5, 0))
        self.submit_data_button = ttk.Button(self, text="SUBMIT", command=lambda: self.submit_data(),
                                             style='DataSubmitter.TButton')
        self.submit_data_button.bind("<Return>", lambda e: self.submit_data())
        self.submit_data_button.grid(row=5, column=7, columnspan=2, sticky="sew")
        self.clear_all_button = ttk.Button(self, text="CLEAR", command=lambda: self.clear_all(),
                                           style='DataRemover.TButton')
        self.clear_all_button.bind("<Return>", lambda e: self.clear_all())
        self.clear_all_button.grid(row=6, column=7, columnspan=2, sticky="new", pady=(5, 0))

        self.feedback_label_border = ttk.Label(self, border=border_default, relief=relief_default)
        self.feedback_label_border.grid(row=7, column=3, rowspan=3, columnspan=7, sticky="nsew")
        self.feedback_label = ttk.Label(self, text="Welcome to check in.\nWe are very excited to see you again! :)",
                                        font=Subhead)
        self.feedback_label.grid(row=7, column=3, rowspan=3, columnspan=7, pady=(5, 5), padx=(5, 5))

        ## Uncomment these lines to see the under-grid that is set up for all frames###
        # for x in range(10):
        #     for y in range(10):
        #         filler = ttk.Label(self, font=("Helvetica", 10), justify="center",
        #                            text="(%d,%d)" % (x, y), border=1, padding=0, relief="groove")
        #         filler.grid(row=x, column=y, sticky="nsew")

    def set_focus(self):
        # Populate information in the currency labels
        event_id = MIS_Database_Functions.get_most_recent_event_id()
        if event_id is not None:
            data = MIS_Database_Functions.get_event_data(event_id)
            self.currency_label['text'] = "Current Check In:\n%s" % data['company']
        else:
            self.currency_label['text'] = "Not ready to check in yet.\nPlease create an event."
            self.currency_label.config(style='ErrorLabel.TLabel')

        # Set the tab indexes
        tab_order_tuple = (self.net_id_entry, self.get_data_button, self.submit_data_button, self.clear_all_button,
                           self.verify_button)
        for widget in tab_order_tuple:
            widget.lift()
        tab_order_tuple[0].focus()

    def get_data(self, net_id, event=None):
        if net_id is None or net_id.strip() == "":
            self.feedback_label.config(style="ErrorLabel.TLabel")
            self.feedback_label['text'] = "No net ID entered yet."
            return  # Failure state

        if self.major_entry.get() and self.classification_entry.get():
            self.feedback_label.config(style="ErrorLabel.TLabel")
            self.feedback_label['text'] = "Make sure to clear the entries\n" \
                                          "before trying to gather data."
            return  # Failure State

        data = MIS_Database_Functions.check_member(net_id)
        if data is not None:
            self.name_entry.insert(START, data['name'])
            self.major_entry.insert(START, data['major'])
            self.classification_entry.insert(START, data['classification'])
            if data['dues_paid'] == 2:
                self.two_semesters.invoke()
            elif data['dues_paid'] == 1:
                self.one_semester.invoke()
            else:
                self.dues.set("trial")
            attendance_data = \
                MIS_Database_Functions.get_attendance_data(net_id,
                                                           MIS_Database_Functions.get_most_recent_semester_tag())
            if attendance_data is not None:
                if attendance_data['meetings_attended'] > 0 and attendance_data['dues'] < 1:
                    self.feedback_label.config(style="ErrorLabel.TLabel")
                    self.feedback_label['text'] = "Member %s has already used their trial meeting.\n" \
                                                  "They have not yet paid dues.\n" \
                                                  "Collect payment as necessary." % net_id
                else:
                    self.feedback_label.config(style="SuccessLabel.TLabel")
                    self.feedback_label['text'] = "Member %s is paid for %d more semester(s).\n" \
                                                  "They have attended %d meetings this semester." % \
                                                  (net_id, attendance_data['dues'],
                                                   attendance_data['meetings_attended'])
            else:
                self.feedback_label.config(style="SuccessLabel.TLabel")
                self.feedback_label['text'] = "This member has not yet used their trial meeting.\n" \
                                              "They are good to go.\n" \
                                              "Collect payment only if they want to pay now."
        else:
            try:
                data = Info_IaState_Scraper.get_raw_html(net_id)
                data = Info_IaState_Scraper.parse_student_data(data)
                if data is not None:
                    self.name_entry.insert(START, data['name'])
                    self.major_entry.insert(START, data['major'])
                    self.classification_entry.insert(START, data['classification'])
                    self.feedback_label.config(style="SuccessLabel.TLabel")
                    self.feedback_label['text'] = "No current data on %s.\n" \
                                                  "Found data in the directory.\n" \
                                                  "New members receive 1 trial meeting." % net_id
                else:
                    self.feedback_label.config(style="SuccessLabel.TLabel")
                    self.feedback_label['text'] = "No current data on  this net id: %s.\n" \
                                                  "Nothing found on the directory either.  \n" \
                                                  "Make sure their net ID is correct.\n" \
                                                  "If it is then ask them to type in data " \
                                                  "for the other fields.\n" \
                                                  "New members receive 1 trial meeting." % net_id
            except URLError:
                self.feedback_label.config(style="ErrorLabel.TLabel")
                self.feedback_label['text'] = 'No current data on net id: %s.\n' \
                                              'Directory request failed.\n' \
                                              'Check internet connection then try again.\n' \
                                              'If all else fails, enter data manually.' % net_id

    def clear_all(self, event=None):
        self.major_entry.delete(START, len(self.major_entry.get()))
        self.classification_entry.delete(START, len(self.classification_entry.get()))
        self.name_entry.delete(START, len(self.name_entry.get()))
        self.net_id_entry.delete(START, len(self.net_id_entry.get()))
        self.dues.set("trial")
        self.payment_made.set(1)
        try:
            self.feedback_label.config(style="SuccessLabel.TLabel")
            self.feedback_label['text'] = "Awaiting next entry.                    "
        #TODO: Figure out why this was commented out before...
        except Exception:
            pass
        self.set_focus()

    def check_web(self, event=None):
        netid = self.net_id_entry.get()
        self.feedback_label.config(style="ErrorLabel.TLabel")
        self.feedback_label['text'] = 'No net id to verify.'
        if netid.strip() == "":
            return

        try:
            raw = Info_IaState_Scraper.get_raw_html(netid)
            parsed = Info_IaState_Scraper.parse_student_data(raw)
            if parsed is not None:
                self.feedback_label.config(style='SuccessLabel.TLabel')
                self.feedback_label['text'] = 'Verification Results:\n'
                #TODO: Can probably refactor this to make it shorter, use for in loop of the object attributes
                if parsed['name'] != self.name_entry.get():
                    self.name_entry.delete(0, len(self.name_entry.get()))
                    self.name_entry.insert(0, parsed['name'])
                    self.feedback_label['text'] += 'Name updated to: %s\n' % parsed['name']
                if parsed['classification'] != self.classification_entry.get():
                    self.classification_entry.delete(0, len(self.classification_entry.get()))
                    self.classification_entry.insert(0, parsed['classification'])
                    self.feedback_label['text'] += 'Classification updated to: %s\n' % parsed['classification']
                if parsed['major'] != self.major_entry.get():
                    self.major_entry.delete(0, len(self.major_entry.get()))
                    self.major_entry.insert(0, parsed['major'])
                    self.feedback_label['text'] += 'Major updated to: %s' % parsed['major']
            else:
                self.feedback_label.config(style='ErrorLabel.TLabel')
                self.feedback_label['text'] = "No results found for this netid."
        except URLError:
            self.feedback_label.config(style="ErrorLabel.TLabel")
            self.feedback_label['text'] = "Internet connection disrupted.\n" \
                                          "Try again later when connection\n" \
                                          "is improved. :("

    def submit_data(self, event=None):
        major = self.major_entry.get().strip()
        classification = self.classification_entry.get().strip()
        name = self.name_entry.get().strip()
        netid = self.net_id_entry.get().strip()

        for x in (major, classification, name, netid):
            if x == "":
                self.feedback_label.config(style="ErrorLabel.TLabel")
                self.feedback_label['text'] = 'Make sure there is an entry for every field.'
                return
        if self.dues.get() == "two":
            dues = 2
        elif self.dues.get() == "one":
            dues = 1
        else:
            dues = 0
        data = MIS_Database_Functions.check_member(netid)
        if data is not None:
            if data['major'] != major:
                MIS_Database_Functions.set_major(netid, major)
                Logger.write_to_log(Logger.get_event_log_file(), "Major updated to %s for net id %s\n" % (major, netid))
            if data['classification'] != classification:
                MIS_Database_Functions.set_classification(netid, classification)
                Logger.write_to_log(Logger.get_event_log_file(), "Classification updated to '%s' for net id '%s'\n" %
                                    (classification, netid))
            if data['name'] != name:
                MIS_Database_Functions.set_name(netid, name)
                Logger.write_to_log(Logger.get_event_log_file(), "Name updated to %s for net id %s\n" % (name, netid))
            if data['dues_paid'] != dues and dues > 0:
                MIS_Database_Functions.update_payment(netid, dues)
                Logger.write_to_log(Logger.get_event_log_file(), "Payment made for %s, %d semesters paid for\n"
                                    % (netid, dues))
                if self.payment_made.get() == 0:
                    Logger.write_to_log(Logger.get_event_log_file(), "Payment above NOT collected\n")
        else:
            MIS_Database_Functions.create_member(netid, name, major, classification, dues)
            Logger.write_to_log(Logger.get_event_log_file(),
                                'New Member: (%s, %s, %s, %s, %d)\n' % (netid, name, major, classification, dues))
            if dues > 0:
                Logger.write_to_log(Logger.get_event_log_file(), "Payment made for %s semesters for net id %s\n"
                                    % (str(dues), netid))
                if self.payment_made.get() == 0:
                    Logger.write_to_log(Logger.get_event_log_file(), "Payment above NOT collected\n")
        event_id = MIS_Database_Functions.get_most_recent_event_id()

        # Weird edge case: when user accidentally presses trial button, may end up recording a trial meeting for a
        # a user who has already paid for the semester. Code is corrected to make sure the users payment information is
        # not affected, this just makes sure the logs don't falsely record a trial meeting.
        if data is None and dues == 0:
            Logger.write_to_log(Logger.get_event_log_file(), "Trial Meeting for %s\n" % netid)
        elif hasattr(data, 'dues_paid'):
            if data['dues_paid'] == 0:
                Logger.write_to_log(Logger.get_event_log_file(), "Trial Meeting for %s\n" % netid)

        MIS_Database_Functions.create_ticket(event_id, netid)
        Logger.write_to_log(Logger.get_event_log_file(), "\n\n")
        self.clear_all()
        self.feedback_label.config(style="SuccessLabel.TLabel")
        self.feedback_label['text'] = name.split(" ")[1] + " was checked in successfully!\n" \
                                                                            "Welcome them to the meeting!"