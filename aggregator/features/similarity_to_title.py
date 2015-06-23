# Must be compliant to feature definition (TO-DO: convert from a Function to a proper Interface).
# For one single Article, given a certain criteria, returns a weighted and ordered list of sentences.
# If that criteria's logics depend on outter parameter(s), it or they must be passed as argument(s).
# The way it's currently architectured, Aggregator will pass a fixed set of arguments to all feature calls.
# So, currently, all features must have equal and fixed prototypes (TO-DO: improve Aggregator-Feature architecture,
# considering different argument needs).

def similarityToTitle(article, titles):
	return "List of sentences after similarityToTitle - " + article[0][:10] + "(...)"

