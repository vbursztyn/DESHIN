class Configurator():

	
	aggregator = None

	collectionId = None
	subjects = None


	def setAggregator(self, aggregator):
		self.aggregator = aggregator


	def setCollection(self, collectionId):
		self.collectionId = collectionId


	def setSubjects(self, subjects):
		self.subjects = subjects


	def run(self):
		print "\n############################"
		print "# Running Configurator for: " + self.collectionId
		print "############################"

		for subject in self.subjects:
			self.aggregator.setSubject(self.subjects[subject])
			self.aggregator.run()