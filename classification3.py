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
	miss1 = 0
	miss2 = 0
	total1 = 0
	total2 = 0
	total = 0
	pn = 0
	np = 0
	nn = 0
	pp = 0
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
		if related.startswith('un'):
			total1 += 1
		else:
			total2 += 1
		for i in range(numFeatures):
			if features[i] >= threshold[i]:
				count += 1
		if (count >= (numFeatures >> 1)):
			print "Prediction: Related."
			if related.startswith('un'):
				for j in features:
					print j
				miss1 += 1
				miss += 1
				pn += 1
			else:
				pp += 1
			#continue
		else:
			print "Prediction: Unrelated."
			if not related.startswith('un'):
				miss2 += 1
				miss += 1
				np += 1
				for j in features:
					print j
			else:
				nn += 1
		print "Standard realtion: " + related
		print "************"
		
	print "PP " + str(pp)
	print "NN " + str(nn)
	print "PN " + str(pn)
	print "NP " + str(np)
	p = float(pp) / (pp + pn)
	r = float(pp) / (pp + np)
	f1 = 2.0 * p * r / (p + r)
	print "Precison: " + str(p)
	print "Recall: " + str(r)
	print "F1: " + str(f1)
 
	
