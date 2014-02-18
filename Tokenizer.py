#this is a tool to train a decent tokenizer so I can stop fucking around
#use _ to denote new spaces and | to denote new lines
from Tkinter import *
from Corpus import *
import pickle, random


class TokenizerFrame(Frame):
    
    def __init__(self, parent, corpus):
        Frame.__init__(self, parent)
        self.corpus = corpus
        self.parent = parent
        self.title = None
        #self.textDict = pickle.load(open('pos.p', 'rb'))
        self.textDict = {work.title: (work.rawText, work.rawText) for work in self.corpus.worksSet}
        
        self.work = StringVar()
        self.work.trace('w', self.setWork)
        self.workList = [work.title for work in self.corpus.worksSet]
        self.workMenu = apply(OptionMenu, (self, self.work) + tuple(self.workList))
        self.workMenu.grid(row=0, column=0, columnspan=2)
         
        self.text = Text(self, width=75, height=40, wrap=WORD)
        self.toks = Text(self, width=75, height=40, wrap=WORD)
        self.text.grid(row=1, column=0)
        self.toks.grid(row=1, column=1)
        
        Button(self, text='Save', command=self.save).grid(row=2, column=0, columnspan=2)
        
    
    def setWork(self, *args):
        if self.title:
            self.textDict[self.title] = (self.textDict[self.title][0], self.toks.get(1.0, END))
        self.title = self.work.get()
        self.text.delete(1.0, END)
        self.toks.delete(1.0, END)
        self.text.insert(END, self.textDict[self.title][0])
        self.toks.insert(END, self.textDict[self.title][1])
    
    def save(self, *args):
        pickle.dump(self.textDict, open('pos.p', 'wb'))
            
        
class Tokenizer:
    def __init__(self, pickleFile='pos.p'):
        dic = pickle.load(open(pickleFile, 'rb'))
        self.pairs = tuple([dic[x] for x in dic if dic[x][0] != dic[x][1]])
        self.punct = [',', '"', "'", '-', ';', ':', '(', ')']
        self.finals = ['.', '?', '!']
        self.training = []
        self.testing = []
        self.DISCOUNT = .5
        for x in self.pairs:
            if random.randrange(0, 9) == 9:
                self.testing.append(x)
            else:
                self.training.append(x)
        self.unigrams = self.getNgramStats(N=1)
        self.bigrams = self.getNgramStats(N=2)
        self.trigrams = self.getNgramStats(N=3)
        
        
        
    def getNgramStats(self, N=1):
        inp = u''
        outp = u''
        nm1 = N-1
        inp += '* ' * nm1
        outp += '* ' * nm1
        for text in self.testing:
            inp += text[0]
            outp += text[1]
        inp = inp.split()
        outp = outp.split()
        if len(outp) == len(inp):
            print "It's working!! It's ALIVE!" + str(N)
        else:
            print "No luck braj" + str(N)
        
        
        grams = {}
        
        for i in range(len(inp)-nm1):
            gram = ' '.join(inp[i:i+N])
            w = outp[i+nm1]
            if gram in grams:
                if w in grams[gram]:
                    grams[gram][w] += 1
                else:
                    grams[gram][w] = 1
            else:
                grams[gram] = {}
                grams[gram][w] = 1
        for gram in grams:
            count = 0
            dic = grams[gram]
            for w in dic:
                count += dic[w]
            for w in dic:
                dic[w] = (dic[w] - self.DISCOUNT) / float(count)
            dic['MPM'] = (len(dic) * self.DISCOUNT) / float(count)
            grams[gram] = dic
        return grams
    
    
    def tokenize(self, string):
        hyp = string
        for x in self.punct:
            hyp = hyp.replace(x, '_'+x+'_')
        for x in self.finals:
            hyp = hyp.replace(x, '_'+x+'|')
        hyp = ['*', '*'] + hyp.split()
        string = ['*', '*'] + string.split()
        outp = u''
        
        for i in range(len(string)-2):
            trigram =  ' '.join(string[i:i+3]) 
            if trigram in self.trigrams:
                for w in self.trigrams[trigram]
        
        
rgn = pickle.load(open('beta_corpus.p', 'rb'))['Romagnol']

root = Tk()

frame = TokenizerFrame(root, rgn)
frame.pack()

root.mainloop()