#Method 1: Naive Bayes

import math

#Set filenames
trainingFilename = "all_posts"
testingFilename = "all_posts"

#Set categories
categories = ['10', '20', '30', '40']

#-----------------------------------------Training-------------------------------------

#Create data structures for word counts and category counts
wordCounts = dict()
categoryDocumentCounts = dict()
categoryWordCounts = dict()
wordProbs = dict()
for category in categories:
	wordCounts[category] = dict()
	categoryDocumentCounts[category] = 0
	categoryWordCounts[category] = 0
	wordProbs[category] = dict()
numDocuments = 0
vocabSet = set()

#Read in training file
trainingFile = open(trainingFilename, 'r')
trainingData = trainingFile.readlines()
trainingFile.close()

#Read through each line; count and divide
for line in trainingData:
	words = line.rstrip().split()
	
	#Separate first element (category) from the rest of the words
	category = words[0]
	words = words[1:]

	#Process the category
	if category not in categories:
		continue
	categoryDocumentCounts[category] += 1
	numDocuments += 1

	#Count words
	for word in words:
		parts = word.split("/")

		#Parse to get the actual word
		if len(parts) != 3:
			continue
		word = parts[0]
		pos = parts[1]
		sentencePart = parts[2]
		
		if word not in wordCounts[category]:
			wordCounts[category][word] = 0

		wordCounts[category][word] += 1
		categoryWordCounts[category] += 1
		vocabSet.add(word)
	
#Set up smoothing
delta = 0.1
vocabSize = len(vocabSet)

#Calculate probabilities for each category
categoryProbs = dict()
for category in categories:
	categoryProbs[category] = float(categoryDocumentCounts[category]) / numDocuments
		
#Calculate probabilities for each word
for category in categories:
	for word in wordCounts[category]:
		wordProbs[category][word] = ( float(wordCounts[category][word]) + delta ) / ( categoryWordCounts[category] + vocabSize*delta )

#Calculate probabilities for unknown words
unknownWordProb = dict()
for category in categories:
	unknownWordProb[category] = float(delta) / ( categoryWordCounts[category] + vocabSize*delta )


#-----------------------------------------------Testing---------------------------------------------

#Read in testing file
testingFile = open(testingFilename, 'r')
testingData = testingFile.readlines()
testingFile.close()

numCorrect = 0
numIncorrect = 0

for line in testingData:
	words = line.rstrip().split()
	
	#Separate first element (category) from the rest of the words
	actualCategory = words[0]
	words = words[1:]

	#Check that the category is valid
	if category not in categories:
		continue

	#Add up log probabilities for each word, for each category:
	thisLineLogProb = dict()
	for category in categories:
		thisLineLogProb[category] = 0
		for word in words:
			parts = word.split("/")

			#Parse to get the actual word
			if len(parts) != 3:
				continue
			word = parts[0]
			pos = parts[1]
			sentencePart = parts[2]

			#Increment probability
			if word in wordProbs[category]:
				thisWordProb = wordProbs[category][word]
			else:
				thisWordProb = unknownWordProb[category]
			thisLineLogProb[category] += math.log10(thisWordProb)

	#For this line, choose the category with the biggest log prob
	winningCategory = max(thisLineLogProb, key=thisLineLogProb.get)
	
	#Evaluate accuracy
	if winningCategory == actualCategory:
		numCorrect += 1
	else:
		numIncorrect += 1

print float(numCorrect)/(numCorrect + numIncorrect)




