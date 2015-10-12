__author__ = 'John'
from tkinter import ttk


class TestFrame(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        for x in range(10):
            for y in range(10):
                filler = ttk.Label(self, font=("Helvetica", 10), justify="center",
                                   text="(%d,%d)" % (x, y), border=1, padding=0, relief="groove")
                filler.grid(row=x, column=y, sticky="nsew")
        self.filler_tester = ttk.Label(self, padding=0,
                                       text="01234567890\n"
                                       "01234567890\n"
                                       "01234567890\n"
                                       "01234567890", font=("Helvetica", 10), border=1, relief="groove")
        self.filler_tester.grid(row=0, column=0, sticky="nsew")