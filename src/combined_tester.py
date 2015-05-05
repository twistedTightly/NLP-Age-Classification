from pos_tagger_class import pos_tagger
from naive_bayes_combined import naive_bayes_combined


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
naive_bayes_combined = naive_bayes_combined(trainData)

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
	winningTag = naive_bayes_combined.decode(words, tagSequence)

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

print "Percent of POS tags correct: " + str(float(correct)/wordsTested*100) + "%"
print "Percent of posts correctly classified: " + str( float(numCorrect)/(numCorrect + numIncorrect) * 100 ) + "%"
