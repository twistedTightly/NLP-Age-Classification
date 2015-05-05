#!/usr/bin/python

# NLP Final Project
# k-fold Cross Validation

import random, os

### Divide all data into pieces of 10 ###

# Assign each line a random number and sort based on those numbers
# in order to achive a random shuffling
with open('../Data/all_posts','r') as source:
    data = [ (random.random(), line) for line in source ]
data.sort()

# Create 10 new files that will be each of the different parts of
# the data held out 
folds = []
for i in range(10):
	f = open('fold' + str(i), 'w')
	folds.append(f)

# Write unique data into each of the 10 files
i = 0
for line in data:
	folds[i%10].write(line[1])
	i += 1

### Run a model 10 times, holding out different data each time ###
### Run all models? ###

### Delete all data pieces ###
for f in folds:
	os.remove(f.name)