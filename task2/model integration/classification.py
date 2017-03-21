#!/usr/bin/python
import pickle
import math
import sys
import csv
import numpy as np
from sklearn import svm
from collections import Counter

labelDict = {"discuss": 0, "agree":1, "disagree":2}

def load_dataSet(f_clfProb, f_ruleBased):
	features = []
	labels = []
	lines_clf = (open(f_clfProb, 'r')).readlines()
	lines_rule = (open(f_ruleBased, 'r')).readlines()

	for l1, l2 in zip(lines_clf, lines_rule):
		clfProb = map(lambda x: float(x), l1.strip().split(' '))
		[ruleBased, label] = l2.strip().split(' ')
		clfProb.append(float(ruleBased))
		features.append(clfProb)
		labels.append(labelDict[label])

	return np.array(labels), np.array(features)

def save_Result(prediction):
    print 'Saving prediction result...'                         
    infile = open('svm_Prediction.csv', 'w')
    lines = csv.writer(infile)
    index = 0
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
	trainLabel, trainFeature = load_dataSet('train_3scores', 'train_gtree.csv')
	testLabel, testFeature = load_dataSet('test_3scores', 'test_gtree.csv')	
	result = svmClassify(trainFeature, trainLabel, testFeature, 5, 'rbf')

	error = 0
	num_test = testFeature.shape[0]	
	[falsePositive, falseNegative, truePositive, trueNegative] = [0] * 4
	for i in xrange(num_test):
		if result[i] != testLabel[i]:
			if result[i] == 1:
				falsePositive += 1
			else:
				falseNegative += 1 
			error += 1
		else:
			if result[i] == 1:
				truePositive += 1
			else:
				trueNegative += 1 

	accuracy = (num_test - error) * 100.0 / num_test
	print "#True Positive = %d, #False Positive = %d" % (truePositive, falsePositive)
	print "#True Negative = %d, #False Negative = %d" % (trueNegative, falseNegative)
	print "#TestCase = %d, #ErrorCase = %d, corresponding IDs saved to file 'error_id.txt'" % (num_test, error)
	precision = (truePositive * 100.0 / (truePositive + falsePositive))
	recall = (truePositive * 100.0 / (truePositive + falseNegative))
	f1 = (2 * (precision * recall) / (precision + recall))
	print "Accuracy = %.2f%%, Precision = %.2f%%, Recall = %.2f%%, F1 Score = %.2f%%" % (accuracy, precision, recall, f1)

if __name__ == '__main__':
	classification()