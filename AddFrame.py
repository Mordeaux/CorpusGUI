from Tkinter import *

class AddFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.translation = BooleanVar()
        
        self.draw()
        self.translation.trace('w', self.check)

    def draw(self):
        self.entry = Frame(self)
        
        
        self.addButton = Button(self.entry, text='Add', command=self.add)
        self.title = Entry(self.entry)
        self.author = Entry(self.entry)
        self.town = Entry(self.entry)
        self.source = Entry(self.entry)
        self.genre = Entry(self.entry)
        self.year = Entry(self.entry)
        Label(self.entry, text='Title').pack()
        self.title.pack()
        Label(self.entry, text='Author').pack()
        self.author.pack()
        Label(self.entry, text='Town').pack()
        self.town.pack()
        Label(self.entry, text='Source').pack()
        self.source.pack()
        Label(self.entry, text='Genre').pack()
        self.genre.pack()
        Label(self.entry, text='Year').pack()
        self.year.pack()
        self.addButton.pack()
        Checkbutton(self.entry, text='Add Translation', variable=self.translation, onvalue=True, offvalue=False).pack()
        self.text = Text(self, width=75, height=40, bg='yellow', wrap=WORD)        
        self.text.grid(row=0, column=1)
        Label(self, text='Text').grid(row=1, column=1)
        
        self.trans = Text(self, width=75, height=40, wrap=WORD)
        self.transLabel = Label(self, text='Translation')
        self.entry.grid(row=0, column=0)

    def add(self):
        title = self.title.get()
        if self.author.get().split() != '':
            author = self.author.get()
        else:
            author = None
        source = self.source.get()
        if self.town.get().split() != '':
            town = self.town.get()
        else:
            town = None
        if self.genre.get().split() != '':
            genre = self.genre.get()
        else:
            genre = None
        text = self.text.get(1.0, END)
        translation = None
        if self.translation.get():
            translation = self.trans.get(1.0, END)
        work = Work(title, source, text, author=author, town=town, genre=genre, rawTranslation=translation)
        if title not in self.parent.currentCorpus.titles:
            self.parent.corpusDict[self.parent.currentCorpus.language] = self.parent.currentCorpus.add(work)
            self.parent.update()
            self.text.delete(1.0, END)
            self.title.delete(0, END)
            self.trans.delete(1.0, END)
                
        
            
        

    def check(self, *args):
        if self.translation.get():
            self.trans.bind('<Double-Button-1>', self.clean)
            self.trans.grid(row=0, column=2)
            self.transLabel.grid(row=1, column=2)
        else:
           self.trans.grid_forget()
           self.transLabel.grid_forget()

    def clean(self, *args):
        
        x = self.trans.get(1.0, END)
        x = x.replace('\n', ' ')
        x = x.replace('//', '/')
        x = x.replace("""\\\\""", """\\""")
        x = x.replace('/', '\n')
        x = x.replace('\\', '\n')
        x = x.replace('\n ', '\n')
        x = x.replace(' \n', '\n')
        self.trans.delete(1.0, END)
        self.trans.insert(END, x)
