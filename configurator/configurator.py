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


	def setSubjects(self, subjects):
		self.subjects = subjects


	def run(self):

		self.results["all"] = []
		self.results["best"] = dict()

		base_configurations = [1.0, 0.95]
		tuning_configurations = []
		tuning_configurations.append( ("orderInText", [0.0]) )
		tuning_configurations.append( ("moreFrequentActors", [0.2]) )
		tuning_configurations.append( ("lessFrequentActors", [0.2]) )
		tuning_configurations.append( ("verbsAndNouns", [0.2, 0.3]) )

		'''
		base_configurations = [1.0, 0.95, 0.9, 0.85, 0.8]
		tuning_configurations = []
		tuning_configurations.append( ("orderInText", [0.0, 0.1, 0.15, 0.2, 0.25, 0.3]) )
		tuning_configurations.append( ("moreFrequentActors", [0.2, 0.3, 0.4, 0.4, 0.6, 0.7]) )
		tuning_configurations.append( ("lessFrequentActors", [0.2, 0.3, 0.4, 0.4, 0.6, 0.7]) )
		tuning_configurations.append( ("verbsAndNouns", [0.2, 0.3, 0.4, 0.4, 0.6, 0.7]) )
		'''

		best_wheights = None
		best_evaluation = 0

		print "\n############################"
		print "# Running Configurator for: " + self.collectionId
		print "############################"

		for base_feature_wheight in base_configurations:
			for tuning_feature_0_wheight in tuning_configurations[0][1]:
				for tuning_feature_1_wheight in tuning_configurations[1][1]:
					for tuning_feature_2_wheight in tuning_configurations[2][1]:
						for tuning_feature_3_wheight in tuning_configurations[3][1]:

							weights = { "base_feature" : base_feature_wheight,
										"tuning_features" : [ tuning_feature_0_wheight,
															  tuning_feature_1_wheight,
															  tuning_feature_2_wheight, 
															  tuning_feature_3_wheight ] } # To be merged to DEFAULT_FEATURES (as dictionaries).
							
							self.aggregator.setWeights(weights=weights) # (TO-DO: actually search for optimal values in n-weights space.)

							evaluations = list()

							for subject in self.subjects:
								self.aggregator.setSubject(self.subjects[subject])
								self.aggregator.run()
								resultingSummary = self.aggregator.getResultingSummary()
								idealSummary = self.aggregator.getIdealSummary()
								#print "\nResulting summary:\n" + str(resultingSummary) + "\n"
								#print "\nIdeal summary:\n" + str(idealSummary) + "\n"
								
								self.evaluator.setTest(resultingSummary, idealSummary)
								evaluations.append( self.evaluator.run() )

							mean_evaluation =  sum(evaluations) / float(len(evaluations))

							local_result = dict()
							local_result["weights"] = weights
							local_result["evaluation"] = mean_evaluation

							self.results["all"].append(local_result)

							if mean_evaluation > best_evaluation:
								best_wheights = weights
								best_evaluation = mean_evaluation

		self.results["best"]["weights"] = best_wheights
		self.results["best"]["evaluation"] = best_evaluation

