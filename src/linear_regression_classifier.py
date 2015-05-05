#Linear Regression: combines probabilities from naive_bayes_class_return_probs.py and pos_classifier_4grams_return_probs.py, using our POS tagger

from naive_bayes_class_return_probs import naive_bayes
from pos_tagger_class import pos_tagger
from pos_classifier_4grams_return_probs import pos_classifier

#Set filenames
trainFilename = "../Data/all_posts_train"
testFilename = "../Data/all_posts_test"

#Read in training file
trainFile = open(trainFilename, 'r')
trainData = trainFile.readlines()
trainFile.close()

#Create naive bayes classifier
naive_bayes = naive_bayes(trainData)

#Create part of speech tagger
pos_tagger = pos_tagger(trainData)

#Create tag sequence classifier
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

	#Get vocab probs from naive bayes model
	vocab_probs = naive_bayes.decode(words)
	
	#Get POS probs by generating the tag sequence and plugging it into the tri- and 4-grams POS classifier
	tagSequence = pos_tagger.decode(words)
	pos_probs = pos_classifier.decode(tagSequence)
	
	#Calculate linear regression model

	#Straight model, no ridge regression or other multicollinearity corrections- leaves out 40s variables, 43.2% accuracy
	predictedAge = 41.4861 - 32.3173*vocab_probs[0] - 22.4564*vocab_probs[1] - 9.166*vocab_probs[2] + 4.2246*pos_probs[0] + 3.2997*pos_probs[1] - 13.55*pos_probs[2]
	
	#Using ridge regression, lambda = 1: 43.2% accuracy
	#predictedAge = 26.8377018 - 17.8059727*vocab_probs[0] - 7.9473321*vocab_probs[1] + 5.3389428*vocab_probs[2] + 14.5049926*vocab_probs[3] + 4.3542027*pos_probs[0] + 3.4327589*pos_probs[1] - 13.3937298*pos_probs[2] + 0.1450386*pos_probs[3]

	#LASSO model
	#predictedAge = -9.860902*vocab_probs[0] + 13.289757*vocab_probs[2] + 22.456358*vocab_probs[3] + 4.224565*pos_probs[0] + 3.299685*pos_probs[1] - 13.549970*pos_probs[2]

	#Model with only vocabulary
	#predictedAge = 40.4623 - 31.9016*vocab_probs[0] - 22.4249*vocab_probs[1] - 10.3633*vocab_probs[2] 

	#print predictedAge

	if predictedAge <= 15:
		winningCategory = '10'
	elif predictedAge <= 25:
		winningCategory = '20'
	elif predictedAge <= 35:
		winningCategory = '30'
	else:
		winningCategory = '40'
	

	#winningIndex = vocab_probs.index(max(vocab_probs))
	#winningCategory = naive_bayes.categories[winningIndex]

	#Evaluate accuracy
	if winningCategory == actualCategory:
		numCorrect += 1
	else:
		numIncorrect += 1

print str( float(numCorrect)/(numCorrect + numIncorrect) * 100 ) + "%"
