#!/usr/bin/python

# NLP Final Project
# k-fold Cross Validation

import random, os, fileinput
import logistic_regression
from pos_tagger_class import pos_tagger
from pos_classifier_4grams_return_probs import pos_classifier
import sys

###################
###
### Divide all data into folds of k
###
###################

k = 10

# Assign each line a random number and sort based on those numbers
# in order to achive a random shuffling
with open('../Data/all_posts','r') as source:
    data = [ (random.random(), line) for line in source ]
data.sort()

# Create 10 new files that will be each of the different parts of
# the data held out 
folds = []
for i in range(k):
	f = open('fold' + str(i), 'w')
	folds.append(f)

# Write unique data into each of the 10 files
i = 0
for line in data:
	folds[i%k].write(line[1])
	i += 1


###################
###
### Run a model k times, holding out different data each time 
###
###################

# LOGISTIC REGRESSION
def logisticRegression(folds, heldout):
	model = logistic_regression.LogisticRegression(0.08, 25, 0.015)
	for i in range(model.trainingIterations):
		# Train on all folds except the heldout fold
		for f in folds:
			if f.name != 'fold' + str(heldout):
				for line in fileinput.input(f.name):
					model.train(line)
	
	for line in fileinput.input(folds[heldout].name):
		guess, maxScore, probs = model.test(line)

	return model.correctGuesses / float(model.guessCount)

# Run model
logRegAccuracy = 0
for i in range(k):
	pass
	accuracy = logisticRegression(folds, i)
	print accuracy
	logRegAccuracy += accuracy

# Calculate combined accuracy
logRegAccuracy /= k
print "Logisitic regression: %f" % (logRegAccuracy)


# POS TAGGER + NAIVE BAYES
def POSTagger(folds, heldout):
	# Train both models
	trainingData = []
	for f in folds[:heldout]+folds[heldout+1:]:
		trainingData.append(f.name)

	with open('all_heldout'+str(heldout), 'w') as outfile:
	    for fname in trainingData:
	        with open(fname) as infile:
	            outfile.write(infile.readline())

	f = open('all_heldout'+str(heldout))
	train = f.readlines()
	f.close()

	tagger = pos_tagger(train)
	classifier = pos_classifier(train)

	#Work through the testing data
	numCorrect = 0
	numIncorrect = 0
	correct = 0
	wordsTested = 0
	linesTested = 0
	for line in fileinput.input(folds[heldout].name):
		print line
		words = line.split()
		age = words[0]
		words = words[1:]
		numWords = len(words)
		print words
		tagSequence = tagger.decode(words)
		probs = classifier.decode(tagSequence)

		winningIndex = probs.index(max(probs))
		winningTag = classifier.categories[winningIndex]

		#If all are equal, choose 40 because it's the most likely tag
		if probs[0] == probs[1] and probs[1] == probs[2] and probs[2] == probs[3]:
			winningTag = classifier.categories[3]

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

	classificationAccuracy = float(numCorrect)/(numCorrect + numIncorrect)
	print "Percent POS tags correct: " + str(float(correct)/wordsTested*100) + "%"
	print "Percent age classifications correct: " + str( classificationAccuracy * 100 ) + "%"

	return classificationAccuracy

# Run model
posAndNaiveBayesAccuracy = 0
for i in range(k):
	accuracy = POSTagger(folds, i)
	posAndNaiveBayesAccuracy += accuracy

# Calculate combined accuracy
posAndNaiveBayesAccuracy /= k
print "POS and NB: %f" % (posAndNaiveBayesAccuracy)
# NAIVE BAYES COMBINED (POS AND BAG OF WORDS)


###################
###
### Delete all data folds
###
###################

for f in folds:
	os.remove(f.name)
