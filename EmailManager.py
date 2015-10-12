__author__ = 'John'
from Globals import *
from tkinter import ttk
import email_functions


class EmailManagerFrameAlt(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
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

        self.frame_title = ttk.Label(self, text="EMAIL MANAGEMENT", font=Superhead, takefocus=False)
        self.frame_title.grid(row=4, column=0, columnspan=3, rowspan=1)

        self.file_label = ttk.Label(self, text="Email Target\n"
                                               "Management", font=Head)
        self.file_label.grid(row=5, column=0, columnspan=3, rowspan=2)

        self.instructions = ttk.Label(self, text="You can use this page to\n"
                                                 "manage email targets.   \n"
                                                 "You can also manually   \n"
                                                 "update the file in the  \n"
                                                 "admin directory.")
        self.instructions.grid(row=7, column=0, columnspan=3, rowspan=3, sticky="nw", padx=(10, 10))

        self.content_border_label = ttk.Label(self, border=border_default, relief=relief_default)
        self.content_border_label.grid(row=0, column=3, sticky="nsew", rowspan=7, columnspan=7)

        ##################################################################
        #                        MAIN CONTENT                            #
        ##################################################################
        self.new_email_label = ttk.Label(self, text="ADD EMAIL TARGETS", font=Head)
        self.new_email_label.grid(row=0, column=5, columnspan=3)
        self.new_email_entry = ttk.Entry(self)
        self.new_email_entry.grid(row=1, column=4, columnspan=2, sticky="ew")
        self.new_email_button = ttk.Button(self, command=lambda: self.add_email(), text="Add to targets",
                                           style="DataSubmitter.TButton")
        self.new_email_button.bind("<Return>", lambda e: self.add_email())
        self.new_email_button.grid(row=1, column=6, sticky="ew", columnspan=2, padx=(5, 0))

        self.delete_email_label = ttk.Label(self, text="DELETE EMAIL TARGETS", font=Head)
        self.delete_email_label.grid(row=3, column=5, columnspan=3)
        self.delete_email_entry = ttk.Entry(self)
        self.delete_email_entry.grid(row=4, column=4, columnspan=2, sticky="ew")
        self.delete_email_button = ttk.Button(self, text="Remove from targets", command=lambda: self.remove_email(),
                                              style="DataRemover.TButton")
        self.delete_email_button.bind("<Return>", lambda e: self.remove_email())
        self.delete_email_button.grid(row=4, column=6, columnspan=2, sticky="ew", padx=(5,0))

        self.feedback_label_border = ttk.Label(self, border=border_default, relief=relief_default)
        self.feedback_label_border.grid(row=7, column=3, rowspan=3, columnspan=7, sticky="nsew")
        targets = email_functions.get_email_recipients()
        self.feedback_label = ttk.Label(self, text="Current Targets:",
                                        font=Subhead)
        for target in targets:
            self.feedback_label['text'] += "\n"+target
        self.feedback_label.grid(row=7, column=3, rowspan=3, columnspan=7, pady=(5, 5), padx=(5, 5))

    def update_feedback_label(self):
        self.feedback_label['text'] = "UPDATE REGISTERED\nCurrent Targets:"
        targets = email_functions.get_email_recipients()
        for target in targets:
            self.feedback_label['text'] += "\n"+target

    def set_focus(self):
        tab_order_tuple = (self.new_email_entry, self.new_email_button,
                           self.delete_email_entry, self.delete_email_button)
        for tab in tab_order_tuple:
            tab.tkraise()
        self.new_email_entry.focus()
        return

    def add_email(self, event=None):
        new_email = self.new_email_entry.get().strip()
        if new_email:
            try:
                email_functions.add_email_recipients(new_email)
                self.feedback_label.config(style="SuccessLabel.TLabel")
                self.new_email_entry.delete(0, len(self.new_email_entry.get()))
                self.update_feedback_label()
            except AttributeError as e:
                self.feedback_label.config(style='ErrorLabel.TLabel')
                self.feedback_label['text'] = str(e)
        else:
            self.feedback_label.config(style="ErrorLabel.TLabel")
            self.feedback_label['text'] = "Nothing to add"
        return

    def remove_email(self, event=None):
        email_to_remove = self.delete_email_entry.get().strip()
        if email_to_remove:
            email_functions.delete_email_recipients(email_to_remove)
            self.delete_email_entry.delete(0, len(self.delete_email_entry.get()))
            self.update_feedback_label()
        else:
            self.feedback_label.config(style="ErrorLabel.TLabel")
            self.feedback_label['text'] = "Nothing to remove"
        return