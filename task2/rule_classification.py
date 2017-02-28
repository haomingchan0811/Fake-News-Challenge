from index import *
from nltk.corpus import wordnet as wn
from rake_nltk import Rake

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

def sentence_rule(title,body):
    # [len(title),len(sentence),#syn appear,#ant appear,#negation appear]
    count = 0
    for word_title in title:
        for syn in getSynonyms(word_title):
            for sent in body:
                if syn in sent:
                    for word in sent:
                        if word in NEGATION:
                            count += 1
        for ant in getAntonyms(word_title):
            for sent in body:
                if ant in body:
                    count += 1

    return count > 0

def sentence_feature_sym(title,sent):
    # [len(title),len(sentence),#syn appear,#ant appear,#negation appear]
    numSyn = 0
    numAnt = 0
    numNegation = 0
    synList = []
    antList = []
    for word_title in title:
        for syn in getSynonyms(word_title):
            synList.append(syn)
        for ant in getAntonyms(word_title):
            antList.append(ant)
    for word in sent:
        if word in synList:
            print word
            numSyn += 1
        if word in antList:
            print word
            numAnt += 1
        if word in NEGATION:
            numNegation += 1

    return [len(title),len(sent),numSyn,numAnt,numNegation]

def keyword_extraction(text):
    r = Rake()
    r.extract_keywords_from_text(text)
    print r.get_ranked_phrases()

    

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
        count[sentence_rule(title,index.getBodySent(bodyId))] += 1
        keyword_extraction(' '.join(index.getBody(bodyId)))
    f.close()
    # print count