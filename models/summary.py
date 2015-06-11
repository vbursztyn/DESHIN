import nltk

import re


class Summary():


	content = None
	sentences = None


	def __init__(self, summaryPath):
		try:
			with open(summaryPath, "r") as summaryFile:
				self.content = self.clearTags(summaryFile.read())
				self.content = self.content.replace("\n", "")
				print self.content + "\n"
		except OSError:
			raise OSError("Summary not found at " + summaryPath)


	def clearTags(self, content): # At start, removes <pX-sY> tags (but it could be useful)
		return re.sub(r"<[^>]+>", "", content)


	def parseSentences(self):
		sentencesTokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
		self.sentences = sentencesTokenizer.tokenize(self.content)


	def getRaw(self):
		return self.content


	def getSentences(self):
		return self.sentences

