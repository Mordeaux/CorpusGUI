# -*- coding: utf-8 -*-
import codecs, pickle, re
from Tkinter import *




class Work:
    def __init__(self, title, source, rawText, author=None, town=None,
                 genre=None, rawTranslation=None, year=None, annotation=None):
        self.title = title
        self.source = source
        self.rawText = rawText
        self.text = self.clean(rawText)
        self.author = author
        self.town = town
        self.genre = genre
        self.year = year
        self.rawTranslation = rawTranslation
        if rawTranslation:
            self.translation = self.clean(rawTranslation, trans=True)
        else:
            self.translation = rawTranslation
        self.getParallel()
        self.anno = {} 
        #if annotation:
        #    self.anno = annotation
        self.getPOS()

    def __str__(self):
        return self.title

    def getParallel(self):
        if self.translation:
            sourceLines = self.clean(self.rawText).split('\n')
            transLines = self.clean(self.rawTranslation, trans=True).split('\n')
            self.parallel = tuple([(sourceLines[x], transLines[x]) for x in range(len(sourceLines)) if sourceLines[x] != ''])
        else:
            lines = self.clean(self.rawText, remove=True).split('\n')
            self.parallel = tuple([(lines[x], '') for x in range(len(lines)) if lines[x] != ''])


    def getPOS(self):
        if 'pos' in self.anno:
            pass
        else:
            pos = []
            for x in range(len(self.parallel)):
                line = self.parallel[x][0]
                pos.append(tuple([(line.split()[y], '')
                                  for y in range(len(line.split()))]))
            source = tuple(pos)
            trans = []
            if self.translation:
                for x in range(len(self.parallel)):
                    line = self.parallel[x][1]
                    trans.append(tuple([(line.split()[y], '')
                                           for y in range(len(line.split()))]))
            self.anno['pos'] = [source, tuple(trans)]

    
    def clean(self, text, remove=False, trans=False):
        "Takes a text, returns a tokenized list of words in lowercase"
        syms = ['!', '"', '$', '%', '&', '(', ')', '*', '+', ',',
                '-', '.', '/', ':', ';', '<', '=', '>', '?', '@',
                '[', ']', '_', '`', '{', '}', '~', '#', '|', '^',
                u'»', u'«']
        
        undesireables = [(u'…', u'...'), (u'“', u'"'), (u'”', u'"'),
                         (u'’', u"'"), (u'‘', u"'")] 
        for x in undesireables:
            text = text.replace(x[0], x[1])
        for s in syms :
            if not remove:
                text = text.replace(s, ' '+s+' ') #keeps punct
            else:
                text = text.replace(s, ' ')         #removes punct
        if trans:
            if not remove:
                text = text.replace("'", " ' ")
            else:
                text = text.replace("'", ' ')
        else:
            il = [(r"\bE'(?=\s)", u"-il1-"), (r"\be'(?=\s)", u"-il2-")]
            for x in il:
                text = re.sub(x[0], x[1], text, re.U)
            if not remove:
                text = text.replace("'", " ' ")
            else:
                text = text.replace("'", ' ')
            text = text.replace(u"-il1-", "E'")
            text = text.replace(u"-il2-", "e'")
        return text
        


class Corpus:
    def __init__(self, worksList, language):
        self.worksSet = set(x for x in worksList)
        self.titles = set(x.title for x in self.worksSet)
        self.language = language
        self.sortingHat()
        self.wordDict = [{}, {}]
        self.regexDict = None



    def add(self, work):
        self.worksSet.add(work)
        return Corpus(list(self.worksSet), self.language)

    def getAuthors(self):
        return set(x.author for x in self.worksSet)
    def getGenres(self):
        return set(x.genre for x in self.worksSet if x.genre)
    def getTowns(self):
        return set(x.town for x in self.worksSet if x.town)
    def getSources(self):
        return set(x.source for x in self.worksSet)

    def subcorpus(self, author=None, genre=None, source=None, town=None):
        #wList = [x for x in self.worksSet]
        newList = [x for x in self.worksSet]
        if author and author != 'None':
            newList = [x for x in newList if x.author == author]
        if genre and genre != 'None':
            newList = [x for x in newList if x.genre == genre]
        if source and source != 'None':
            newList = [x for x in newList if x.source == source]
        if town and town != 'None':
            newList = [x for x in newList if x.town == town]
        return SubCorpus(newList)
    
    def getToks(self):
        tokens = []
        for work in self.worksSet:
            tokens += work.clean(work.text, remove=True).lower().split()
        return tokens

    def getTypes(self):
        return set(self.getToks())
    def getTTR(self):
        return len(self.getTypes())/float(len(self.getToks()))

    def getWordNGrams(self, n=1):
        """Does not respect text/line boundaries"""
        freqdict = {}
        toks = self.getToks()
        for x in range(len(toks)-(n-1)):
            gram = ' '.join(toks[x:x+n])
            if gram not in freqdict:
                freqdict[gram] = 1
            else:
                freqdict[gram] += 1
        return [(x, freqdict[x]) for x in sorted(freqdict, key=freqdict.get, reverse=True)]

    def getCharNGrams(self, n=1, percent=False):
        """Does not respect word boundaries"""
        freqdict = {}
        toks = ''.join(self.getToks())
        for x in range(len(toks)-(n-1)):
            gram = toks[x:x+n]
            if gram not in freqdict:
                freqdict[gram] = 1
            else:
                freqdict[gram] += 1
        if percent == True:
            total = len(toks)
            return [(x, freqdict[x]/float(total)) for x in sorted(freqdict, key=freqdict.get, reverse=True)]
        else:
            return [(x, freqdict[x]) for x in sorted(freqdict, key=freqdict.get, reverse=True)]

    def find(self, string):
        hits = {}
        for work in self.worksSet:
            text = work.rawText
            if re.search(string, text, re.U|re.M):
                lines = text.split('\n')
                hits[work.title] = tuple([(lines[x], x) for x in range(len(
                    lines)) if re.search(string, lines[x], re.U|re.M)])
        return hits

    def findWord(self, string, translated=False):
        words = set()
        works = self.worksSet
        if translated:
            works = [x for x in works if x.translation]
        for work in works:
            for word in work.clean(work.rawText, remove=True).lower().split():
                if re.search(string, word, re.U|re.I):
                    words.add(word) 
        return words

    def getWord(self, token, trans=False):
        if token not in self.wordDict[trans]:
            self.wordDict[trans][token] = Word(token, self, trans=trans)
        return self.wordDict[trans][token]

    
    def sourceToTrans(self):
        freqDict = {}
        translated = [work for work in self.worksSet if work.translation]
        for work in translated:
            for line in work.parallel:
                for sWord in line[0].lower().split():
                    if sWord in freqDict:
                        for tWord in line[1].lower().split():
                            if tWord in freqDict[sWord]:
                                freqDict[sWord][tWord] += 1
                            else:
                                freqDict[sWord][tWord] = 1
                    else:
                        freqDict[sWord] = {}
                        for tWord in line[1].lower().split():
                            if tWord in freqDict[sWord]:
                                freqDict[sWord][tWord] += 1
                            else:
                                freqDict[sWord][tWord] = 1
        return freqDict

    def getMinimalPairs(self):
        regexDict = {}
        text = u''
        regexSet = set()
        words = set()
        if self.regexDict:
            return self.regexDict
        else:
            for work in self.worksSet:
                text = set(work.clean(work.rawText, remove=True).lower().split())
                for word in text:
                    words.add(word)
            for word in words:
                for regex in self.getWord(word).getMinimalPairs():
                    if regex in regexDict:
                        regexDict[regex].add(word)
                    else:
                        regexDict[regex] = set([word])
                    regexSet.add(regex)
            singletons = []
            for regex in regexDict:
                if len(regexDict[regex]) == 1:
                    singletons.append(regex)
            for regex in singletons:
                del regexDict[regex]
            self.regexDict = regexDict
            return regexDict
            
                
            
    
                    
        


    def sortingHat(self):
        authors = {}
        for x in self.getAuthors():
            authors[x] = [y for y in self.worksSet if y.author == x]
        genres = {}
        for x in self.getGenres():
            genres[x] = [y for y in self.worksSet if y.genre == x]
        towns = {}
        for x in self.getTowns():
            towns[x] = [y for y in self.worksSet if y.town == x]
        sources = {}
        for x in self.getSources():
            sources[x] = [y for y in self.worksSet if y.source == x]
        attr = {
            'translated': [x for x in self.worksSet if x.translation != None]
            }
        self.worksDict = {'authors': authors, 'genres': genres,
                          'towns': towns, 'sources': sources,
                          'attr': attr}
    def getChars(self):
        text = ''
        for work in self.worksSet:
            text += work.rawText
        return set(list(text))

class SubCorpus(Corpus):
    def __init__(self, worksList):
        Corpus.__init__(self, worksList, 'subcorpus')
        

    def add(self, work):
        print "Please don't try to add to a subcorpus"

    def subcorpus(self, author=None, genre=None, source=None, town=None):
        pass
        
class Word():
    def __init__(self, token, corpus, trans=False):
        self.token = token
        self.corpus = corpus
        self.trans = trans
        #self.regex = self.getRegex()
        
        self.posDict = False
        self.transDict = False
    
        


    def getRegex(self):
        li = [r'\b'] + list(self.token) + [r'(?=(\b|\W))']
        li[1] = r'(' +li[1].upper() + r'|' + li[1].lower() + r')'
        if self.token == 'e' and not self.trans:
            return r'\be\s'
        else:
            return ''.join(li)

    def getPOS(self):
        if not self.posDict:
            posDict = {}
            for work in self.corpus.worksSet:
                pos = work.anno['pos'][self.trans]
                for line in pos:
                    for token in line:
                        if token[0] == self.token:
                            if token[1] != '':
                                if token[1] in posDict:
                                    posDict[token[1]] +=1
                                else:
                                    posDict[token[1]] = 1
            self.posDict = posDict
            if len(self.posDict) == 0:
                self.posDict[None] = 1
        return sorted(self.posDict, key=self.posDict.get, reverse=True)[0]
            
    def getTranslation(self, freq=False):
        if not self.transDict:
            transDict = {}
            for work in self.corpus.worksSet:
                if work.translation:
                    for line in work.parallel:
                        if self.token in line[self.trans].split():
                            for tWord in line[not self.trans].split():
                                if tWord in transDict:
                                    transDict[tWord] += 1
                                else:
                                    transDict[tWord] = 1
            self.transDict = transDict
            if len(self.transDict) == 0:
                self.transDict[None] = 1
            transSort = sorted(self.transDict, key=self.transDict.get, reverse=False)
            bestTrans = transSort[-1]
            for tWord in transSort:
                pos = self.corpus.getWord(tWord, trans=not self.trans).getPOS()
                if pos == self.getPOS():
                    bestTrans = tWord
            self.bestTrans = bestTrans
        if not freq:
            return self.bestTrans
        else:
            return (self.bestTrans, self.transDict[self.bestTrans])

    def getMinimalPairs(self):
        regexList = []
        if len(self.token) == 1:
            regexList.append(r'\b\w\b')
        else:
            for x in range(len(self.token)):
                token = list(self.token)
                token[x] = r'(\w?)'
                regex = ''.join([r'\b'] + token +[ r'\b'])
                regexList.append(regex)
            
        return regexList

def cor():
    return pickle.load(open('beta_corpus.p', 'rb'))['Romagnol']


def update():
    
    corpusDict = pickle.load(open('beta_corpus.p', 'rb'))
    
    for d in corpusDict:
        worksList = []
        undesireables = [(u'þ', u'ṣ'), (u'ð', u'ẓ'), (u'Ð', u'Ẓ'), (u'Þ', u'Ṣ')] #ê
        for w in corpusDict[d].worksSet:
            for x in undesireables:
                w.rawText = w.rawText.replace(x[0], x[1])
                w.title = w.title.replace(x[0], x[1])
                w.title = w.title.replace(u'Ý', u'ẓ')
        
##        if type(w.text) != type(u''):
##            w.text = w.text.decode('utf-8')        
            y = Work(w.title, w.source, w.rawText, author=w.author, town=w.town,
                     genre=w.genre, rawTranslation=w.rawTranslation, year=w.year,
                     annotation=w.anno)
            worksList.append(y)

        corpusDict[d] = Corpus(worksList, corpusDict[d].language)
    
        

    pickle.dump(corpusDict, open('beta_corpus.p', 'wb'))
    #pickle.dump(corpusDict, open('jumper.p', 'wb'))
    return pickle.load(open('beta_corpus.p', 'rb'))['Romagnol']

#x = update()
