#!/usr/bin/python
# baseline.py
#
# Maribeth Rauh and Jen Long
#
# This is the baseline algorithm for our project. This will randomly select a tag and class
#	 for each word in the testing data.

import sys
import fileinput
import random

# Breaks the dataset into training and testing data
#	'Percent' is the percentage of the data that will be used for testing (ex: 10)
#	Returns a list of testing and training data, divided by age
def partitionData(percent):
	train = list()
	test = list()
	# The for loop starts at 1 so the name of this program is not
	#	in the input as data
	for i in range(1, len(sys.argv)): # Loop through all input files
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

# Counts the occurance of each tag and class
def train(trainingList):
	classCount = dict()
	classCount['total'] = 0
	tagCount = dict()
	tagCount['total'] = 0
	ageCount = dict()
	ageCount['total'] = 0

	for f in trainingList:
		# Return file pointer to the beginning of the file
		f.seek(0)
		for line in f:
			line = line.strip().split(' ')
			actualAge = line.pop(0)
			
			if actualAge in ageCount:
				ageCount[actualAge] += 1
			else:
				ageCount[actualAge] = 1
			ageCount['total'] += 1
				

	return ageCount #, classCount, tagCount

def test(testingList):
	correctlyClassified = 0
	totalClassified = 0

	for f in testingList:
		f.seek(0); # Return pointer to beginning of file
		for line in f:
			line = line.strip().split(' ')
			actualAge = line.pop(0)

			# The age of the speaker for each line is guessed randomly
			r = random.random()
			if r < 0.25:
				guessedAge = '10'
			elif r < 0.5:
				guessedAge = '20'
			elif r < 0.75:
				guessedAge = '30'
			else:
				guessedAge = '40'

			totalClassified += 1
			if actualAge == guessedAge:
				correctlyClassified += 1

	return correctlyClassified / float(totalClassified)


if __name__ == "__main__":
	# testingList and trainingList are lists of data files that are
	#	still separated by age
	# testing is a single file with the testing data combined randomly
	testingList, trainingList = partitionData(10)

	# Note - this counts the frequency of each class, which could be
	#	used to slightly improve the baseline if desired
	ageCount = train(trainingList)

	accuracy = test(testingList)
	print accuracy


