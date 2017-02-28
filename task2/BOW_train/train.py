import random
from index import *
from sklearn.feature_extraction.text import HashingVectorizer
def createTrainingSet(agree,disagree,discuss):
    l = []
    for fileName in [agree,disagree,discuss]:
        f = open(fileName,'r')
        for line in f.xreadlines():
            l.append(line)
        f.close()
    random.shuffle(l)
    train = l[:int(0.8 * len(l))]
    test = l[int(0.8 * len(l)):]
    f = open('training.csv','w')
    for item in train:
        f.write(item)
    f.close()
    f = open('test.csv','w')
    for item in test:
        f.write(item)
    f.close()


def loadTrainingSet(trainingFile):
    # return matrix bag of words
    index = Index.load('index_task2')
    hv = HashingVectorizer(n_features=1000)
    titles = []
    bodies = []
    y = []
    f = open(trainingFile,'r')
    for line in f.xreadlines():
        line = line.replace('\n','').split(',')
        title = line[0]
        bodyId = line[1]
        label = line[2]
        titles.append(title)
        bodies.append(' '.join(index.getBody(bodyId)))
        if label == 'agree':
            y.append(1)
        if label == 'disagree':
            y.append(2)
        if label == 'discuss':
            y.append(0)

    X_title = hv.fit_transform(titles)
    X_body = hv.fit_transform(bodies)
    return X_title,X_body,y,hv





if __name__ == '__main__':
    # createTrainingSet('../agree_stances.csv','../disagree_stances.csv','../discuss_stances.csv')
    X_title,X_body,y,hv = loadTrainingSet('training.csv')