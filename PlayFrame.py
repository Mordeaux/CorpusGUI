from Tkinter import *

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
