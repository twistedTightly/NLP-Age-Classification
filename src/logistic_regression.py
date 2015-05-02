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

	def train(self, trainingData):
		for line in fileinput.input(trainingData):
			tokens = line.split(' ')
			age = tokens.pop(0)

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

		# Calculate the score for each class to make a guess
		scores = dict()
		maxScore = -10000
		guess = ''
		for c in self.classScores:
			scores[c] = self.weightMessage(tokens, c)

			if scores[c] > maxScore:
				guess = c
				maxScore = scores[c]

		# Calculate accuracy
		self.guessCount += 1
		if guess == age:
			self.correctGuesses += 1

		return guess, maxScore, scores


if __name__ == "__main__":
	model = LogisticRegression(0.09, 25, 0.015)
	for i in range(model.trainingIterations):
		model.train('../Data/all_posts_train')
		print model.classScores
	
	for line in fileinput.input():
		guess, maxScore, scores = model.test(line)
		print scores

	print model.correctGuesses / float(model.guessCount)