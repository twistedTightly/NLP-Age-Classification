#Creates parsed version of our data files
#Usage: python xml_parser.py <input file> <output file>

import sys, re

#Get files
inputFilename = sys.argv[1]
outputFilename = sys.argv[2]
inputFile = open(inputFilename, 'r')
outputFile = open(outputFilename, 'w')

currentlyReadingLine = 0

for line in inputFile.readlines():
	if currentlyReadingLine:
		if "</terminals>" in line:
			#This is the closing line for the post
			currentlyReadingLine = 0
			outputFile.write("\n")
		else:
			#This is a line of content- parse for word and tag and write to file
			line = re.split(' |/', line)
			word = re.sub(r'word=', '', line[2])
			word = re.sub(r'"', '', word)
			tag = re.sub(r'pos=', '', line[1])
			tag = re.sub(r'"', '', tag)

			if "User" in word:
				word = "USER"

			outputFile.write(word + "/" + tag + "/" + sentenceType + " ")
	elif "\t\t<Post class=" in line and '''class="System"''' not in line:
		#Start a post
		line = re.split(' |/', line)
		sentenceType = re.sub(r'class=', '', line[1])
		sentenceType = re.sub(r'"', '', sentenceType) #Save the sentenceType
		currentlyReadingLine = 1
		

inputFile.close()
outputFile.close()
