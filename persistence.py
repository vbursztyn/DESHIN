from globals import DB_CONFIG, DB_NAMESPACE_COLLECTIONS, DB_DEFAULT_COLLECTIONS_KEY, DB_NAMESPACE_SUBJECTS

import pymongo

from abc import ABCMeta, abstractmethod


class MongoWritable():
	

	__metaclass__ = ABCMeta


	@abstractmethod
	def save(self):
		# All writable classes must write its data to Mongo by using MongoInterface
		return


class MongoInterface():


	client = None
	db = None


	def setup(self, CONFIG=DB_CONFIG):
		self.client = pymongo.MongoClient(DB_CONFIG["host"])
		self.db = self.client[ DB_CONFIG["db"] ]


	def testSetup(self):
		if not self.client or not self.db:
			raise Exception("Database is not set - call setup()")
	

	def writeCollections(self, collections):
		self.testSetup()

		mongoCollection = self.db[ DB_NAMESPACE_COLLECTIONS ]
		mongoCollection.save(collections)


	def writeSubject(self, subject):
		self.testSetup()
		
		mongoCollection = self.db[ DB_NAMESPACE_SUBJECTS ]
		mongoCollection.save(subject)


	def getCollections(self):
		self.testSetup()

		mongoCollection = self.db[ DB_NAMESPACE_COLLECTIONS ]
		return mongoCollection.find({"_id" : "collections"})


	def getSubject(self, subjectId):
		self.testSetup()
		
		mongoCollection = self.db[ DB_NAMESPACE_SUBJECTS ]
		return mongoCollection.find({"_id" : subjectId})


	def close(self):
		self.client.close()


mongoInterface = MongoInterface()

