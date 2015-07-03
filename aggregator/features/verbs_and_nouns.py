# Must be compliant to feature definition (TO-DO: convert from a Function to a proper Interface).
# For one single article, given a certain criteria, returns a weighted and ordered list of sentences.
# If that criteria's logics depend on outter parameter(s), it(they) must be passed as argument(s).
# The way it's currently architectured, Aggregator will pass a fixed set of arguments to all feature calls.
# So, currently, all features must have equal and fixed prototypes (TO-DO: improve Aggregator-Feature architecture,
# considering different argument needs).


from aggregator.pos_tagger.global_tagger import tagger

import pickle

import nltk


stopwords = nltk.corpus.stopwords.words("portuguese")


def removeStopwords(text):
	textWords = list()
	for word in nltk.tokenize.word_tokenize(text):
		textWords.append(word)

	for stopword in stopwords:
		textWords = filter(lambda w: w != stopword, textWords)

	return textWords


def verbsAndNouns(article, titles):
	verbsOrNouns = [ "V", "N" ]

	weightedSentences = list()

	maxScore = 0.0

	for sentence in article:
		score = 0.0
		taggedWords = tagger.tag(removeStopwords(sentence))
		for pair in taggedWords:
			if pair[1] in verbsOrNouns:
				score = score + 1
		
		weightedSentence = { "content" : sentence, "score" : score }
		weightedSentences.append(weightedSentence)
		if score > maxScore:
			maxScore = score

	orderedSentences = sorted(weightedSentences, key=lambda k: k["score"], reverse=True)
	orderedSentences = [ { "content" : sentence["content"], "score" : (sentence["score"] / maxScore) } \
	 for sentence in orderedSentences ]
	return orderedSentences

