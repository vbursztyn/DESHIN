import sys, os
sys.path.append(os.path.join(os.getcwd(), ".."))

from models.collections import Collections

from models.subject import Subject

from persistence import mongoInterface


mongoInterface.setup()

collections = Collections()
collections.save(mongoInterface)

for collectionId, subjectsIds in collections.getCollections():
	print "############################"
	print "# Preprocessing collection: " + collectionId
	print "############################\n"
	for subjectId in subjectsIds:
		try:
			subject = Subject(subjectId)
			subject.fetch()
			subject.parse()
			subject.save(mongoInterface)
		except (OSError, Exception) as e:
			print "Error: ", e


mongoInterface.close()
