import sys, os
sys.path.append(os.getcwd())

from globals import RESULTS_PATH

from configurator.configurator import Configurator

from persistence import mongoInterface

import json


mongoInterface.setup()

collections = mongoInterface.getCollections()
allSubjects = dict()

for collectionId, subjectsIds in collections[0].iteritems():
	if collectionId == "_id":
		continue

	print "\n############################"
	print "# Reading collection: " + collectionId
	print "############################"
	
	for subjectId in subjectsIds:
		subject = mongoInterface.getSubject(subjectId)[0]
		allSubjects[subjectId] = subject
		print "Successfully read subject: " + subjectId

# Configurator gathers Collection-wise results and, until it converges, adjusts weights for a new iteration
configurator = Configurator()
finalResults = dict()

for collectionId, subjectsIds in collections[0].iteritems():

	if collectionId == "_id":
		continue

	print "\n############################"
	print "# Processing collection: " + collectionId
	print "############################"

	subjects = dict()
	for subjectId in subjectsIds:
		subjects[subjectId] = allSubjects[subjectId]
	configurator.setCollection(collectionId)
	configurator.setSubjects(subjects)
	configurator.run()

	finalResults[collectionId] = configurator.getResults()

mongoInterface.close()


with open(RESULTS_PATH, "w") as fResults:
		json.dump(finalResults, fResults, indent=4)


