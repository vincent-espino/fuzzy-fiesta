import sys
import json

def begin(filePath: str()):
    # Print out the file path. This should be the untagged test data for which the tagger will attempt to tag.
    print("File path is ", filePath)
    untaggedWords = open(filePath, 'r')
    modelFile = open("hmmmodel.txt", "r")
    model = json.load(modelFile)
    modelFile.close()

    emissionProbabilities = model[0]['emissionProbabilities']
    transitionProbabilities = model[1]['transitionProbabilities']
    print("Model loaded.")

    sentence = untaggedWords.readline()

    while sentence:
        print("Line from file: ", sentence)
        sentence = untaggedWords.readline()
        words = sentence.split()

        for word in words:
            print("Attempting to decode POS tags for")

    print("Done reading file.")
    untaggedWords.close()

# Open the model for processing. Open a file called hmmmodel.txt
if len(sys.argv) == 0:
    exit(0)
else:
    begin(sys.argv[1])