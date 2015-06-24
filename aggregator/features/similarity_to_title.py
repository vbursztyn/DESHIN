# Must be compliant to feature definition (TO-DO: convert from a Function to a proper Interface).
# For one single Article, given a certain criteria, returns a weighted and ordered list of sentences.
# If that criteria's logics depend on outter parameter(s), it or they must be passed as argument(s).
# The way it's currently architectured, Aggregator will pass a fixed set of arguments to all feature calls.
# So, currently, all features must have equal and fixed prototypes (TO-DO: improve Aggregator-Feature architecture,
# considering different argument needs).


import nltk

import re

import string

from math import sqrt


stopwords = nltk.corpus.stopwords.words("portuguese")

stemmer = nltk.stem.RSLPStemmer()


def removePunctuation(text):
	regex = re.compile("[%s]" % re.escape(string.punctuation))
	return regex.sub("", text)


def removeStopwords(text):
	textWords = list()
	for word in nltk.tokenize.word_tokenize(text):
		textWords.append(word.lower())

	for stopword in stopwords:
		textWords = filter(lambda w: w != stopword, textWords)

	return textWords


def applyStemmer(textWords):
	stemmedWords = list()
	for word in textWords:
		stemmedWords.append(stemmer.stem(word))

	return stemmedWords


def calculateCosines(vectorA, vectorB):
	intersection = 0
	uniqueWordsA = set(vectorA)
	for wordA in uniqueWordsA:
		if wordA in vectorB:
			intersection = intersection + vectorB.count(wordA)

	d = (norm(vectorA) * norm(vectorB))
	if not d:
		return 0.0
	return float(intersection) / d


def norm(wordsVector):
	norm = 0
	for word in wordsVector:
		count = wordsVector.count(word)
		norm = norm + count * count
	return sqrt(norm)


def similarityToTitle(article, titles):
	titles = titles.values()
	
	weightedSentences = list()

	for sentence in article:
		score = 0
		sentence = removePunctuation(sentence)
		sentenceWords = removeStopwords(sentence)
		sentenceWords = applyStemmer(sentenceWords)

		for title in titles:
			title = removePunctuation(title)
			titleWords = removeStopwords(title)
			titleWords = applyStemmer(titleWords)
			score = score + calculateCosines(sentenceWords, titleWords)

		score = score / len(titles)
		weightedSentence = { "content" : sentence, "score" : score }
		weightedSentences.append(weightedSentence)

	orderedSentences = sorted(weightedSentences, key=lambda k: k["score"], reverse=True)
	return orderedSentences


