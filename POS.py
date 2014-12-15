import random, re
from Corpus import *
#instead of p(label|word) (discriminative model) we will learn p(word, label) which is equal to p(label)p(word|label) (Generative Model)

class GenerativeModel:
    
    def __init__(self, corpus):
        self.corpus = corpus
        self.getSents()


                    
    def getSents(self):
        lines = ''
        training = ''
        testing = ''
        for work in self.corpus.worksSet:
            for line in work.anno['pos'][0]:
                for word in line:
                    lines += ' '+word[0] + '/' + word[1] + ' '
                 
        lines = ' '.join(lines.split())
        lines = re.sub(r'(\./.? ?)+', r'./.\n', lines, re.U)
        for line in lines.split('\n'):
            #line = ' '.join(line.split())
            rand = random.randrange(0, 10)
            if rand == 9:
                testing += line + '\n' 
            else:
                training += line + '\n'
        self.training = training
        self.testing = testing
        
    def emmissions(self):
        eDict = {}
        for word in text.split():
            pass
        
        



rgn = pickle.load(open('corpus.p', 'rb'))['English']
model = GenerativeModel(rgn)
