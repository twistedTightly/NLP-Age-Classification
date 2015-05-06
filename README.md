# NLP-Age-Classification
A final project for a natural language processing course in which we classify chatroom messages by age.

Maribeth Rauh, Jennifer Long
CSE 40657
Final Project README

In this README, we will describe how to run each of the models described in our report. Each can be run on the student machines, but they require the updated version of Python found in Dr. Chiang's public folder.

Baseline
--------

Baseline: baseline-wd-length.py

Usage: baseline-wd-length.py <name of age group's data file> <age group's key> ...
Ex: python baseline-wd-length.py 20s_data.dat 20s 30s_data.dat 30s teens_data.dat teens

This is a simple baseline method that averages the word length for each message and classifies the message by age depending on this average. Certain average word length ranges correspond to different age groups.


Naive Bayes Vocabulary Model
----------------------------

Unigram model: naive_bayes_class_return_probs.py
Bigram model: naive_bayes_bigrams_class_return_probs.py

These two files are very similar; both contain the naive_bayes class, which has all of the logic for training and decoding. Both files have a main routine that runs the model on the testing data and determines the accuracy, so these files can be run directly to see those results. The training and testing files are lines in the file, for simplicity.


Logistic Regression Vocabulary Model
------------------------------------

Basic training: logistic_regression.py
With k-fold cross-validation: 10-fold-cross-validation.py

Usage: python logistic_regression.py <test data>

logistic_regression.py is a class that contains the training and testing functions for the logistic regression vocabulary model. This file is a dependency for the cross validation file, which only runs logistic regression.

Part of Speech Tagger
---------------------

pos_tagger class: pos_tagger_class.py
To test accuracy: pos_tester.py

The part of speech tagger class is found in pos_tagger_class.py. This class contains all of the logic for training and decoding. The accuracy of the tagger is tested by running "python pos_tester.py": this file tests the accuracy of the POS tagger itself and the tag n-gram classifier, described below.


Naive Bayes Tag n-grams Model
-----------------------------

Class: pos_classifier_4grams_return_probs.py
To test accuracy: run pos_classifier_4grams_return_probs.py, which uses the annotated tags
		  run pos_tester.py, which uses our POS tagger
			

The naive Bayes classifier using tag n-grams is found in pos_classifier_4grams_return_probs.py. The main routine in this file tests the pure accuracy of the classifier, using the annotated tags instead of the POS tagger that we built. The classifier is used with our tagger in pos_tester.py.


Combined Bag of Words: Vocabulary and POS
-----------------------------------------

Class: naive_bayes_combined.py
To test accuracy: combined_tester.py

The two bags of words (for vocabulary and tag n-grams) are combined in naive_bayes_combined.py. Running "python combined_tester.py" will give the results on the testing data.


Linear Regression
-----------------

To test accuracy: linear_regression_classifier.py

This file uses the naive Bayes vocabulary model and the tag n-gram model to determine and overall classification.

Cross-Validation
----------------

With k-fold cross-validation: 10-fold-cross-validation.py

This file can be run directly without any data input from the command line, assuming that the entire dataset is at '../Data/all_posts' relative to the file. It will only run the logistic regression model.



