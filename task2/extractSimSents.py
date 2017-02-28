import gensim, nltk
import math
import numpy as np
from index import *
from nltk.corpus import stopwords

stopwords = set(stopwords.words('english'))
index = Index.load('index_task2')

# Load Google's pre-trained Word2Vec model.
model = gensim.models.Word2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
print "word2vec model loading complete..."

vocab = model.vocab.keys()
print "vocabulary size = ", len(vocab)

"""
Select the top K similar sentences in the body to the headline
@param headline string of tokens seperated by blank
@param bodyId bodyID for this headline
@param label label of this pair of headline and body
@param k the number of most similar sentences to extract
@return a list of top 
"""
def selectSents(headline, bodyId, label, k = 3):
	# f = open('train_stances_tokenized_task2.csv', 'r')
	# firstLine = True
	# for line in f.readlines():
	# 	if firstLine:
	# 		firstLine = False
	# 		continue
	scores = {}  # scores for each sentence in the body comparing to the headline

	# [headline, bodyId, label] = line.strip().split(',')
	headline = [token for token in headline.split(' ')]
	body = index.getBodySent(bodyId)

	for sentence in body:
		str_sent = ' '.join(sentence)
		scores[str_sent] = sent_similarity(headline, sentence)

	top_sents = sorted(scores.iteritems(), key = lambda x:x[1], reverse = True)
	print top_sents

	return top_sents[:3]


"""
Compute the semantic similarity between two sentences
"""
def sent_similarity(s1, s2):
	s1_vec = vectorize(s1)
	s2_vec = vectorize(s2)
	# print s1_vec
	# print s2_vec
	return cosSim(s1_vec, s2_vec)


"""
Turn a list of tokens into a sentence vector
"""
def vectorize(tokens):
	num_tokens = 0
	# initialize sentence vector
	sent_vec = np.zeros((300,))  

	for token in tokens:
		if token not in stopwords:
			try:
				sent_vec += model[token]
				num_tokens += 1
			except KeyError, e:
				"word '%s' not in model, discard automatically..." % token

	if num_tokens != 0:
		sent_vec /= num_tokens

	return sent_vec

"""
Compute the cosine similarity between two vectors.
"""
def cosSim(vec1, vec2):
	if len(vec1) != len(vec2):
		print "dimension doesn't match"
		return None
	
	[dotProduct, v1_square, v2_square] = [0.0] * 3

	for v1, v2 in zip(vec1, vec2):
		dotProduct += v1 * v2
		v1_square += v1 ** 2
		v2_square += v2 ** 2

	normalizer = math.sqrt(v1_square * v2_square)      
	if normalizer == 0.0:
		return None
	else:
		return dotProduct / normalizer


if __name__ == '__main__':
	headline = "hundreds of palestinians flee floods in gaza as israel opens dams"
	bodyId = 158
	selectSents(headline, bodyId, 'agree')