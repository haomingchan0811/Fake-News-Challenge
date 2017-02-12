import nltk
from nltk.corpus import stopwords
def cleanStances(stancesFileName,outputFileName):
    f = open(stancesFileName,'r')
    output = open(outputFileName, 'w')
    for line in f.xreadlines():
        line = line.split(",")
        headline = ','.join(line[:-2])
        stop = set(stopwords.words('english'))
        newHeadline = [i for i in nltk.word_tokenize(headline.lower()) if i not in stop and i.isalpha()]
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
        line = line.split(",")
        bodyid = line[0]
        if bodyid.isdigit():
            if lastId:
                output.write(lastId + ',' + ' '.join(lastBody) + '\n')
            lastBody = []
            lastId = bodyid
            tmp = [i for i in ','.join(line[1:]).lower().split(' ') if i not in stop and i.isalpha()]
        else:
            tmp = [i for i in ''.join(line).lower().split(' ') if i not in stop and i.isalpha()]
        lastBody += tmp
            
        
        
    f.close()
    output.close()


if __name__ == '__main__':
    # cleanStances('train_stances_cleaned.csv','train_stances_tokenized.csv')
    cleanBodies('train_bodies.csv','train_bodies_tokenized.csv')