from Tkinter import *
from Corpus import *
import pickle, re
from Navigation import Navigation
from AboutFrame import AboutFrame
from AddFrame import AddFrame
from AnnotationFrame import AnnotationFrame
from MainFrame import MainFrame
from MinimalPairsFrame import MinimalPairsFrame
from PlayFrame import PlayFrame




class CorpusGUI(Tk):
    def __init__(self, pickleFile='corpus.p'):
        Tk.__init__(self)
        
        Navigation(self)
        self.pickleFile = pickleFile
        self.corpusDict = pickle.load(open(self.pickleFile, 'rb'))
        self.currentCorpus = self.corpusDict['Romagnol']
        self.homeFrame = MainFrame(self)
        self.currentFrame = self.homeFrame
        self.playFrame = PlayFrame(self)
        self.addFrame = AddFrame(self)
        self.aboutFrame = AboutFrame(self)
        self.annotationFrame = AnnotationFrame(self)
        self.minimalPairsFrame = MinimalPairsFrame(self)
        self.currentFrame.pack()
        self.title('A Graphical User Interface for Corpus Building')
        
        self.mainloop()
        
        

    def home(self):
        self.currentFrame.pack_forget()
        self.currentFrame = self.homeFrame
        self.currentFrame.pack()
        

    def add(self):
        self.currentFrame.pack_forget()
        self.currentFrame = self.addFrame
        self.currentFrame.pack()

    def play(self):
        self.currentFrame.pack_forget()
        self.currentFrame = self.playFrame
        self.currentFrame.pack()
        
    def annotate(self):
        self.currentFrame.pack_forget()
        self.currentFrame = self.annotationFrame
        self.currentFrame.pack()
        
    def about(self):
        self.currentFrame.pack_forget()
        self.currentFrame = self.aboutFrame
        self.currentFrame.pack()
    def mp(self):
        self.currentFrame.pack_forget()
        self.currentFrame = self.minimalPairsFrame
        self.currentFrame.pack()

    def save(self):
        pickle.dump(self.corpusDict, open(self.pickleFile, 'wb'))

    def update(self):
        self.playFrame.destroy()
        self.playFrame = PlayFrame(self)
        self.annotationFrame.destroy()
        self.annotationFrame = AnnotationFrame(self)



gui = CorpusGUI()
