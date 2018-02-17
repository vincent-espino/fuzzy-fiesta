import sys
import json
import numpy

# Note: the output file from this program should be named hmmoutput.txt.
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

    # Dictionary of backpointers. The main keys are each word.
    # Each word contains keys, which themselves are POS tags that point to dictionaries which
    # contain the state they can be reached from along the probability of getting to them from that state.
    # Ultimately, we want a dictionary that looks like the following:
    # {
    #     "time": {"VB": {"start": 0.02},
    #              "NN": {"start": 0.08}},
    #     "flies": {"VB": {"NN": 0.0064},
    #               "NN": {"NN": .004}}
    #     etc, etc.
    # }
    backpointers = dict()

    sentence = untaggedWords.readline()

    while sentence:
        print("Line from file: ", sentence)
        words = sentence.split()

        for i in range(len(words)):
            # Grab tags for a word.
            possibleTags = emissionProbabilities[words[i]]

            # If this is the first tag in the sequences, consider starting probabilities AND probabilities from the first sequences to the next.
            if i == 0:
                for possibleTag in possibleTags:
                    print("possibleTag: ", possibleTag)
                    if possibleTag in transitionProbabilities["start"]:
                        # Still need checks for if a word/tag isn't found. Worry about that later.
                        # If using log probabilities, try this:
                        # probabilities[tag] = numpy.log(transitionProbabilities["start"][tag] * emissionProbabilities[words[i]][tag])
                        probability = transitionProbabilities["start"][possibleTag] * emissionProbabilities[words[i]][possibleTag]
                        if words[i] not in backpointers:
                            backpointers[words[i]] = dict()
                            backpointers[words[i]][possibleTag] = {"start": probability}
                        else:
                            if possibleTag not in backpointers[words[i]]:
                                backpointers[words[i]][possibleTag] = {"start": probability}
            else:
                previousTransitionTags = emissionProbabilities[words[i - 1]]
                previousWord = words[i - 1]
                for possibleTag in possibleTags:
                    print("possible tag, i > 0: ", possibleTag)
                    for tag in previousTransitionTags:
                        if possibleTag in transitionProbabilities[tag]:
                            if possibleTag == "IN":
                                print("Uh oh")
                            valueList = list(backpointers[previousWord][tag].values())
                            probability = valueList[0] * emissionProbabilities[words[i]][possibleTag] * transitionProbabilities[tag][possibleTag]
                            if words[i] not in backpointers:
                                backpointers[words[i]] = dict()
                                backpointers[words[i]][possibleTag] = {tag:probability}
                            else:
                                if possibleTag not in backpointers[words[i]]:
                                    backpointers[words[i]][possibleTag] = {tag:probability}


        sentence = untaggedWords.readline()
    untaggedWords.close()

    print("Done reading file.")

# Open the model for processing. Open a file called hmmmodel.txt
if len(sys.argv) == 0:
    exit(0)
else:
    begin(sys.argv[1])



# Code probably not needed for after transition probabilities extraction.
# startTransitions = dict()
# for transition in transitionProbabilities:
#     states = transition.rsplit('/', 1)
#     if states[0] == "start":
#         startTransitions[transition] = transitionProbabilities[transition]

# This code correctly determines if tags are/aren't present.
# for tag in transitionProbabilities["start"]:
#     if tag not in emissionProbabilities[words[i]]:
#         print("tag not found. time to smooth")
#     else:
#         print("transition probability: ", transitionProbabilities["start"][tag])
#         print(emissionProbabilities[words[i]])
#         print("tag: ", tag)
#         probabilities[tag] = transitionProbabilities["start"][tag] * emissionProbabilities[words[i]][tag]

# More code
# for possibleTransitionTag in possibleTransitionTags:
#     print("tag to possibly transition to: ", possibleTransitionTag)
#     print("probabilities[possibleTag]: ", probabilities[possibleTag])
#     print("emissionProbabilities[words[i + 1]][possibleTransitionTag]: ",
#           emissionProbabilities[words[i + 1]][possibleTransitionTag])
#     print("transitionProbabilities[possibleTag][possibleTransitionTag]: ",
#           transitionProbabilities[possibleTag][possibleTransitionTag])
#     probabilities[possibleTag] = probabilities[possibleTag] * emissionProbabilities[words[i + 1]][possibleTransitionTag] * transitionProbabilities[possibleTag][possibleTransitionTag]