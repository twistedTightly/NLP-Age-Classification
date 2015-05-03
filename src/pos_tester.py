from pos_tagger_class import pos_tagger
from pos_classifier_4grams_return_probs import pos_classifier

#Set filenames
trainFilename = "../Data/all_posts_train"
testFilename = "../Data/all_posts_test"

#Open training file and read in lines
trainFile = open(trainFilename)
trainData = trainFile.readlines()
trainFile.close()

#Create part of speech tagger
pos_tagger = pos_tagger(trainData)

#Create tag sequence classifier
pos_classifier = pos_classifier(trainData)

#Set up testing data
testFile = open(testFilename)
testData = testFile.readlines()
testFile.close()

#Work through the testing data
numCorrect = 0
numIncorrect = 0
correct = 0
wordsTested = 0
linesTested = 0
for line in testData:
	words = line.split()
	age = words[0]
	words = words[1:]
	numWords = len(words)

	tagSequence = pos_tagger.decode(words)
	probs = pos_classifier.decode(tagSequence)

	#Print probabilities- for use in R
	#print str(probs[0]) + "\t" + str(probs[1]) + "\t" + str(probs[2]) + "\t" + str(probs[3])

	#If all are equal, choose 40
	if probs[0] == probs[1] and probs[1] == probs[2] and probs[2] == probs[3]:
		winningTag = pos_classifier.categories[3]

	winningIndex = probs.index(max(probs))
	winningTag = pos_classifier.categories[winningIndex]

	#If all are equal, choose 40 because it's the most likely tag
	if probs[0] == probs[1] and probs[1] == probs[2] and probs[2] == probs[3]:
		winningTag = pos_classifier.categories[3]

	#Evaluate accuracy
	if winningTag == age:
		numCorrect += 1
	else:
		numIncorrect += 1

	for i in range(0, numWords):
		wordTagPair = words[i].split('/')
		word = wordTagPair[0]
		actualTag = wordTagPair[1]
		guessTag = tagSequence[i]

		wordsTested = wordsTested + 1

		#Check accuracy
		if guessTag == actualTag:
			correct += 1

print "Percent POS tags correct: " + str(float(correct)/wordsTested*100) + "%"
print "Percent age classifications correct: " + str( float(numCorrect)/(numCorrect + numIncorrect) * 100 ) + "%"
