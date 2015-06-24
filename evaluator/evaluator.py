class Evaluator():


	def __init__(self):
		self.summary = None
		self.idealSummary = None


	def setTest(self, summary, idealSummary):
		self.summary = summary
		self.idealSummary = idealSummary


	def precision(self):
		return


	def recall(self):
		return


	def F1(self):
		return
	

	def run(self):
		# Combinates precision, recall or whatever other evaluation metric, into one final test result.
		# At a first glance, F1 offers a fair combination.
		return