from Tkinter import Frame, Label

class AboutFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        Label(self, text='Created by Michael Mordowanec').pack(padx=30, pady=30)
        Label(self, text='(c) 2013').pack(padx=30, pady=30)
        
