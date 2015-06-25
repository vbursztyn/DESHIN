class Configurator():

	
	def __init__(self):
		self.aggregator = None
		self.evaluator = None

		self.collectionId = None
		self.subjects = None


	def setAggregator(self, aggregator):
		self.aggregator = aggregator


	def setEvaluator(self, evaluator):
		self.evaluator = evaluator


	def setCollection(self, collectionId):
		self.collectionId = collectionId


	def setSubjects(self, subjects):
		self.subjects = subjects


	def run(self):
		print "\n############################"
		print "# Running Configurator for: " + self.collectionId
		print "############################"

		self.aggregator.setWeights() # (TO-DO: actually search for optimal values in n-weights space.)

		for subject in self.subjects:
			self.aggregator.setSubject(self.subjects[subject])
			self.aggregator.run()
			resultingSummary = self.aggregator.getResultingSummary()
			idealSummary = self.aggregator.getIdealSummary()
			print "\nResulting summary:\n" + str(resultingSummary) + "\n"
			print "\nIdeal summary:\n" + str(idealSummary) + "\n"
			# self.evaluator.setTest(resultingSummary, idealSummary)
			# self.evaluator.run()