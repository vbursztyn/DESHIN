class Evaluator():


	def __init__(self):
		self.summary = None
		self.idealSummary = None


	def setTest(self, summary, idealSummary):
		self.summary = summary
		self.idealSummary = idealSummary
	

	def run(self):
		# Combinates precision, recall or whatever other evaluation metric, into one final test result.
		# At a first glance, F1 offers a fair combination.
		if not self.summary or not self.idealSummary:
			raise Exception("Evaluator misscalled - set it first")
		
		cooccurrences = 0
		for sentence in self.summary:
			if sentence in self.idealSummary:
				cooccurrences = cooccurrences + 1

		precision = cooccurrences / float( len(self.summary) )
		print "Precision is: " + str(precision)
		return precision