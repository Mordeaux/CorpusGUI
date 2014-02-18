#This script will contain the statistical modeling algorithms as class entities.
from Corpus import *
import pickle, random
import math


class KatzModel:
    """A language model hopefully based on the Katz Back Off method."""
    
    def __init__(self, corpus, discount=.5):
        self.corpus = corpus
        self.textSet = set([work.clean(work.rawText) for work in self.corpus.worksSet])
        self.DISCOUNT = discount
        self.getSents()
        self.unigrams = self.getUnigramStats()
        self.bigrams = self.getBigramStats()
        self.trigrams = self.getTrigramStats()
                        
    def getSents(self):
        lines = ''
        training = ''
        testing = ''
        for text in self.textSet:
            text = text.split('.')
            for line in text:
                line = ' '.join(line.split())
                line += line + ' .' + '\n'
                if line.split() != ['.']:
                    lines += line
        for line in lines.split('\n'):
            rand = random.randrange(0, 10)
            if rand == 9:
                testing += line + '\n' 
            else:
                training += line + '\n'
        self.sents = training
        self.testing = testing
        
    def getUnigramStats(self):
        statDict = {}
        tokens = self.sents.split()
        count = 0
        for tok in tokens:
            if tok in statDict:
                statDict[tok] += 1
            else:
                statDict[tok] = 1
            count += 1
        for tok in statDict:
            statDict[tok] = statDict[tok]/float(count)
        self.SINGLE_COUNT = 1/float(count)
        return statDict
        
    def getBigramStats(self):
        bigrams = {}
        for line in self.sents.split('\n'):
            toks = ['*'] + line.split()
            for i in range(len(toks)-1):
                bigram = toks[i:i+2]
                wm1 = bigram[0]
                w = bigram[1]
                if wm1 in bigrams:
                    if w in bigrams[wm1]:
                        bigrams[wm1][w] += 1
                    else:
                        bigrams[wm1][w] = 1
                else:
                    bigrams[wm1] = {}
                    bigrams[wm1][w] = 1
        for wm1 in bigrams:
            count = 0
            dic = bigrams[wm1]
            for w in dic:
                count += dic[w]
            for w in dic:
                dic[w] = (dic[w] - self.DISCOUNT) / float(count)
            dic['MPM'] = (len(dic) * self.DISCOUNT) / float(count)
            bigrams[wm1] = dic
        return bigrams

    def getTrigramStats(self):
        trigrams = {}
        for line in self.sents.split('\n'):
            toks = ['*', '*'] + line.split()
            for i in range(len(toks)-2):
                trigram = toks[i:i+3]
                w = trigram[2]
                bigram = ' '.join(trigram[:2])
                if bigram in trigrams:
                    if w in trigrams[bigram]:
                        trigrams[bigram][w] += 1
                    else:
                        trigrams[bigram][w] = 1
                else:
                    trigrams[bigram] = {}
                    trigrams[bigram][w] = 1
        for bigram in trigrams:
            count = 0
            dic = trigrams[bigram]
            for w in dic:
                count += dic[w]
            for w in dic:
                dic[w] = (dic[w] - self.DISCOUNT) / float(count)
            dic['MPM'] = (len(dic) * self.DISCOUNT) / float(count)
            trigrams[bigram] = dic       
        return trigrams
        
    def qMLunigram(self, w):
        """takes token as string and returns the qMaximum Likelihood for the token"""
        if w in self.unigrams:
            return self.unigrams[w]
        else:
            return self.SINGLE_COUNT
           
    
    def qMLbigram(self, wm1, w):
        """takes wm1 and w as strings and returns the qMaximum Likelihood for the bigram"""
        if wm1 in self.bigrams:
            dic = self.bigrams[wm1]
            if w in dic:
                return dic[w]
            else:
                denom = 1.0
                for x in dic:
                    if x != 'MPM':
                        denom -= self.unigrams[x] #this shortcut assumes that the sum of the qML(w) for all words that 
                                                  #are B for wm1 is equal to 1 - qML(w) for all words that are A.
                return dic['MPM'] * self.qMLunigram(w) / denom
        else:
            return self.qMLunigram(w)
            
    def qMLtrigram(self, wm2, wm1, w):
        bigram = wm2 + ' ' + wm1
        if bigram in self.trigrams:
            dic = self.trigrams[bigram]
            if w in dic:
                return dic[w]
            else:
                denom = 1.0
                for x in dic:
                    if x != 'MPM':
                        denom -= self.qMLbigram(wm1, x)
                return dic['MPM'] * self.qMLbigram(wm1, w) / denom
        else:
            return self.qMLbigram(wm1, w)
            
        
    def sentLikelihood(self, sentence):
        """Takes pre-tokenized sentences as strings only, please and thank you."""
        toks = ['*', '*'] + sentence.split()
        probs = [1 for x in toks[:-2]]
        for i in range(len(toks)-2):
            w = toks[i+2]
            wm1 = toks[i+1]
            wm2 = toks[i]
            probs[i] = math.log(self.qMLtrigram(wm2, wm1, w))
        prob = 0
        for x in probs:
            prob += x
        return prob
        
    def testModel(self):
        sents = self.testing.split('\n')
        probs = [1.0 for x in sents]
        for i in range(len(sents)):
            probs[i] = self.sentLikelihood(sents[i])
        prob = 0
        for x in probs:
            prob += x
        M = len(self.testing.split())
        l = prob/float(M)
        return 2**-l
        
        
class InterpolationModel(KatzModel):
    
    def __init__(self, corpus):
        KatzModel.__init__(self, corpus)
        
    def getBigramStats(self):
        bigrams = {}
        for line in self.sents.split('\n'):
            toks = ['*'] + line.split()
            for i in range(len(toks)-1):
                bigram = toks[i:i+2]
                wm1 = bigram[0]
                w = bigram[1]
                if wm1 in bigrams:
                    if w in bigrams[wm1]:
                        bigrams[wm1][w] += 1
                    else:
                        bigrams[wm1][w] = 1
                else:
                    bigrams[wm1] = {}
                    bigrams[wm1][w] = 1
        for wm1 in bigrams:
            count = 0
            dic = bigrams[wm1]
            for w in dic:
                count += dic[w]
            for w in dic:
                dic[w] = dic[w] / float(count)
            bigrams[wm1] = dic
        return bigrams
    
    def getTrigramStats(self):
        trigrams = {}
        for line in self.sents.split('\n'):
            toks = ['*', '*'] + line.split()
            for i in range(len(toks)-2):
                trigram = toks[i:i+3]
                w = trigram[2]
                bigram = ' '.join(trigram[:2])
                if bigram in trigrams:
                    if w in trigrams[bigram]:
                        trigrams[bigram][w] += 1
                    else:
                        trigrams[bigram][w] = 1
                else:
                    trigrams[bigram] = {}
                    trigrams[bigram][w] = 1
        for bigram in trigrams:
            count = 0
            dic = trigrams[bigram]
            for w in dic:
                count += dic[w]
            for w in dic:
                dic[w] = dic[w] / float(count)
            trigrams[bigram] = dic       
        return trigrams
        
    def qMLbigram(self, wm1, w):
        if wm1 in self.bigrams:
            dic = self.bigrams[wm1]
            if w in dic:
                return dic[w]
            else: 
                return 0.0
        else:
            return 0.0
            
    def qMLtrigram(self, wm2, wm1, w):
        bigram = wm2+' '+wm1
        if bigram in self.trigrams:
            dic = self.trigrams[bigram]
            if w in dic:
                return dic[w]
            else:
                return 0.0
        else:
            return 0.0
    
    def sentLikelihood(self, sentence):
        
        toks = ['*', '*'] + sentence.split()
        probs = [1 for x in toks[:-2]]
        for i in range(len(toks)-2):
            w = toks[i+2]
            wm1 = toks[i+1]
            wm2 = toks[i]
            l1 = self.qMLunigram(w)/float(3)
            l2 = self.qMLbigram(wm1, w)/float(3)
            l3 = self.qMLtrigram(wm2, wm1, w)/float(3)
            probs[i] = math.log(l1 + l2 + l3)
        prob = 0
        for x in probs:
            prob += x
        return prob              
                    
       
        
        

rgn = pickle.load(open('beta_corpus.p', 'rb'))['Romagnol']


discounts = range(10, 100, 10)

for x in discounts:
    tests = range(0, 10)
    for i in range(len(tests)):
        model = KatzModel(rgn, discount=x/100.0)
        tests[i] = model.testModel()
    prob = sum(tests)/float(len(tests))
    print '\n'
    print 'Discount: ' + str(x/100.0) + '  '
    print 'Average Perplexity: ' + str(prob)

model = InterpolationModel(rgn)
print model.testModel()
    


    