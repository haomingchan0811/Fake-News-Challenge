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
	for line in lines:
		line = line.split(',')
		title = line[1]
		title = title.split(' ')
		bodyId = line[0]
		related = line[3]
		body = line[2]
		#body = s.getBody(bodyId)
		body = body.split(' ')
		features[0] = feature.BM25(title, bodyId, body)
		features[1] = feature.Indri(title, bodyId, body)
		features[2] = feature.cosSim(title, bodyId, body)
		count = 0
		for i in range(numFeatures):
			if features[i] >= threshold[i]:
				count += 1
		if (count > (numFeatures >> 1)):
			print "Prediction: Related.\n"
		else:
			print "Prediction: Unrelated.\n"
			if not related.startswith('un'):
				miss += 1
		print "Standard realtion: " + related + "\n"
		print "************"
	print miss

