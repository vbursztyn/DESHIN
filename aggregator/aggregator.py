from globals import FEATURES_MIN_THRESHOLD

from features.similarity_to_title import similarityToTitle
from features.order_in_text import orderInText


DEFAULT_FEATURES = { "base_feature" : similarityToTitle,
					"tuning_features" : [ orderInText ] } # To be moved to elsewhere.


DEFAULT_WEIGHTS = { "base_feature" : 1.0,
					"tuning_features" : [ 0.0 ] } # To be merged to DEFAULT_FEATURES (as dictionaries).


class Aggregator():


	def __init__(self):
		self.features = None
		self.weights = None

		self.articlesResults = None
		self.subjectResult = None

		self.summary = None
		self.titles = None
		self.articles = None


	def loadFeatures(self, features=DEFAULT_FEATURES):
		self.features = features
	

	def setWeights(self, weights=DEFAULT_WEIGHTS):
		self.weights = weights


	def setSubject(self, subject):
		keys = ["articles_sentences", "articles_titles", "summary_sentences"]
		if not any(subject[key] for key in keys):
			raise KeyError("Malformed Subject object - missing one or more keys")
		self.summary = subject["summary_sentences"]
		self.titles = dict( filter(lambda item: item[1] is not None, subject["articles_titles"].items()) )
		self.articles = subject["articles_sentences"]
		self.articlesResults = dict()
		self.subjectResult = list()
	

	# For each Article about this Subject, computes base feature,
	# and all optional features, then stores scored sentences in
	# articlesResults, before we approach the problem with Knapsack.
	def runForEachArticle(self):
		self.articlesResults["base_feature"] = dict()
		self.articlesResults["tuning_features"] = dict()
		for article in self.articles:
			self.articlesResults["base_feature"][article] = self.features["base_feature"]( self.articles[article], self.titles )
			self.articlesResults["tuning_features"][article] = dict()
			for i, optionalFeature in enumerate(self.features["tuning_features"]):
				self.articlesResults["tuning_features"][article][i] = optionalFeature( self.articles[article], self.titles )


	def applyThreshold(self, minCut=FEATURES_MIN_THRESHOLD):
		keys = ["base_feature", "tuning_features"]
		if not any(self.articlesResults[key] for key in keys):
			raise KeyError("Threshold application misscalled - run features first")

		for article in self.articlesResults["base_feature"]:
			for i, sentence in enumerate(self.articlesResults["base_feature"][article]):
				if sentence["score"] < minCut:
					self.articlesResults["base_feature"][article].pop(i)

		for article in self.articlesResults["tuning_features"]:
			for feature in self.articlesResults["tuning_features"][article]:
				for i, sentence in enumerate(self.articlesResults["tuning_features"][article][feature]):
					if sentence["score"] < minCut:
						self.articlesResults["tuning_features"][article][feature].pop(i)


	def applyFeaturesWeights(self):
		keys = ["base_feature", "tuning_features"]
		if not any(self.articlesResults[key] for key in keys):
			raise KeyError("Weights application misscalled - run features first")

		weight = DEFAULT_WEIGHTS["base_feature"]
		for article in self.articlesResults["base_feature"]:
			for i, sentence in enumerate(self.articlesResults["base_feature"][article]):
				sentence["score"] = sentence["score"] * weight

		for article in self.articlesResults["tuning_features"]:
			for feature in self.articlesResults["tuning_features"][article]:
				weight = DEFAULT_WEIGHTS["tuning_features"][feature]
				for i, sentence in enumerate(self.articlesResults["tuning_features"][article][feature]):
					sentence["score"] = sentence["score"] * weight


	def runKnapsack(self):
		print "TO-DO: Consolidate all scored sentences using Knapsack:"
		# While knapsack is not yet implemented, a (really) dummy selection algorithm allows us
		# to move further onto the Evaluation class (TO-DO: actually implement Knapsack + selection logics).
		sackSize = len(self.summary)
		result = list()
		level = 0
		while len(result) < sackSize:
			for article in self.articlesResults["base_feature"]:
				result.append(self.articlesResults["base_feature"][article][level])
			level = level + 1

		for i in range(0, sackSize):
			self.subjectResult.append(result[i]["content"])


	def run(self):
		if not self.features or not self.summary:
			raise Exception("Aggregator misscalled - set it first")
		
		self.runForEachArticle() # Map/Reduce analogy: like "Map", as it creates Article-Feature pairs.
		self.applyThreshold()
		self.applyFeaturesWeights()
		self.runKnapsack() # Map/Reduce analogy: like "Reduce", where we actually aggregate results for the Subject.

