#!/usr/bin/python
import sys
import pickle
import math
import csv

def readFile(fileName):
	id2text = {}
	with open(fileName, 'r') as f:
		for line in f.readlines():
			content = line.split(',')
			bodyId, text = content[0].strip(), content[1].strip()
			id2text[bodyId] = text 

	return id2text

def linker(id2body, fileName):
	trainingSet = []
	with open(fileName, 'r') as f:
		for line in f.readlines():
			headline, bodyId, label = line.strip().split(',')
			try:
				body = id2body[bodyId]
				trainingSet.append([bodyId, headline, body, label])
			except:
				print "KeyError: ", bodyId

	with open('trainingSet.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerow(['BodyId', 'Headline', 'Body', 'Label'])
		for dataPoint in trainingSet:
			writer.writerow(dataPoint)

	# return trainingSet


if __name__ == '__main__':
	print "indexing body..."
	id2body = readFile("train_bodies_tokenized.csv")
	print "combing body and headline..." 
	linker(id2body, "train_stances_tokenized.csv")
	