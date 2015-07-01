from globals import FEATURES_MIN_THRESHOLD

from features.less_frequent_actors import lessFrequentActors

from features.more_frequent_actors import moreFrequentActors

from features.order_in_text import orderInText

from features.similarity_to_title import similarityToTitle

from features.verbs_and_nouns import verbsAndNouns

from google.apputils import app

import gflags

from ortools.algorithms import pywrapknapsack_solver

FLAGS = gflags.FLAGS


DEFAULT_FEATURES = { "base_feature" : similarityToTitle,
					"tuning_features" : [ orderInText, moreFrequentActors, \
										lessFrequentActors, verbsAndNouns ] } # To be moved to elsewhere.


DEFAULT_WEIGHTS = { "base_feature" : 1.0,
					"tuning_features" : [ 0.2, 0.6, 0.4, 0.3 ] } # To be merged to DEFAULT_FEATURES (as dictionaries).


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
		self.weightedScores = dict()
	

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
				if sentence["content"] in self.weightedScores:
					self.weightedScores[sentence["content"]] += sentence["score"]
				else:
					self.weightedScores[sentence["content"]] = sentence["score"]

		for article in self.articlesResults["tuning_features"]:
			for feature in self.articlesResults["tuning_features"][article]:
				weight = DEFAULT_WEIGHTS["tuning_features"][feature]
				for i, sentence in enumerate(self.articlesResults["tuning_features"][article][feature]):
					sentence["score"] = sentence["score"] * weight
					if sentence["content"] in self.weightedScores:
						self.weightedScores[sentence["content"]] += sentence["score"]
					else:
						self.weightedScores[sentence["content"]] = sentence["score"]

		weightedScoreAux = []
		for content, score in self.weightedScores.iteritems():
			weightedScoreAux.append( {"content": content, "score": score, "length": len(content)} )

		self.weightedScores = sorted(weightedScoreAux, key=lambda k: k["score"], reverse=True)


	def runKnapsack(self):
		# Create the solver.
		solver = pywrapknapsack_solver.KnapsackSolver(pywrapknapsack_solver.KnapsackSolver.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'test')

		idealSummarySize = 0

		for sentence in self.summary:
			idealSummarySize += len(sentence)

		# Transforme real scores into integer profits
		profits = [ long(x["score"] * pow(10,6)) for x in self.weightedScores]
		weights = [[x["length"] for x in self.weightedScores]]
		capacities = [idealSummarySize]

		solver.Init(profits, weights, capacities)
		solver.Solve()

		for i in xrange(len(profits)):
			if solver.BestSolutionContains(i):
				self.subjectResult.append(self.weightedScores[i]["content"])


	def recoverReadingOrder(self):
		reorderedSentences = list()

		for sentence in self.subjectResult:
			level = -1
			for article in self.articles:
				if sentence in self.articles[article]:
					level = self.articles[article].index(sentence)
					break
			if level == -1:
				raise Exception("Broken Aggregator.articles - unable to locate sentence")
			reorderedSentence = { "content" : sentence, "level" : level }
			reorderedSentences.append(reorderedSentence)
		
		reorderedSentences = sorted(reorderedSentences, key=lambda k: k["level"])

		self.subjectResult = [ sentence["content"] for sentence in reorderedSentences ]


	def run(self):
		if not self.features or not self.summary:
			raise Exception("Aggregator misscalled - set it first")
		
		self.runForEachArticle() # Map/Reduce analogy: like "Map", as it creates Article-Feature pairs.
		self.applyThreshold()
		self.applyFeaturesWeights()
		self.runKnapsack() # Map/Reduce analogy: like "Reduce", where we actually aggregate results for the Subject.
		self.recoverReadingOrder()


	def getResultingSummary(self):
		if not self.subjectResult or not len(self.subjectResult):
			raise Exception("Nonexistent or null result - be sure Aggregator was properly called")
		return self.subjectResult


	def getIdealSummary(self):
		if not self.summary:
			raise Exception("Nonexistent summary - be sure subject was properly set")
		return self.summary

