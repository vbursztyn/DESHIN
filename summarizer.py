import sys, os
sys.path.append(os.getcwd())

from aggregator.aggregator import Aggregator

from evaluator.evaluator import Evaluator

from configurator.configurator import Configurator

from persistence import mongoInterface


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


# Aggregator gathers features, its weights and processes summarization logics one subject per time
aggregator = Aggregator()
aggregator.loadFeatures()
# Evaluator formalizes the criteria by which we look at the results
evaluator = Evaluator()
# Configurator gathers Collection-wise results and, until it converges, adjusts weights for a new iteration
configurator = Configurator()
configurator.setAggregator(aggregator)
configurator.setEvaluator(evaluator)

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

# 	configurator.printResults() # Optimal configuration and actual evaluation metrics


mongoInterface.close()
