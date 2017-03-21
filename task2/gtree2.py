from index import *
from nltk.corpus import wordnet as wn
from nltk.tokenize import *
from nltk import pos_tag
from extractSimSents import *

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
    
def statistics(title,sens):
    title = word_tokenize(title)
    title_tags = pos_tag(title)
    tverbs = []
    tnouns = []
    
    for ttag in title_tags:
        if ttag[1].startswith('V'):
           tverbs.extend([ttag[0]])
        if ttag[1].startswith('N'):
            tnouns.extend([ttag[0]])

    totalNum = float(len(tverbs)+len(tnouns))
    noVerb = True
    noNoun = True
    count = 0
    for sen in sens:
        sen = sen[0]
        sen = word_tokenize(sen)
        sen_tags = pos_tag(sen)
        sverbs = []
        snouns = []
        for stag in sen_tags:
            if stag[1].startswith('V'):
               sverbs.extend([stag[0]])
            if stag[1].startswith('N'):
                snouns.extend([stag[0]])       
        for tverb in tverbs:
            for syn in getSynonyms(tverb):
                pos = sen.index(syn) if syn in sen else -1
                if pos != -1:
                    noVerb = False
                    #print pos
                    for word in sen[max([0,pos-10]):min([len(sen),pos+10])]:
                        #print word
                        if word in NEGATION:
                            count += 1
            for ant in getAntonyms(tverb):
                if ant in sen:
                    noVerb = False
                    count += 1                
        for tnoun in tnouns:
            for syn in getSynonyms(tnoun):
                pos = sen.index(syn) if syn in sen else -1
                if pos != -1:
                    noNoun = False
                    for word in sen[max([0,pos-10]):min([len(sen),pos+10])]:
                        #print word
                        if word in NEGATION:
                            count += 1
            for ant in getAntonyms(tnoun):
                if ant in sen:
                    noNoun = False
                    count += 1

    if noNoun and noVerb:
        score = 0.0
        return score
    reverse = False
    for word in title:
        if word in NEGATION:
            reverse = True
    if reverse:
        score = float(count)/totalNum    
    else:
        score = 1 - float(count)/totalNum
    if (score == 1.0) and (not noVerb):
        score += 0.5
    score = score / 1.5
    return score


    

if __name__ == '__main__':
    # print getSynonyms('happy')
    # print getAntonyms('happy')
    index = Index.load('index_task2')
    count = {'disagree':0,'agree':0, 'discuss':0}
    #title = 'spider burrowed through tourist stomach and up into his chest'
    #sen = 'spider does not burrow through tourist stomach and up into his chest'
    #count[statistics(title,sen)] += 1
    f = open('training.csv','r')
    ag_ag = 0
    ag_no = 0
    cus_cus = 0
    cus_no = 0
    dis_no = 0
    dis_dis = 0
    th_dd = 0.2
    th_da = 0.67
    for line in f.xreadlines():
        line = line.split(',')
        title = line[0]
        bodyId = line[1]
        label = line[2]
        sens = selectSents(title, bodyId, 'agree', 10)
        #print sens
        score = statistics(title,sens)
        
        if score <= th_dd:
            predict = 'disagree'
        elif score <= th_da:
            predict = 'discuss'
        else:
            predict = 'agree'
        #print label
        #print predict
        #print '******'
        if label.startswith('a'):
            #print 'A'
            #print score
            if predict.startswith('a'):
                #print 'B'
                ag_ag += 1
                #print ag_ag
            else:
                #print 'C'
                ag_no += 1
                #print ag_dis

        elif label.startswith('disagr'):
            #print 'D'
            #print score
            if predict.startswith('disagr'):
                #print 'E'
                #print title
                #print sens

                dis_dis += 1
                #print dis_ag
            else:
                #print 'F'
                dis_no += 1
                #print dis_dis
        else:
            #print score
            if predict.startswith('disc'):
                cus_cus += 1
            else:
                cus_no += 1
        count[predict] += 1
    f.close()
    print count
    print 'ag_ag: ' + str(ag_ag)
    print 'ag_no: ' + str(ag_no)
    print 'cus_cus: ' + str(cus_cus)
    print 'cus_no: ' + str(cus_no)
    print 'dis_dis: ' + str(dis_dis)
    print 'dis_no: ' + str(dis_no)
    p = float(ag_ag + cus_cus + dis_dis) / (ag_ag + ag_no + cus_no + cus_cus + dis_dis + dis_no)
    #r = float(ag_ag) / (ag_ag + dis_ag)
    #a = float(ag_ag + dis_dis) / (ag_ag + ag_dis + dis_ag + dis_dis)
    #f1 = 2.0 * p * r / (p + r)
    print "Precison: " + str(p)
    #print "Recall: " + str(r)
    #print "F1: " + str(f1)
    #print "Accuracy: " + str(a)