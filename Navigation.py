from Tkinter import Frame, Button

class Navigation(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        Button(self, text='Home', width=15, command=self.parent.home).grid(padx=5, row=0, column=0)
        Button(self, text='Play around', width=15, command=self.parent.play).grid(padx=5, row=0, column=1)
        Button(self, text='Add to corpus', width=15, command=self.parent.add).grid(padx=5, row=0, column=2)
        Button(self, text='Annotate', width=15, command=self.parent.annotate).grid(padx=5, row=0, column=3)
        Button(self, text='About', width=15, command=self.parent.about).grid(padx=5, row=0, column=4)
        Button(self, text='Save', width=15, command=self.parent.save).grid(padx=5, row=0, column=5)
        Button(self, text='Minimal Pairs', width=15, command=self.parent.mp).grid(padx=5, row=0, column=6)
        self.pack()
