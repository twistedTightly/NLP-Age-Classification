#!/usr/bin/python
# baseline-wd-length.py
#
# Maribeth Rauh and Jen Long
#
# This is the baseline algorithm for our project. This will randomly select a tag and class
#	 for each word in the testing data.
# Usage: python baseline-wd-length.py <name of age group's data file> <age group 'key> ...
#			Ex: python baseline-wd-length.py 20s_data 20s 30s_data 30s teens_data teens

import sys
import fileinput
import random

useLength = False

# Breaks the dataset into training and testing data
#	'Percent' is the percentage of the data that will be used for testing (ex: 10)
#	Returns a list of testing and training data, divided by age
def partitionData(percent):
	train = list()
	test = list()
	# The for loop starts at 1 so the name of this program is not
	#	in the input as data
	for i in range(1, len(sys.argv), 2): # Loop through all input files
		# Create two new files to hold each part of the partitioned data
		f_train = open(str(sys.argv[i]).split('_')[0] + '-train', 'w+')
		f_test = open(str(sys.argv[i]).split('_')[0] + '-test', 'w+')
		j = 0
		for line in fileinput.input(sys.argv[i]): # Loop through all lines in the file
			# Only percent% will be in the testing data
			if (j % percent) == 0:
				# Add line to testing file
				f_test.write(line)
			else:
				# Add line to training file
				f_train.write(line)
			j += 1

		train.append(f_train)
		test.append(f_test)

	return test, train

def findMaxWdLength(tokens):
	maxWdLength = 0

	for token in tokens:
		word = token.split('/')[0]
		if word != 'USER' and len(word) > maxWdLength:
			maxWdLength = len(word)

	return maxWdLength

def findAvgWdLength(tokens):
	avgWdLength = 0
	numWords = 0

	for token in tokens:
		word = token.split('/')[0]
		if word != 'USER':
			avgWdLength += len(word)
			numWords += 1

	return avgWdLength / float(numWords)

def predictAgeFromMax(score):
	agePrediction = ''

	if score < 4:
		agePrediction = '40s'
	elif score < 6:
		agePrediction = '20s'
	elif score < 8:
		agePrediction = '30s'
	else:
		agePrediction = 'teens'

	return agePrediction

def predictAgeFromAvg(score):
	agePrediction = ''

	if score < 3:
		agePrediction = 'teens'
	elif score < 4:
		agePrediction = '20s'
	elif score < 5:
		agePrediction = '30s'
	else:
		agePrediction = '40s'

	return agePrediction

def classifyByWordLength():
	lines = 0
	correct = 0

	teens = 0
	twenties = 0
	thirties = 0
	fourties = 0

	# Loop through each file
	# 	Starts at 1 to skip name of code file
	# 	Goes by 2 because each file is followed by a key to compare the age prediction to
	for i in range(1, len(sys.argv), 2):
		# Loop through each message in the file
		for line in fileinput.input(sys.argv[i]):
			tokens = line.split(' ')

			if useLength:
				avgWdLength = findAvgWdLength(tokens)
				ageGroup = predictAgeFromAvg(avgWdLength)
			else:
				maxWdLength = findMaxWdLength(tokens)
				ageGroup = predictAgeFromMax(maxWdLength)

			# The next argument is the age group key
			if ageGroup == sys.argv[i+1]:
				correct += 1
			lines += 1

			# See totals for each class
			if ageGroup == 'teens':
				teens += 1
			elif ageGroup == '20s':
				twenties += 1
			elif ageGroup == '30s':
				thirties += 1
			else:
				fourties += 1

	print '-----------'
	print teens
	print twenties
	print thirties
	print fourties
	return correct / float(lines)


if __name__ == "__main__":
	#train, test = partitionData(10)

	print classifyByWordLength()

