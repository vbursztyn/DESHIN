from globals import SUBJECTS_BASE_PATH, ARTICLES_RELATIVE_PATH, ARTICLE_TITLE_SUFFIX, \
					SUMMARY_RELATIVE_PATH, SUMMARY_SUFFIX

from persistence import MongoWritable

from models.summary import Summary

from models.article import Article

import glob


# USAGE:
# subject = Subject("C12_Mundo_EnchenteCoreia")
# try:
# 	subject = Subject(subjectId)
# 	subject.fetch()
# 	subject.parse()
# 	subject.save(mongoInterface)
# except (OSError, Exception) as e:
# 	print "Error: ", e


class Subject(MongoWritable):


	def __init__(self, subjectId):
		self.subjectId = subjectId

		self.articles = dict()
		self.titlesPaths = dict()
		self.summary = None


	def fetchArticles(self, subjectId):
		# Contains articles' contents and maybe a title:
		articlesPath = SUBJECTS_BASE_PATH + subjectId + ARTICLES_RELATIVE_PATH

		contentsPaths = list()
		for path in glob.glob(articlesPath + "*"):
			if ARTICLE_TITLE_SUFFIX not in path: # If it's a content file
				contentsPaths.append(path)
			else: # If it happens to be a title file
				self.titlesPaths[path.replace(ARTICLE_TITLE_SUFFIX,"")] = path
		return contentsPaths


	def fetchSummary(self, subjectId):
		summariesPath = SUBJECTS_BASE_PATH + subjectId + SUMMARY_RELATIVE_PATH

		for path in glob.glob(summariesPath + "*"):
			if SUMMARY_SUFFIX in path:
				return path
		return None


	def fetch(self):
		# Firstly, we fetch articles:
		for articlePath in self.fetchArticles(self.subjectId):
			articleId = articlePath.split("/")[-1].split(".txt")[0]
			print "Fetching article " + articleId + " at " + articlePath

			articleTitle = None # Title is not mandatory in our dataset
			if articlePath in self.titlesPaths: # But if it exists, we fetch it:
				articleTitle = self.titlesPaths[articlePath]

			try:
				self.articles[articleId] = Article(articleId, articlePath, articleTitle)
			except OSError as e:
				print "Error: ", e

		# Then we fetch its summary:
		summaryPath = self.fetchSummary(self.subjectId)
		if not summaryPath:
			raise OSError("Summary not found for: " + self.subjectId)
		try:
			self.summary = Summary(summaryPath)
		except OSError as e:
			print "Error: ", e


	def parse(self):
		# First, we parse subject's articles:
		for articleId in self.articles:
			self.articles[articleId].parseSentences()
		# Then we parse its summary:
		self.summary.parseSentences()


	def save(self, mongoInterface):
		saveObj = dict()
		saveObj["_id"] = self.subjectId
		saveObj["articles_titles"] = dict()
		saveObj["articles_raw"] = dict()
		saveObj["articles_sentences"] = dict()
		print len(self.articles)
		for articleId in self.articles:
			saveObj["articles_titles"][articleId] = self.articles[articleId].getTitle()
			saveObj["articles_raw"][articleId] = self.articles[articleId].getRaw()
			saveObj["articles_sentences"][articleId] = self.articles[articleId].getSentences()
		saveObj["summary_raw"] = self.summary.getRaw()
		saveObj["summary_sentences"] = self.summary.getSentences()

		try:
			mongoInterface.writeSubject(saveObj)
		except Exception as e:
			print "Error: ", e

