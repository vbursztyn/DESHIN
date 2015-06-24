import nltk


class Article():


	def __init__(self, articleId, articlePath, articleTitle=None):
		self.articleId = None

		self.title = None
		self.content = None
		self.sentences = None

		try:
			if articleTitle:
				with open(articleTitle, "r") as titleFile:
					self.title = titleFile.read()
					self.title = self.title.replace("\n", "")
					print "Title: " + self.title
			with open(articlePath, "r") as articleFile:
				self.content = articleFile.read()
				print "Content: "+ self.content[:50] + " (...)\n"
		except OSError:
			raise OSError("Article " + articleId + " not found")


	def parseSentences(self):
		sentencesTokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
		self.sentences = sentencesTokenizer.tokenize(self.content.decode("utf-8"))


	def getTitle(self):
		return self.title


	def getRaw(self):
		return self.content


	def getSentences(self):
		return self.sentences