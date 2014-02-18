from Tkinter import *

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
        


