from features.similarity_to_title import similarityToTitle
from features.order_in_text import orderInText


DEFAULT_FEATURES = { "base_feature" : similarityToTitle,
					"tuning_features" : [ orderInText ] } # To be moved to elsewhere.


class Aggregator():


	def __init__(self):
		self.features = None
		self.articlesResults = None
		self.subjectResult = None

		self.summary = None
		self.titles = None
		self.articles = None


	def loadFeatures(self, features=DEFAULT_FEATURES):
		self.features = features


	def setSubject(self, subject):
		keys = ["articles_sentences", "articles_titles", "summary_sentences"]
		if not any(subject[key] for key in keys):
			raise KeyError("Malformed Subject object - missing one or more keys")
		self.summary = subject["summary_sentences"]
		self.titles = dict( filter(lambda item: item[1] is not None, subject["articles_titles"].items()) )
		self.articles = subject["articles_sentences"]
		self.articlesResults = dict()
	

	# For each Article about this Subject, computes base feature,
	# and all optional features, then stores scored sentences in
	# articlesResults, before we approach the problem with Knapsack.
	def runForEachArticle(self):
		self.articlesResults["base_feature"] = dict()
		self.articlesResults["tuning_features"] = dict()
		for article in self.articles:
			self.articlesResults["base_feature"][article] = self.features["base_feature"]( self.articles[article], self.titles )
			for optionalFeature in self.features["tuning_features"]:
				self.articlesResults["tuning_features"][article] = optionalFeature( self.articles[article], self.titles )


	def runKnapsack(self):
		print "TO-DO: Consolidate all scored sentences using Knapsack:"


	def run(self):
		if not self.features or not self.summary:
			raise Exception("Aggregator misscalled - set it first")
		
		self.runForEachArticle() # Map/Reduce analogy: like "Map", as it creates Article-Feature pairs.
		# self.applyThreshold()
		# self.applyFeaturesWeights()
		self.runKnapsack() # Map/Reduce analogy: like "Reduce", where we actually aggregate results for the Subject.

