import pickle
import math
from statistics import *
from collections import Counter



if __name__ == '__main__':
	filename = sys.argv[1]
	f = open(filename, 'r')
	feature = Feature()
	lines = f.readlines()
	threshold = [20, 0.001, 0.1]
	numFeatures = 3
	for line in lines:
		line = line.split(',')
        title = line[0]
        title = title.split(' ')
        bodyId = line[1]
        related = line[2]
		#Todo: get body from bodyId
		body = getBody(bodyId)
		features = []
		features[0] = feature.BM25(title, bodyId, body)
		features[1] = feature.Indri(title, bodyId, body)
		features[2] = feature.cosSim(title, bodyId, body)
		count = 0
		for i in range(numFeatures):
			if features[i] >= threshold[i]:
				count++

		if (count > (numFeatures >> 1)):
			print "Prediction: Related.\n"
		else:
			print "Prediction: Unrelated.\n"

		print "Standard realtion: " + related + "\n"
		print "************"

