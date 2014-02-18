# -*- coding: utf-8 -*-
from Tkinter import *
from Corpus import *
import pickle, re





class CorpusGUI(Tk):
    def __init__(self, title=None, pickleFile='beta_corpus.p'):
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

class AboutFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        Label(self, text='Created by Michael Mordowanec').pack(padx=30, pady=30)
        Label(self, text='(c) 2013').pack(padx=30, pady=30)
        



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

        
class PlayFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        
        self.corpus = self.parent.currentCorpus
        self.subcorpus = self.corpus
        self.subcorpusMenu()
        self.display()
        self.search()
        self.currentFrame = self.displayFrame
        self.currentFrame.grid(row=0, column=1)

    def subcorpusMenu(self):
        self.subcorpusFrame = Frame(self)

        Button(self.subcorpusFrame, text='Search', command=self.setSearch).pack()
        Button(self.subcorpusFrame, text='Stats', command=self.setDisplay).pack()
        

        self.author = StringVar()
        self.author.set(None)
        Label(self.subcorpusFrame, text='Authors:').pack()
        self.authorsList = [None]
        self.authorsList.extend([x for x in self.corpus.getAuthors()])
        self.authorMenu = apply(OptionMenu, (self.subcorpusFrame, self.author) + tuple(self.authorsList))
        self.authorMenu.pack()

        self.town = StringVar()
        self.town.set(None)
        Label(self.subcorpusFrame, text='Towns:').pack()
        self.townList = [None]
        self.townList.extend([x for x in self.corpus.getTowns()])
        self.townMenu = apply(OptionMenu, (self.subcorpusFrame, self.town) + tuple(self.townList))
        self.townMenu.pack()

        self.source = StringVar()
        self.source.set(None)
        Label(self.subcorpusFrame, text='Sources:').pack()
        self.sourceList = [None]
        self.sourceList.extend([x for x in self.corpus.getSources()])
        self.sourceMenu = apply(OptionMenu, (self.subcorpusFrame, self.source) + tuple(self.sourceList))
        self.sourceMenu.pack()

        self.genre = StringVar()
        self.genre.set(None)
        Label(self.subcorpusFrame, text='Genres:').pack()
        self.genreList = [None]
        self.genreList.extend([x for x in self.corpus.getGenres()])
        self.genreMenu = apply(OptionMenu, (self.subcorpusFrame, self.genre) + tuple(self.genreList))
        self.genreMenu.pack()

        self.author.trace('w', self.getSubcorpus)
        self.town.trace('w', self.getSubcorpus)
        self.source.trace('w', self.getSubcorpus)
        self.genre.trace('w', self.getSubcorpus)

        
        self.subcorpusFrame.grid(row=0, column=0)
        
        
    def show(self):
        GraphDialog(self, 'authors')

    def search(self):
        self.searchFrame = Frame(self)
        self.searchVar = StringVar()
        self.searchVar.trace('w', self.showSearch)
        Label(self.searchFrame, text='Regular Expression:').grid(row=0, column=0)
        Entry(self.searchFrame, textvariable=self.searchVar, width=30).grid(row=0, column=1)
        self.results = Text(self.searchFrame, width=75, height=40, wrap=WORD)
        self.results.grid(row=1, column=0, columnspan=2)
        self.searchStatsFrame = Frame(self.searchFrame)
        Label(self.searchFrame, text='   Word : Possible Translation').grid(row=0, column=2)


    def showSearch(self, *args):
        regex = unicode(self.searchVar.get())
        if len(regex) > 0:
            if regex[-1] == '\\':
                pass
            elif regex.count('(') != regex.count(')'):
                pass
            elif regex.count('{') != regex.count('}'):
                pass
                
            else:
                searchDict = self.subcorpus.find(regex)
                textList = []
                for work in searchDict:
                    textList.append(work + ':\n')
                    for line in searchDict[work]:
                        textList.append('\t'+'Line:'+str(line[1])+'\n\t\t'+line[0]+'\n')
                self.results.delete(1.0, END)
                text = ''.join(textList)
                self.results.insert(1.0, text)

                self.searchStatsFrame.destroy()
                self.searchStatsFrame = Frame(self.searchFrame)
                transDict = self.subcorpus.sourceToTrans()
                mostFreq = {}
                words = list(self.subcorpus.findWord(regex, translated=True))
                for word in words:
                    sdict = transDict[word] #make this us the Word class!    #
                    trans = sorted(sdict, key=sdict.get, reverse=True)[0]    # SPEED
                    n = sdict[trans]                                         #
                    mostFreq[(word, trans)] = n                           #
                    #obj = self.subcorpus.getWord(word)                           #
                    #transTup = obj.getTranslation(freq=True)                     # ACCURACY
                    #mostFreq[(word, transTup[0])] = transTup[1]                  #
                    
                for wordPair in sorted(mostFreq, key=mostFreq.get, reverse=True)[:20]:
                    Label(self.searchStatsFrame, text=wordPair[0]+'  :  '+wordPair[1]).pack()
                
                self.searchStatsFrame.grid(row=1, column=2)                
        

                
                            

    def display(self):
        self.displayFrame = Frame(self)
        self.titleFrame = Frame(self.displayFrame)
        Label(self.titleFrame, text='Titles:').pack()
        for x in self.subcorpus.titles:
            Label(self.titleFrame, text=x).pack()
        if len(self.subcorpus.titles) <= 17:
            self.titleFrame.grid(row=0, column=0)

        self.statsFrame = Frame(self.displayFrame)
        Label(self.statsFrame, text='Number of works: ' +
                                  str(len(self.subcorpus.worksSet))).pack()
        Label(self.statsFrame, text='Number of tokens: ' +
                                  str(len(self.subcorpus.getToks()))).pack()
        Label(self.statsFrame, text='Number of types: ' +
                                  str(len(self.subcorpus.getTypes()))).pack()
        Label(self.statsFrame, text='TTR: ' + str(self.subcorpus.getTTR())).pack()

        self.statsFrame2 = Frame(self.displayFrame)

        uni = self.subcorpus.getWordNGrams()
        Label(self.statsFrame2, text='Top 5 word unigrams').pack()
        for x in range(5):
            Label(self.statsFrame2, text=uni[x][0]
                  + ': ' + str(uni[x][1])).pack()
            
        bi = self.subcorpus.getWordNGrams(n=2)
        Label(self.statsFrame2, text='Top 5 word bigrams').pack()
        for x in range(5):
            Label(self.statsFrame2, text=bi[x][0]
                  + ': ' + str(bi[x][1])).pack()

        self.statsFrame3 = Frame(self.displayFrame)
        Label(self.statsFrame3, text='Character frequencies: ').grid(row=0, column=0, columnspan=2)
        self.statsFrame3one = Frame(self.statsFrame3)
        self.statsFrame3two = Frame(self.statsFrame3)
        
        chars = self.subcorpus.getCharNGrams(percent=True)
        for x in range(len(chars)):
            if x < len(chars)/2:
                Label(self.statsFrame3one, text=chars[x][0]
                      + ': ' + str(chars[x][1])[2:4] + '.' + str(chars[x][1])[4:7]
                      + '%').pack()
            else:
                Label(self.statsFrame3two, text=chars[x][0]
                      + ': ' + str(chars[x][1])[2:4] + '.' + str(chars[x][1])[4:7]
                      + '%').pack()
        self.statsFrame3one.grid(row=1, column=0)
        self.statsFrame3two.grid(row=1, column=1)
        
        Label(self.statsFrame2, text='Top 5 character bigrams').pack()
        bichar = self.subcorpus.getCharNGrams(n=2)
        for x in range(5):
            Label(self.statsFrame2, text=bichar[x][0]
                  + ': ' + str(bichar[x][1])).pack()


        
        self.statsFrame.grid(row=0, column=1)
        self.statsFrame2.grid(row=0, column=2)
        self.statsFrame3.grid(row=0, column=3)
        

    def getSubcorpus(self, name, *args):
        subcorpus = self.corpus.subcorpus(author=self.author.get(),
                                               town=self.town.get(),
                                               source=self.source.get(),
                                               genre=self.genre.get())
        if len(self.subcorpus.titles) == 0:
            print 'Error, no input to Subcorpus constructor' #allow this to select the main corpus instance

        else:
            if len(subcorpus.worksSet) == len(self.corpus.worksSet):
                self.subcorpus = self.corpus
            else:
                self.subcorpus = subcorpus
            regex = self.searchVar.get()
            if self.currentFrame == self.displayFrame:
                self.displayFrame.destroy()
                self.searchFrame.destroy()
                self.display()
                self.search()
                self.currentFrame = self.displayFrame
            elif self.currentFrame == self.searchFrame:
                self.displayFrame.destroy()
                self.searchFrame.destroy()
                self.display()
                self.search()
                self.currentFrame = self.searchFrame
            
            self.currentFrame.grid(row=0, column=1)
            self.searchVar.set(regex)

    def setSearch(self, *args):
        self.currentFrame.grid_forget()
        self.currentFrame = self.searchFrame
        self.currentFrame.grid(row=0, column=1)

    def setDisplay(self, *args):
        self.currentFrame.grid_forget()
        self.currentFrame = self.displayFrame
        self.currentFrame.grid(row=0, column=1)

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

class AnnotationFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.corpus = self.parent.currentCorpus
        self.posFrame = Frame(self)
        self.posFrame.pack()
        self.currentFrame = self.posFrame
        
        self.optionMenu()
        self.posTag()
        




    def optionMenu(self):
        self.optionFrame = Frame(self)
        #Button(self.optionFrame, text='POS', command=self.pos)

        self.work = StringVar()
        self.worksList = [x for x in self.corpus.titles]
        self.work.set(self.worksList[0])
        self.work.trace('w', self.posTag)
        Label(self.optionFrame, text='Works:').grid(column=0, row=0)
        self.worksMenu = apply(OptionMenu, (self.optionFrame, self.work) + tuple(self.worksList))
        self.worksMenu.grid(column=1, row=0)
        Label(self.optionFrame, text='Page #:').grid(column=2, row=0)
        self.pageMenu = Frame(self.optionFrame)
        self.pageMenu.grid(column=3, row=0)

        self.transBool = BooleanVar()
        Checkbutton(self.optionFrame, text='Tag Translation', variable=self.transBool, onvalue=True, offvalue=False).grid(column=4, row=0)
        self.transBool.trace('w', self.posTag)
        self.optionFrame.pack()



    def posTag(self, *args):
        self.posFrame.destroy()
        self.posFrame = Frame(self)
        self.currentFrame.pack_forget()
        self.currentFrame = self.posFrame
        for x in self.corpus.worksSet:
            if x.title == self.work.get():
                self.workObj = x
        if self.workObj.rawTranslation:
            if self.transBool.get():
                parallel = [line for line in self.workObj.text.split('\n')]
            else:
                parallel = [line for line in self.workObj.rawTranslation.split('\n')]
        else:
            parallel = [line[1] for line in self.workObj.parallel]
        self.pos = self.workObj.anno['pos'][self.transBool.get()]
        frameList = []
        self.variables = self.getVars(self.pos)

        for w in range(len(self.pos)/7):
            wframe = Frame(self.posFrame)
            for x in range(7):
                lineInd = x + w*7
                frame = Frame(wframe)
                lineTok = self.pos[lineInd]
                Label(frame, text=parallel[lineInd]).grid(row=0, column=0, columnspan=len(lineTok))
                for y in range(len(lineTok)):
                    Label(frame, text=lineTok[y][0], width=len(lineTok[y][0])*2).grid(row=1, column=y)
                    Entry(frame, textvariable=self.variables[lineInd][y], width=len(lineTok[y][0])*2).grid(row=2, column=y)
                frame.grid(row=x, column=0)
            frameList.append(wframe)
        if len(self.pos)%7 != 0:
            wframe = Frame(self.posFrame)
            for x in range(len(self.pos)%7, 0, -1):
                frame = Frame(wframe)
                lineTok = self.pos[-x]
                Label(frame, text=parallel[-x]).grid(row=0, column=0, columnspan=len(lineTok))
                for y in range(len(lineTok)):
                    Label(frame, text=lineTok[y][0], width=len(lineTok[y][0])*2).grid(row=1, column=y)
                    Entry(frame,textvariable=self.variables[-x][y], width=len(lineTok[y][0])*2).grid(row=2, column=y)
                frame.grid(row=range(len(self.pos)%7, 0, -1).index(x), column=0)
            frameList.append(wframe)
        if len(frameList) == 0:
            nothing = Frame(self.posFrame)
            Label(nothing, text='This work has no translation!').pack()
            frameList.append(nothing)
        self.currentPosFrameList = frameList
        self.currentPosFrame = self.currentPosFrameList[0]
        self.currentPosFrame.pack()

        self.page = IntVar()
        self.page.set(1)
        self.page.trace('w', self.changePage)
        self.pageMenu.grid_forget()
        self.pageMenu = apply(OptionMenu, (self.optionFrame, self.page) + tuple(range(1, len(frameList)+1)))
        
        self.pageMenu.grid(column=3, row=0)
        

        self.posFrame.pack()

    def getVars(self, pos):
        variables = []
        if len(pos) == 0:
            pass
        else:
            for x in range(len(pos)):
                line = []
                for y in range(len(pos[x])):
                    var = StringVar()
                    var.set(pos[x][y][1])
                    var.trace('w', self.setVars)
                    line.append(var)
                variables.append(line)
            return variables

    def setVars(self, *args):
                
        pos = []
        if len(self.pos) == 0:
            pass
        else:
            for x in range(len(self.pos)):
                pos.append(tuple([(self.pos[x][y][0], self.variables[x][y].get())
                                  for y in range(len(self.pos[x]))]))
            self.workObj.anno['pos'][self.transBool.get()] = tuple(pos)
            self.corpus.wordDict = [{}, {}]
                
                

    def changePage(self, *args):
        self.currentPosFrame.pack_forget()
        self.currentPosFrame = self.currentPosFrameList[self.page.get()-1]
        self.currentPosFrame.pack()
        


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
            

    
                

        
            
            
        
        
    




class Dialog(Toplevel):

    def __init__(self, parent, title=None):
        Toplevel.__init__(self, parent)
        self.transient(parent) #attaches it to the parent, when minimizing etc.
        if title:
            self.title(title)

        self.parent = parent
        self.result = None #what does this mean?

        body = Frame(self)
        self.initialFocus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set() #Makes this the only window user can interact with

        if not self.initialFocus:
            self.initialFocus = self

        self.protocol('WM_DELETE_WINDOW', self.cancel)

        self.geometry('+%d+%d' % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))
        self.initialFocus.focus_set()
        self.wait_window(self)

    def body(self, parent):
        pass
        

    def buttonbox(self):

        box = Frame(self)
        w = Button(box, text='OK', width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text='Cancel', width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind('<Return>', self.ok)
        self.bind('<Escape>', self.cancel)

        box.pack()

    def ok(self, event=None):
        if not self.validate():
            self.initialFocus.focus_set()
        else:
            self.withdraw() #what is?
            self.update_idletasks() #?

            self.apply()

            self.cancel()

    def cancel(self, event=None):

        self.parent.focus_set()
        self.destroy()


    def validate(self):
        return 1 #override this
    
    def apply(self): #this is purple already???
        pass

class GraphDialog(Dialog):
    def __init__(self, parent, criterion, method='ttr'):
        self.corpus = parent.subcorpus
        self.dic = self.corpus.worksDict[criterion]
        
        Dialog.__init__(self, parent)
        
    def body(self, parent):
        for x in self.dic:
            Label(parent, text=x + ': ' +
                  str(SubCorpus(self.dic[x]).getTTR())).pack()


gui = CorpusGUI()
