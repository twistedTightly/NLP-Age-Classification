#Method 3: POS tagging with naive bayes trigrams and 4-grams classifier

import math

def addLogProbs(logp, logq):
	if logp > logq:
		bigger = logp
		smaller = logq
	else:
		bigger = logq
		smaller = logp
	return bigger + math.log10(1 + math.pow(10, smaller - bigger))

class pos_classifier:
	def __init__(self, trainData = None):
		if trainData != None: #Train if the training data has been provided
			self.train(trainData)

	def train(self, trainingData):
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

			#Construct tag sequence
			tagSequence = ["<s>"]
			for word in words:
				parts = word.split("/")
				pos = parts[1]
				tagSequence.append(pos)
			tagSequence.append("</s>")

			#Construct all of the tag n-grams that can be used, for n=3,4
			tagNGrams = []

			#Add trigrams
			prevPrevTag = tagSequence[0]
			prevTag = tagSequence[1]
			for tag in tagSequence[2:]:
				tagTrigram = prevPrevTag + "/" + prevTag + "/" + tag
				tagNGrams.append(tagTrigram)	
				prevPrevTag = prevTag
				prevTag = tag	

			#Add 4-grams (only if the tag sequence has at least 4 tags, meaning it's at least two words plus <s> and </s>
			if len(tagSequence) >= 4:
				prevPrevPrevTag = tagSequence[0]
				prevPrevTag = tagSequence[1]	
				prevTag = tagSequence[2]
				for tag in tagSequence[3:]:
					tag4Gram = prevPrevPrevTag + "/" + prevPrevTag + "/" + prevTag + "/" + tag
					tagNGrams.append(tag4Gram)
					prevPrevPrevTag = prevPrevTag
					prevPrevTag = prevTag
					prevTag = tag	

			for tagNGram in tagNGrams:

				if tagNGram not in wordCounts[category]:
					wordCounts[category][tagNGram] = 0

				wordCounts[category][tagNGram] += 1
				categoryWordCounts[category] += 1
				vocabSet.add(tagNGram)

		#Set up smoothing
		delta = 100
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

	def decode(self, tagSequence):
		#Get relevant data structures
		wordProbs = self.wordProbs
		unknownWordProb = self.unknownWordProb
		categories = self.categories

		#Construct all of the tag n-grams that can be used, for n=3,4
		tagNGrams = []

		#Add trigrams
		prevPrevTag = tagSequence[0]
		prevTag = tagSequence[1]
		for tag in tagSequence[2:]:
			tagTrigram = prevPrevTag + "/" + prevTag + "/" + tag
			tagNGrams.append(tagTrigram)	
			prevPrevTag = prevTag
			prevTag = tag	

		#Add 4-grams (only if the tag sequence has at least 4 tags, meaning it's at least two words plus <s> and </s>
		if len(tagSequence) >= 4:
			prevPrevPrevTag = tagSequence[0]
			prevPrevTag = tagSequence[1]	
			prevTag = tagSequence[2]
			for tag in tagSequence[3:]:
				tag4Gram = prevPrevPrevTag + "/" + prevPrevTag + "/" + prevTag + "/" + tag
				tagNGrams.append(tag4Gram)
				prevPrevPrevTag = prevPrevTag
				prevPrevTag = prevTag
				prevTag = tag	

		#Add up log probabilities for each word, for each category:
		thisLineLogProb = dict()
		for category in categories:
			thisLineLogProb[category] = 0	


			for tagNGram in tagNGrams:
				#Increment probability
				if tagNGram in wordProbs[category]:
					thisWordProb = wordProbs[category][tagNGram]
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

	#Create pos_classifier
	pos_classifier = pos_classifier(trainData)

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

		#Construct tag sequence
		tagSequence = ["<s>"]
		for word in words:
			parts = word.split("/")
			pos = parts[1]
			tagSequence.append(pos)
		tagSequence.append("</s>")

		probs = pos_classifier.decode(tagSequence)

		winningIndex = probs.index(max(probs))
		winningCategory = pos_classifier.categories[winningIndex]

		#Evaluate accuracy
		if winningCategory == actualCategory:
			numCorrect += 1
		else:
			numIncorrect += 1

	print str( float(numCorrect)/(numCorrect + numIncorrect) * 100 ) + "%"








