#!/usr/bin/python

# NLP Final Project
# Logistic regression

# Usage: python logistic_regression.py <test data>

import fileinput, math

class LogisticRegression(object):
	def __init__(self, eta, i, c):
		self.classScores = { '10': 0, '20': 0, '30': 0, '40': 0 }
		self.wordWeights = dict()
		self.trainingIterations = i
		self.eta = eta
		# Regularization factor
		self.C = c

		# Finding single word lines
		self.totalLines = 0
		self.singleWdLines = 0

		self.includeSingleLines = True

		self.guessCount = 0
		self.correctGuesses = 0

		# wordWeights will hold a dictionaries of all words in the training data
		# and associated weights
		for c in self.classScores:
			self.wordWeights[c] = dict()

	def weightMessage(self, tokens, c):
		# Weight for words
		lambda_k_w = 0
		for token in tokens:
			word = token.split('/')[0]
			if word not in self.wordWeights[c]:
				self.wordWeights[c][word] = 0
			lambda_k_w += self.wordWeights[c][word]

		# Total weight for this class
		return self.classScores[c] + lambda_k_w

	# Finding how many single word lines there are
	# Can be used to only use multi-word lines
	def countSingleLine(self, tokens):
		self.totalLines += 1
		if len(tokens) == 2:
			self.singleWdLines += 1
			return True
		return False

	def scoreToProb(self, scores):
		scoreSum = 0
		for c in self.classScores:
			scoreSum += scores[c]

		# Hardcoded because order is important
		probs = []
		probs.append(scores['10']/scoreSum)
		probs.append(scores['20']/scoreSum)
		probs.append(scores['30']/scoreSum)
		probs.append(scores['40']/scoreSum)

		return probs

	def train(self, line):
		tokens = line.split(' ')
		age = tokens.pop(0)

		if not self.countSingleLine(tokens) or self.includeSingleLines:

			#l2 Regularization
			for token in tokens:
				word = token.split('/')[0]
				for c in self.classScores:
					if word not in self.wordWeights[c]:
						self.wordWeights[c][word] = 0
					self.wordWeights[c][word] = self.wordWeights[c][word]*(1-self.eta*self.C)

			# Calculate the score for each class,
			# make a guess, and find z
			classGuess = ('', -10000)
			z = 0
			scores = dict()
			for c in self.classScores:
				scores[c] = self.weightMessage(tokens, c)

				# See if this guess is higher than the previous max
				# Update class guess and score if so
				if scores[c] > classGuess[1]:
					classGuess = (c, scores[c])

				z += math.exp(scores[c])

			# Calculate actual P(k|d) for each class
			if z == 0:
				z = 0.001
			probs = dict()
			for c in self.classScores:
				probs[c] = math.exp(scores[c]) / float(z)

			# Update class and word scores
			self.classScores[age] += self.eta
			for c in self.classScores:
				# Update classes
				self.classScores[c] -= probs[c] * self.eta
				# Update words
				for token in tokens:
					word = token.split('/')[0]
					self.wordWeights[c][word] -= probs[c] * self.eta
					if c == age:
						self.wordWeights[c][word] += probs[c] * self.eta

	# Run on one line at a time
	# Output class and probability that it is that class
	def test(self, line):
		tokens = line.split(' ')
		age = tokens.pop(0)

		scores = dict()
		maxScore = -10000
		guess = ''

		if not self.countSingleLine(tokens) or self.includeSingleLines:

			# Calculate the score for each class to make a guess
			for c in self.classScores:
				scores[c] = self.weightMessage(tokens, c)

				if scores[c] > maxScore:
					guess = c
					maxScore = scores[c]

			# Calculate accuracy
			self.guessCount += 1
			if guess == age:
				self.correctGuesses += 1

		return guess, maxScore, self.scoreToProb(scores)


if __name__ == "__main__":
	model = LogisticRegression(0.09, 25, 0.015)
	for i in range(model.trainingIterations):
		for line in fileinput.input('../Data/all_posts_train'):
			model.train(line)
		#print model.classScores

	#print "Percent of data that are single lines: %f" % (model.singleWdLines / float(model.totalLines) * 100)
	#model.singleWdLines = 0
	#model.totalLines = 0
	
	for line in fileinput.input():
		guess, maxScore, probs = model.test(line)
		print probs

	print "Accuracy: %f" % (model.correctGuesses / float(model.guessCount) * 100)
	print "Percent of data that are single lines: %f" % (model.singleWdLines / float(model.totalLines) * 100)