from Tkinter import *

class MinimalPairsFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.corpus = self.parent.currentCorpus
        self.regexDict = self.corpus.getMinimalPairs()
        
        self.searchVar = StringVar()

        self.entry = Entry(self, textvariable=self.searchVar)
        self.searchVar.trace('w', self.search)
        self.entry.grid(row=0, column=0)
        
        self.textDisplay = Text(self, width=100, height=60)
        self.textDisplay.grid(row=1, column=0)


    def search(self, *args):
        text = u''
        self.textDisplay.delete(1.0, END)
        for regex in self.regexDict:
            if re.match(regex, self.searchVar.get(), re.U|re.M):
                text += '\n' + regex.replace(r'(\w?)', '_').replace(r'\b', ' ').replace(r'\w', '_') + ':\n'
                for word in self.regexDict[regex]:
                    text += word + ', '

        self.textDisplay.insert(1.0, text)
            

