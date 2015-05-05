#Method 1: Naive Bayes
#In main in this file is the final bag of words classifier where the classifier returns probabilities and we interpret them to get a final accuracy

import math

def addLogProbs(logp, logq):
	if logp > logq:
		bigger = logp
		smaller = logq
	else:
		bigger = logq
		smaller = logp
	return bigger + math.log10(1 + math.pow(10, smaller - bigger))

class naive_bayes:
	def __init__(self, trainingData):
		#Set categories
		categories = ['10', '20', '30', '40']

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

			#Count bigrams
			prevWord = words[0].split("/")[0]
			for word in words[1:]:
				parts = word.split("/")
	
				#Parse to get the actual word
				if len(parts) != 3:
					continue
				word = parts[0]
				pos = parts[1]
				sentencePart = parts[2]

				bigram = prevWord + " " + word

				if bigram not in wordCounts[category]:
					wordCounts[category][bigram] = 0

				wordCounts[category][bigram] += 1
				categoryWordCounts[category] += 1
				vocabSet.add(bigram)

				prevWord = word
	
		#Set up smoothing
		delta = 5
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

		#Save relevant data structures
		self.wordProbs = wordProbs
		self.unknownWordProb = unknownWordProb
		self.categories = categories

	#Testing
	def decode(self, words):
		
		#Get relevant data structures
		wordProbs = self.wordProbs
		unknownWordProb = self.unknownWordProb
		categories = self.categories
		

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

			#Count bigrams
			prevWord = words[0].split("/")[0]
			for word in words[1:]:
				parts = word.split("/")
	
				#Parse to get the actual word
				if len(parts) != 3:
					continue
				word = parts[0]
				pos = parts[1]
				sentencePart = parts[2]

				bigram = prevWord + " " + word

				#Increment probability
				if bigram in wordProbs[category]:
					thisWordProb = wordProbs[category][bigram]
				else:
					thisWordProb = unknownWordProb[category]
				thisLineLogProb[category] += math.log10(thisWordProb)
		
		#Get log sum of the 4 log probabilities
		runningLogSum = thisLineLogProb[categories[0]]
		for category in categories[1:]:
			runningLogSum = addLogProbs(runningLogSum, thisLineLogProb[category])
		totalLogSum = runningLogSum
		
		#Construct 4-tuple to be returned of the probability of each category
		probsToReturn = []
		for category in categories:
			thisLogProb = thisLineLogProb[category] - totalLogSum
			thisProb = math.pow(10, thisLogProb)
			probsToReturn.append(thisProb)

		return probsToReturn

if __name__ == "__main__":
	#Set filenames
	trainFilename = "../Data/all_posts_train"
	testFilename = "../Data/all_posts_test"

	#Read in training file
	trainFile = open(trainFilename, 'r')
	trainData = trainFile.readlines()
	trainFile.close()

	#Create naive bayes classifier
	naive_bayes = naive_bayes(trainData)

	#Read in testing file
	testFile = open(testFilename, 'r')
	testData = testFile.readlines()
	testFile.close()

	numCorrect = 0
	numIncorrect = 0

	for line in testData:
		words = line.rstrip().split()
	
		#Separate first element (category) from the rest of the words
		actualCategory = words[0]
		words = words[1:]

		probs = naive_bayes.decode(words)
		
		#Print probabilities- for use in R
		#print str(probs[0]) + "\t" + str(probs[1]) + "\t" + str(probs[2]) + "\t" + str(probs[3])

		winningIndex = probs.index(max(probs))
		winningCategory = naive_bayes.categories[winningIndex]

		#Evaluate accuracy
		if winningCategory == actualCategory:
			numCorrect += 1
		else:
			numIncorrect += 1

	print str( float(numCorrect)/(numCorrect + numIncorrect) * 100 ) + "%"






