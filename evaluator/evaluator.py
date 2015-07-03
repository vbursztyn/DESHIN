class Evaluator():


	def __init__(self):
		self.summary = None
		self.idealSummary = None


	def setTest(self, summary, idealSummary):
		self.summary = summary
		self.idealSummary = idealSummary
	

	def calculatePrecision(self):
		cooccurrences = 0
		for sentence in self.summary:
			if sentence in self.idealSummary:
				cooccurrences = cooccurrences + 1

		precision = cooccurrences / float( len(self.summary) )

		return precision


	def calculateRecall(self):
		cooccurrences = 0
		for sentence in self.summary:
			if sentence in self.idealSummary:
				cooccurrences = cooccurrences + 1

		recall = cooccurrences / float( len(self.idealSummary) )

		return recall


	def run(self):
		# Picked and calculated F1, mostly based on:
		# F1: http://www.isi.edu/natural-language/projects/webclopedia/pubs/02hlt-neats.pdf
		# Precision and Recall: http://www.aclweb.org/anthology/P03-1048
		# Definition: https://en.wikipedia.org/wiki/Precision_and_recall

		if not self.summary or not self.idealSummary:
			raise Exception("Evaluator misscalled - set it first")
		
		precision = self.calculatePrecision()
		recall = self.calculateRecall()
		if precision or recall:
			F1 = (2 * precision * recall) / (precision + recall)
		else:
			F1 = 0.0

		#print "F1 is: " + str(F1)
		return F1

