import nltk
from nltk.corpus import stopwords
import re
def cleanStances(stancesFileName,outputFileName):
    f = open(stancesFileName,'r')
    output = open(outputFileName, 'w')
    for line in f.xreadlines():
        line = line.replace('\n','').split(",")
        headline = ','.join(line[:-2])
        stop = set(stopwords.words('english'))
        newHeadline = [i for i in nltk.word_tokenize(headline.lower()) if i.isalnum()]
        output.write(' '.join(newHeadline) + ',' + line[-2] + ',' + line[-1])
    f.close()
    output.close()

def cleanBodies(bodiesFileName,outputFileName):
    stop = set(stopwords.words('english'))
    f = open(bodiesFileName,'r')
    output = open(outputFileName, 'w')
    lastBody = []
    lastId = None
    for line in f.xreadlines():
        line = line.replace('\n','').split(",")
        bodyid = line[0]
        if bodyid.isdigit():
            if lastId:
                output.write(lastId + ',' + ' '.join(lastBody).encode('utf-8') + '\n')
            lastBody = []
            lastId = bodyid
            tmp = [i for i in nltk.word_tokenize(','.join(line[1:]).lower().decode('utf-8')) if i.isalnum()]
        else:
            tmp = [i for i in nltk.word_tokenize(''.join(line[1:]).lower().decode('utf-8')) if i.isalnum()]
        lastBody += tmp
    f.close()
    output.write(lastId + ',' + ' '.join(lastBody) + '\n')
    output.close()

def tokenizeBodiesBySentence(bodiesFileName,outputFileName):
    stop = set(stopwords.words('english'))
    f = open(bodiesFileName,'r')
    output = open(outputFileName, 'w')
    lastBody = []
    lastId = None
    for line in f.xreadlines():
        line = line.replace('\n','').split(",")
        bodyid = line[0]
        if bodyid.isdigit():
            if lastId:
                lastBody =  [[i for i in l if i.isalnum()] for l in lastBody]
                output.write(lastId + ',' + u'\t'.join([' '.join(i) for i in lastBody if sum([len(x) for x in i]) > 0]).encode('utf-8') + '\n')
            lastBody = []
            lastId = bodyid
            sents = [nltk.word_tokenize(sent.decode('utf-8')) for sent in ','.join(line[1:]).lower().split('.')]
        else:
            sents = [nltk.word_tokenize(sent.decode('utf-8')) for sent in ''.join(line[1:]).lower().split('.')]
        lastBody += sents
    f.close()
    lastBody =  [[i for i in l if i.isalnum()] for l in lastBody]
    output.write(lastId + ',' + u'\t'.join([' '.join(i) for i in lastBody if sum([len(x) for x in i]) > 0]).encode('utf-8') + '\n')
    output.close()


def classification(stanceFileName, unrelatedFileName, agreeFileName, disagreeFileName, discussFileName):
    f_unrel = open(unrelatedFileName,'w')
    f_agree = open(agreeFileName,'w')
    f_disagree = open(disagreeFileName,'w')
    f_discuss = open(discussFileName,'w')
    f = open(stanceFileName,'r')
    for line in f.xreadlines():
        c = line.split(',')[-1].replace('\n','')
        if c == 'unrelated':
            f_unrel.write(line)
        elif c == 'agree':
            f_agree.write(line)
        elif c == 'disagree':
            f_disagree.write(line)
        elif c == 'discuss':
            f_discuss.write(line)
    f.close()
    f_unrel.close()
    f_agree.close()
    f_disagree.close()
    f_discuss.close()


if __name__ == '__main__':
    tokenizeBodiesBySentence('train_bodies_cleaned.csv','train_bodies_tokenized_task2_sentence.csv')
    # cleanStances('train_stances_cleaned.csv','train_stances_tokenized_task2.csv')
    cleanBodies('train_bodies_cleaned.csv','train_bodies_tokenized_task2.csv')
    # classification('train_stances_tokenized_task2.csv','unrelated_stances.csv','agree_stances.csv','disagree_stances.csv','discuss_stances.csv')