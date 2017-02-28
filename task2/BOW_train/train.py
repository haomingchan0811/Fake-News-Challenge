import random
from index import *
from sklearn.feature_extraction.text import HashingVectorizer
import numpy as np
import xgboost as xgb
from sklearn.metrics import roc_auc_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score


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


def loadTrainingSet(trainingFile,posLabel):
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
        if label == posLabel:
            y.append(1)
        else:
            y.append(0)

    X_title = hv.fit_transform(titles)
    X_body = hv.fit_transform(bodies)
    X = np.concatenate((X_title.todense(),X_body.todense()), axis = 1)
    return X,y,hv

def loadTestSet(testFile,hv,posLabel):
    index = Index.load('index_task2')
    titles = []
    bodies = []
    y = []
    f = open(testFile,'r')
    for line in f.xreadlines():
        line = line.replace('\n','').split(',')
        title = line[0]
        bodyId = line[1]
        label = line[2]
        titles.append(title)
        bodies.append(' '.join(index.getBody(bodyId)))
        if label == posLabel:
            y.append(1)
        else:
            y.append(0)
    X_title = hv.fit_transform(titles)
    X_body = hv.fit_transform(bodies)
    X = np.concatenate((X_title.todense(),X_body.todense()), axis = 1)
    return X,y

def xgbTrain(X_train,y_train,X_test,y_test,posLabel):
    dtrain = xgb.DMatrix(X_train, label = y_train)
    dtest = xgb.DMatrix(X_test)
    max_depth = 10
    param = {'max_depth': max_depth, 'eta':1, 'silent':1, 'objective':'binary:logistic' }
    num_round = 10
    bst = xgb.train(param, dtrain, num_round)
    preds = bst.predict(dtest)
    f = open('output_'+posLabel,'w')
    for prob in preds:
        f.write(str(prob) + '\n');
    f.close()
    print 'max_depth: ' + str(max_depth)
    print 'auc score: ' + str(roc_auc_score(y_test,preds))
    tmp = list(preds)
    for threshold in [0.2,0.3,0.4,0.5]:
        preds = [1 if i > threshold else 0 for i in tmp]
        print 'threshold:', threshold
        print 'F1 score:', f1_score(y_test, preds)
        print 'Recall:', recall_score(y_test, preds)
        print 'Precision:', precision_score(y_test, preds)

def getResult(agree,discuss,disagree,test):
    labels = []
    f_agree = open(agree,'r')
    f_discuss = open(discuss,'r')
    f_disagree = open(disagree,'r')
    f_test = open(test,'r')
    for line in f_test.readlines():
        labels.append(line.split(',')[2])
    f_test.close()
    pass
    # to be implemented


if __name__ == '__main__':
    # createTrainingSet('../agree_stances.csv','../disagree_stances.csv','../discuss_stances.csv')
    
    X_train,y_train,hv = loadTrainingSet('training.csv','disagree') 
    X_test,y_test = loadTestSet('test.csv',hv,'disagree')
    xgbTrain(X_train,y_train,X_test,y_test,'disagree')

    # getResult('output_agree','output_discuss','output_disagree','test.csv')
