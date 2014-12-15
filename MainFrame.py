from Tkinter import *

class MainFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        
        self.parent = parent
        self.display = Frame(self, bd=5, relief=SUNKEN)
        Canvas(self.display, bg='red', width=200, height=500).grid(column=0, row=0)
        Canvas(self.display, bg='white', width=200, height=500).grid(column=1, row=0)
        Canvas(self.display, bg='green', width=200, height=500).grid(column=2, row=0)
        self.display.grid(column=0, row=0)
        
        self.corpus = StringVar()
        self.corpus.set('Romagnol')
        Label(self, text='Choose a corpus:').grid(column=0, row=1)
        self.corpusMenu = apply(OptionMenu, (self, self.corpus) + tuple(x for x in self.parent.corpusDict))
        self.corpusMenu.grid(column=1, row=1)
        self.corpus.trace('w', self.getCorpus)

    def getCorpus(self, *args):
        title = self.corpus.get()
        self.parent.currentCorpus = self.parent.corpusDict[title]
        self.parent.update()

