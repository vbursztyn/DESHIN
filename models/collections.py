from globals import COLLECTIONS_PATH, DB_DEFAULT_COLLECTIONS_KEY

from persistence import MongoWritable

import copy


# USAGE:
# collections = Collections()
# try:
# 	print collections.getCollection("type2")
# except KeyError as e:
# 	print "Error: ", e


class Collections(MongoWritable):

	
	collections = dict()

	
	def __init__(self, collectionsPath=COLLECTIONS_PATH):
		with open(collectionsPath, "r") as collectionsFile:
			for line in collectionsFile:
				tokens = line.split("\t")
				if tokens[0] == ";" or len(tokens) != 2:
					continue
				collection = tokens[0]
				subjectId = tokens[1].replace("\n","")

				if collection not in self.collections:
					self.collections[collection] = list()
				self.collections[collection].append( subjectId )


	def getCollection(self, collection):
		if collection not in self.collections:
			raise KeyError("Collection name not found")
		return self.collections[collection]


	def getCollections(self):
		return self.collections.iteritems()


	def save(self, mongoInterface):
		# Not copying by reference (otherwise pymongo.save() affects original dict)
		saveObj = copy.deepcopy(self.collections)
		saveObj["_id"] = DB_DEFAULT_COLLECTIONS_KEY

		try:
			mongoInterface.writeCollections(saveObj)
		except Exception as e:
			print "Error: ", e

