class Configurator():

	
	def __init__(self):
		self.aggregator = None
		self.evaluator = None

		self.collectionId = None
		self.subjects = None
		self.results = dict()


	def setAggregator(self, aggregator):
		self.aggregator = aggregator


	def setEvaluator(self, evaluator):
		self.evaluator = evaluator


	def setCollection(self, collectionId):
		self.collectionId = collectionId
		self.results = dict()


	def setSubjects(self, subjects):
		self.subjects = subjects


	def getResults(self):
		return self.results


	def run(self):

		self.results["all"] = []
		self.results["best"] = dict()

		# Base feature only:
		# baseConfigurations = [1.0]
		# tuningConfigurations = []
		# tuningConfigurations.append( ("orderInText", [0.0]) )
		# tuningConfigurations.append( ("moreFrequentActors", [0.0]) )
		# tuningConfigurations.append( ("lessFrequentActors", [0.0]) )
		# tuningConfigurations.append( ("verbsAndNouns", [0.0]) )
			
		baseConfigurations = [0.5, 0.7]
		tuningConfigurations = []
		tuningConfigurations.append( ("orderInText", [0.1, 0.3, 0.5, 0.7, 0.9]) )
		tuningConfigurations.append( ("moreFrequentActors", [0.1, 0.3, 0.5, 0.7, 0.9]) )
		tuningConfigurations.append( ("lessFrequentActors", [0.1, 0.3, 0.5, 0.7, 0.9]))
		tuningConfigurations.append( ("verbsAndNouns", [0.1, 0.3, 0.5, 0.7, 0.9]))

		bestWeights = None
		bestEvaluation = 0.0

		print "\n############################"
		print "# Running Configurator for: " + self.collectionId
		print "############################"

		for baseFeatureWeight in baseConfigurations:
			for tuningFeatureN1Weight in tuningConfigurations[0][1]:
				for tuningFeatureN2Weight in tuningConfigurations[1][1]:
					for tuningFeatureN3Weight in tuningConfigurations[2][1]:
						for tuningFeatureN4Weight in tuningConfigurations[3][1]:

							weights = { "base_feature" : baseFeatureWeight,
										"tuning_features" : [ tuningFeatureN1Weight,
															  tuningFeatureN2Weight,
															  tuningFeatureN3Weight, 
															  tuningFeatureN4Weight ] }
							
							print "Testing configuration: " + str(weights)

							self.aggregator.setWeights(weights) # (TO-DO: actually search for optimal values in n-weights space.)

							evaluations = list()

							for subject in self.subjects:
								self.aggregator.setSubject(self.subjects[subject])
								self.aggregator.run()
								resultingSummary = self.aggregator.getResultingSummary()
								idealSummary = self.aggregator.getIdealSummary()
								
								self.evaluator.setTest(resultingSummary, idealSummary)
								evaluations.append( self.evaluator.run() )

							print "Resulting evaluations: " + str(evaluations)

							meanEvaluation =  sum(evaluations) / float(len(evaluations))

							print "So that mean evaluation is: " + str(meanEvaluation) + "\n"

							localResult = dict()
							localResult["weights"] = weights
							localResult["evaluation"] = meanEvaluation

							self.results["all"].append(localResult)

							if meanEvaluation > bestEvaluation:
								bestWeights = weights
								bestEvaluation = meanEvaluation

		self.results["best"]["weights"] = bestWeights
		self.results["best"]["evaluation"] = bestEvaluation

