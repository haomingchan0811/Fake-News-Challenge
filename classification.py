import pickle
import math
import sys
from index import *
from feature import *
from collections import Counter



if __name__ == '__main__':
	filename = sys.argv[1]
	f = open(filename, 'r')
	s = Index.load('index')
	feature = Feature()
	lines = f.readlines()
	threshold = [20, 0.001, 0.1]
	features = [0,0,0]
	numFeatures = 3
	miss = 0
	total = 0
	for line in lines:
		total += 1
		line = line.split(',')
		title = line[0]
		title = title.split(' ')
		bodyId = line[1]
		related = line[2]
		body = s.getBody(bodyId)
		features[0] = feature.BM25(title, bodyId, body)
		features[1] = feature.Indri(title, bodyId, body)
		features[2] = feature.cosSim(title, bodyId, body)
		count = 0
		for i in range(numFeatures):
			if features[i] >= threshold[i]:
				count += 1
		if (count >= (numFeatures >> 1)):
			print "Prediction: Related.\n"
			#continue
		else:
			print "Prediction: Unrelated."
			if not related.startswith('un'):
				miss += 1
				for j in features:
					print j
		print "Standard realtion: " + related
		print "************"
		
	print "#Miss " + str(miss)
	print "#Total " + str(total)
	precision = 1 - float(miss) / total
	print "Precision: " + str(precision)

