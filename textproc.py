# -*- coding: utf-8 -*-
# textproc.py
# A collection of text processing functions

#def getCharNGram(txt, n) :
#    "Takes a string and n, returns a list of char n-grams"
#    grams = []
#    for i in range(len(txt)-n +1) :
#        gram = txt[i:i+n]
#        grams.append(gram)
#    return grams

def getCharNGram(li, n) :
    "Takes a list of strings and n, returns a list of char n-grams"
    grams = []
    for x in range(len(li)):
        txt = li[x]
        if len(txt) < n:
            pass
        else:
            for i in range(len(txt)-n +1) :
                gram = txt[i:i+n]
                grams.append(gram)
    return grams

def getWordNGram(wds, n) :
    "Takes a list of words and n, returns a list of word n-grams"
    grams = []
    for i in range(len(wds)-n +1) :
        gram = ' '.join(wds[i:i+n])
        grams.append(gram)
    return grams


def getFreq(li) :
    "Takes a list of strings, returns frquency count as a dict"
    freq = {}
    for x in li :
        if x in freq: freq[x] += 1
        else: freq[x] = 1
    return freq


def getTopN(di, n) :
    """Takes a dictionary and n, returns a list of pairs (k,v)
    sorted by the value, in descending order"""
    li = []
    for k in sorted(di, key=di.get, reverse=True)[:n] :
        li.append((k,di[k]))
    return li



def getToks(text) :
    "Takes a text, returns a tokenized list of words in lowercase"
    syms = ['!', '"', '$', '%', '&', "'", '(', ')', '*', '+', ',',
            '-', '.', '/', ':', ';', '<', '=', '>', '?', '@',
            '[', ']', '_', '`', '{', '}', '~', '#', '|', '^', u'…',
            u'“', u'”']
    for s in syms :
#        text = text.replace(s, ' '+s+' ') #keeps punct
        text = text.replace(s, '')         #removes punct
    tokens = text.lower().split()
    return tokens


def getTypes(toks) :
    """Takes a tokenized list of words, returns a list of
    word types, alphabetically sorted"""
    toksset = set(toks)   # set() turns a list into a set
                          # object, removing duplicates
    # a set must be turned into a list before being sorted:
    return sorted(list(toksset))


    
# NOTE: getTTR below works off a raw piece of text, which means
# that if your caller script already has processed tokens and
# types, using this function will duplicate some of the steps. 
def getTTR(txt) :
    """Takes a completely unprocessed piece of text as input
    and returns the Type-Token Ratio (TTR)."""
    # Your code below:

    tokens = getToks(txt)
    types = getTypes(tokens)
    ratio = float(len(types)) / len(tokens)

    return ratio



    

    
def main() :
    print 'textproc.py'
    print 'A collection of common text processing functions.'
    print 'In the future, this main function will contain'
    print 'demos that showcase the functions in this module.'



if __name__ == '__main__':
    main()



