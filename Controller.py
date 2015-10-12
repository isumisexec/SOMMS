__author__ = 'John'
# Imports used for the creation of the GUI
import tkinter as tk
from tkinter import ttk, PhotoImage

# Import MIS Club specific frame classes into scope
from CheckIn import CheckInFrameAlt
from CreateEvent import CreateEventFrameAlt
from StartPage import StartPageAlt
from Reporter import ReportGeneratorFrameAlt
from Analyzer import AnalyzeFrameAlt
from EmailManager import EmailManagerFrameAlt
from EndOfSemester import EndOfSemesterAlt
from SemesterCreator import SemesterCreatorAlt
import MIS_Database_Functions

# Import global styles and helper functions
from Globals import *
from FrameHelpers import *


class CheckInSystem(tk.Tk):
    """
        Class derived from Tk. Designed in an OO fashion to incorporate custom frames.
        Each custom frame is included in the tuple beneath the self.frames dictionary
        and is expected to provide a method called <<set_focus>>. While the intended purpose
        of this method is to set the cursor focus, Python does support the declaration
        of interfaces, so any implementation will do (even one that is simply to return
        immediately after being called).
    """
    def __init__(self):
        tk.Tk.__init__(self)
        #tk.Tk.iconbitmap(self, default="Images/mis_logo.ico") ==> this was making Linux cry,
        #                                                          if you can get it to work go ahead
        tk.Tk.wm_title(self, "Club Check In")

        image_location = MIS_Database_Functions.select_config_info('logo_location')
        self.image = PhotoImage(file=image_location)

        # This container will contain all the other frames.
        container = ttk.Frame(self)
        container.pack(expand=True, fill="both")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.container = container

        # Menu bar => contains the drop down menus
        menu_bar = tk.Menu(container, font=Body)
        # Other menu variables are the actual content of the drop down menus
        # Check in menu contains the systems primary functions (i.e. event creation and checking in members)
        check_in_menu = tk.Menu(menu_bar, tearoff=0, font=Body)
        check_in_menu.add_command(label="Home", command=lambda: self.show_frame(StartPageAlt))
        check_in_menu.add_separator()
        check_in_menu.add_command(label="Check In Members", command=lambda: self.show_frame(CheckInFrameAlt))
        check_in_menu.add_separator()
        check_in_menu.add_command(label="Create An Event", command=lambda: self.show_frame(CreateEventFrameAlt))
        check_in_menu.add_separator()
        check_in_menu.add_command(label="Quit", command=quit)
        check_in_menu.add_separator()
        menu_bar.add_cascade(menu=check_in_menu, label="Main")

        # Data menu contains functions for viewing data and sending it to those who need it.
        data_menu = tk.Menu(menu_bar, tearoff=0, font=Body)
        data_menu.add_command(label="Generate Report", command=lambda: self.show_frame(ReportGeneratorFrameAlt))
        data_menu.add_separator()
        data_menu.add_command(label="Analysis", command=lambda: self.show_frame(AnalyzeFrameAlt))
        menu_bar.add_cascade(menu=data_menu, label="Data")

        # Admin menu contains information
        admin_menu = tk.Menu(menu_bar, tearoff=0, font=Body)
        admin_menu.add_command(label="Manage Email Recipients", command=lambda: self.show_frame(EmailManagerFrameAlt))
        admin_menu.add_separator()
        admin_menu.add_command(label="New Semester", command=lambda: self.show_frame(SemesterCreatorAlt))
        admin_menu.add_separator()
        admin_menu.add_command(label="End of Semester", command=lambda: self.show_frame(EndOfSemesterAlt))
        menu_bar.add_cascade(menu=admin_menu, label="Admin")
        tk.Tk.config(self, menu=menu_bar)

        # Universal Style to be used by SOMMS
        data_getter_style = ttk.Style()
        data_getter_style.configure('DataGetter.TButton', foreground='#006600')
        data_remover_style = ttk.Style()
        data_remover_style.configure('DataRemover.TButton', foreground='#CC0000')
        data_submitter_style = ttk.Style()
        data_submitter_style.configure('DataSubmitter.TButton', foreground='#000066')

        error_label = ttk.Style()
        error_label.configure('ErrorLabel.TLabel', foreground='#CC0000')
        success_label = ttk.Style()
        success_label.configure('SuccessLabel.TLabel', foreground='#000066')

        # Set the size of the primary window
        self.geometry(newGeometry="800x600")

        # This dictionary will hold all the frames for the GUI, call show_frame with the name of the class
        # to bring them to the front of the primary window
        self.frames = {}
        # If new frames need to be added remember to add them to the END of the tuple to protect the key bindings.
        self.frame_set = (StartPageAlt, CheckInFrameAlt, CreateEventFrameAlt,
                          ReportGeneratorFrameAlt,
                          AnalyzeFrameAlt, EmailManagerFrameAlt, SemesterCreatorAlt, EndOfSemesterAlt)
        for f in self.frame_set:
            frame = f(container, self)
            for x in range(10):
                frame.rowconfigure(x, minsize=600/10)
                frame.columnconfigure(x, minsize=800/10)
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        for f in self.container.children:
            bind_keys(self, self.container.children[f])
        self.show_frame(StartPageAlt)

    def show_frame(self, frame_to_show, event=None):
        frame = self.frames[frame_to_show]
        try:
            frame.set_focus()
        except AttributeError:
            print("set_focus not implemented...")
        frame.tkraise()
        return "break"
        # return ensures that user's key entry isn't actually written (e.g. no ~ appears when returning to home)

    def burn_it_down(self):
        self.quit()
