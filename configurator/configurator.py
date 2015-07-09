from aggregator.aggregator import Aggregator

from evaluator.evaluator import Evaluator

from joblib import Parallel, delayed 

import multiprocessing

# Static method for running and evaluating one weigth configuration
def runConfiguration(weights, subjects):
		print "Testing configuration: " + str(weights)

		aggregator = Aggregator()
		evaluator = Evaluator()
		aggregator.loadFeatures()
		aggregator.setWeights(weights) # (TO-DO: actually search for optimal values in n-weights space.)

		evaluations = list()

		for subject in subjects:
			aggregator.setSubject(subjects[subject])
			aggregator.run()
			resultingSummary = aggregator.getResultingSummary()
			idealSummary = aggregator.getIdealSummary()
			
			evaluator.setTest(resultingSummary, idealSummary)
			evaluations.append( evaluator.run() )

		print "Resulting evaluations: " + str(evaluations)

		meanEvaluation =  sum(evaluations) / float(len(evaluations))

		print "So that mean evaluation is: " + str(meanEvaluation) + "\n"

		localResult = dict()
		localResult["weights"] = weights
		localResult["evaluation"] = meanEvaluation

		return localResult

class Configurator():

	
	def __init__(self):
		self.collectionId = None
		self.subjects = None
		self.results = dict()

	def setCollection(self, collectionId):
		self.collectionId = collectionId
		self.results = dict()


	def setSubjects(self, subjects):
		self.subjects = subjects


	def getResults(self):
		return self.results

	def run(self):

		self.results["all"] = None
		self.results["best"] = dict()

		# Base feature only:
		baseConfigurations = [1.0]
		tuningConfigurations = []
		tuningConfigurations.append( ("orderInText", [0.0, 0.1]) )
		tuningConfigurations.append( ("moreFrequentActors", [0.0, 0.1]) )
		tuningConfigurations.append( ("lessFrequentActors", [0.0, 0.1]) )
		tuningConfigurations.append( ("verbsAndNouns", [0.0, 0.1]) )
		
		'''	
		baseConfigurations = [0.5, 0.7]
		tuningConfigurations = []
		tuningConfigurations.append( ("orderInText", [0.1, 0.3, 0.5, 0.7, 0.9]) )
		tuningConfigurations.append( ("moreFrequentActors", [0.1, 0.3, 0.5, 0.7, 0.9]) )
		tuningConfigurations.append( ("lessFrequentActors", [0.1, 0.3, 0.5, 0.7, 0.9]))
		tuningConfigurations.append( ("verbsAndNouns", [0.1, 0.3, 0.5, 0.7, 0.9]))
		'''

		bestWeights = None
		bestEvaluation = 0.0

		print "\n############################"
		print "# Running Configurator for: " + self.collectionId
		print "############################"

		configurations = [{ "base_feature" : baseFeatureWeight,
							"tuning_features" : [ tuningFeatureN1Weight,
												  tuningFeatureN2Weight,
												  tuningFeatureN3Weight, 
												  tuningFeatureN4Weight ] }
		for baseFeatureWeight in baseConfigurations
			for tuningFeatureN1Weight in tuningConfigurations[0][1]
				for tuningFeatureN2Weight in tuningConfigurations[1][1]
					for tuningFeatureN3Weight in tuningConfigurations[2][1]
						for tuningFeatureN4Weight in tuningConfigurations[3][1]
		]

		num_cores = multiprocessing.cpu_count()
		self.results["all"] = Parallel(n_jobs=num_cores)(delayed(runConfiguration)(weights, self.subjects) for weights in configurations)

		for result in self.results["all"]:
			if result["evaluation"] > bestEvaluation:
				bestWeights = result["weights"]
				bestEvaluation = result["evaluation"]

		self.results["best"]["weights"] = bestWeights
		self.results["best"]["evaluation"] = bestEvaluation

