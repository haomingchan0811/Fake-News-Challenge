from index import *
from nltk.corpus import wordnet as wn

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
    
def statistics(title,body):
    count = 0
    for word_title in title:
        for syn in getSynonyms(word_title):
            pos = body.index(syn) if syn in body else -1
            if pos != -1:
                for word in body[max([0,pos-10]):min([len(body),pos+10])]:
                    if word in NEGATION:
                        count += 1
        for ant in getAntonyms(word_title):
            if ant in body:
                count += 1

    if count > 0:
        return True
    else:
        return False


    

if __name__ == '__main__':
    # print getSynonyms('happy')
    # print getAntonyms('happy')
    index = Index.load('index_task2')
    count = {True:0,False:0}
    f = open('disagree_stances.csv','r')
    for line in f.xreadlines():
        line = line.split(',')
        title = line[0].split(' ')
        bodyId = line[1]
        count[statistics(title,index.getBody(bodyId))] += 1
    f.close()
    print count