from index import *
from nltk.corpus import wordnet as wn
from nltk.tokenize import *
from nltk import pos_tag

NEGATION = ['no','not','none','nor','nobody','nothing','neither','nowhere','never','hardly','scarcely','barely']

def getSynonyms(word):
    return set([item.name().split('.')[0] for item in wn.synsets(word)])

def getAntonyms(word):
    res = []
    for l in [item.lemmas()[0].antonyms() for item in wn.synsets(word)]:
        res.extend([item.name() for item in l])
    return set(res)

def importantWords(title):
    # try verbs
    pass
    
def statistics(title,sen):
    title = word_tokenize(title)
    title_tags = pos_tag(title)
    sen = word_tokenize(sen)
    sen_tags = pos_tag(sen)
    tverbs = []
    tnouns = []
    sverbs = []
    snouns = []
    for ttag in title_tags:
        if ttag[1].startswith('V'):
           tverbs.extend([ttag[0]])
        if ttag[1].startswith('N'):
            tnouns.extend([ttag[0]])
    for stag in sen_tags:
        if stag[1].startswith('V'):
           sverbs.extend([stag[0]])
        if stag[1].startswith('N'):
            snouns.extend([stag[0]])

    count = 0
    noVerb = True
    for tverb in tverbs:
        for syn in getSynonyms(tverb):
            pos = sen.index(syn) if syn in sverbs else -1
            if pos != -1:
                noVerb = False
                #print pos
                for word in sen[max([0,pos-5]):min([len(sen),pos+5])]:
                    #print word
                    if word in NEGATION:
                        count += 1
        for ant in getAntonyms(tverb):
            if ant in sverbs:
                noVerb = False
                count += 1
    noNoun = True
    for tnoun in tnouns:
        for syn in getSynonyms(tnoun):
            pos = sen.index(syn) if syn in snouns else -1
            if pos != -1:
                noNoun = False
        for ant in getAntonyms(tnoun):
            if ant in snouns:
                noNoun = False

    if noNoun and noVerb:
        return True
    if count > 0:
        return True
    else:
        return False


    

if __name__ == '__main__':
    # print getSynonyms('happy')
    # print getAntonyms('happy')
    index = Index.load('index_task2')
    count = {True:0,False:0}
    title = 'spider burrowed through tourist stomach and up into his chest'
    sen = 'spider does not burrow through tourist stomach and up into his chest'
    count[statistics(title,sen)] += 1
    #f = open('disagree_stances.csv','r')
    #for line in f.xreadlines():
    #    line = line.split(',')
    #    title = line[0].split(' ')
    #    bodyId = line[1]
    #    count[statistics(title,index.getBody(bodyId))] += 1
    #f.close()
    print count