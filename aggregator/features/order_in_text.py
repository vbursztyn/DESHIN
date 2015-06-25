# Must be compliant to feature definition (TO-DO: convert from a Function to a proper Interface).
# For one single article, given a certain criteria, returns a weighted and ordered list of sentences.
# If that criteria's logics depend on outter parameter(s), it(they) must be passed as argument(s).
# The way it's currently architectured, Aggregator will pass a fixed set of arguments to all feature calls.
# So, currently, all features must have equal and fixed prototypes (TO-DO: improve Aggregator-Feature architecture,
# considering different argument needs).


from math import fabs


def orderInText(article, titles):
	weightedSentences = list()
	numberOfSentences = len(article)
	middle = int(numberOfSentences / 2)
	for i, sentence in enumerate(article):
		score = fabs(i - middle) * 0.1
		weightedSentence = { "content" : sentence, "score" : score }
		weightedSentences.append(weightedSentence)
	orderedSentences = sorted(weightedSentences, key=lambda k: k["score"], reverse=True)
	return orderedSentences


