#!/usr/bin/python
import pickle
import math
import sys
import csv
import numpy as np
from sklearn import svm
from feature import *
from collections import Counter

def load_dataSet(fileName, isTest = False):
	features = []
	labels = []
	ids = []
	feature = Feature()
	lines = (open(fileName, 'r')).readlines()
	attributeLine = True  # first line of the file is the attribute names 
	for line in lines:
		if attributeLine:
			attributeLine = False
			continue
		bodyId, headline, body, label = line.split(',')
		headline = headline.split(' ')
		body = body.split(' ')
		f_bm25 = feature.BM25(headline, bodyId, body)
		f_indri = feature.Indri(headline, bodyId, body)
		f_cosSim = feature.cosSim(headline, bodyId, body)

		label = 0 if label.startswith('un') else 1
		labels.append(label)
		features.append([f_bm25, f_indri, f_cosSim])
		ids.append(bodyId)

		assert(len(labels) == len(features))

	if isTest:
		return np.array(labels), np.array(features), ids
	return np.array(labels), np.array(features)

def save_Result(prediction):
    print 'Saving prediction result...'                         
    infile = open('svm_Prediction.csv', 'w')
    lines = csv.writer(infile)
    lines.writerow(['testId', 'predict_Label'])
    index = 1
    for item in prediction:
        lines.writerow([index, item])
        index += 1


def svmClassify(trainFeature, trainLabel, testFeature, c, k):
	print "Training SVM classifier..."
	# default: C = 1.0, k = 'rbf (can try 'linear', 'poly', 'rbf', 'sigmoid', 'precomputed')
	clf = svm.SVC(C = c, kernel = 'rbf')
	clf.fit(trainFeature, trainLabel)
	predictLabel = clf.predict(testFeature)
	save_Result(predictLabel)
	return predictLabel


def classification():
	trainLabel, trainFeature = load_dataSet('trainingSet.csv')
	testLabel, testFeature, ids = load_dataSet('testSet.csv', True)
	result = svmClassify(trainFeature, trainLabel, testFeature, 5, 'rbf')

	error = 0
	errorFile = open("error_id.txt", 'w')
	num_test = testFeature.shape[0]	
	for i in xrange(num_test):
		if result[i] != testLabel[i]:
			error += 1
			errorFile.write("%s\n" % ids[i])

	accuracy = (num_test - error) * 100.0 / num_test
	print "#TestCase = %d, Accuracy = %.2f%%" % (num_test, accuracy)
	print "#ErrorCase = %d, corresponding IDs saved to file 'error_id.txt'" % error

if __name__ == '__main__':
	classification()
