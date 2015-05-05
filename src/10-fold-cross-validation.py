#!/usr/bin/python

# NLP Final Project
# k-fold Cross Validation

import random, os, fileinput
import logistic_regression, pos_tagger_class

### Divide all data into folds of k ###
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


### Run a model k times, holding out different data each time ###

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

def POSTagger(folds, heldout):
	model = pos_tagger_class.pos_tagger(folds) # TODO need training data here

logRegAccuracy = 0
for i in range(k):
	accuracy = logisticRegression(folds, i)
	print accuracy
	logRegAccuracy += accuracy

# Calculate combined accuracy
logRegAccuracy /= k
print "Logisitic regression: %f" % (logRegAccuracy)


### Delete all data folds ###
for f in folds:
	os.remove(f.name)