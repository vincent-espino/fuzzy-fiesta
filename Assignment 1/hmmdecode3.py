import sys
import json

# Dictionaries can only have one instace of a particular key. Using them is causing issues when using the backpointers.
def decode(backpointers: list, words: list()) -> list():
    sequence = list()
    if len(words) >= 2:
        lastword = words[len(words) - 1]
        lastTransitionDict = backpointers[len(words) - 1][lastword]
        lastTransition = list(lastTransitionDict.keys())[0]
        sequence.append(lastTransition)
        temp = list(lastTransitionDict[list(lastTransitionDict.keys())[0]])[0]
        for entry in reversed(backpointers):
            sequence.append(temp)
            temp = list(entry[list(entry.keys())[0]])[0]
            print(entry)

    return sequence

    # lastword = words[len(words) - 1]
    # words.remove(lastword)
    # lastWordTransitions = backpointers[len(words)]
    # lastTransition = list(lastWordTransitions.keys())[0]
    # penultimateTransition = list(lastWordTransitions[list(lastWordTransitions.keys())[0]])[0]
    # sequence.append(lastTransition)
    # sequence.append(penultimateTransition)
    # temp = penultimateTransition
    # for word in reversed(words):
    #     transition = list(backpointers[word][temp].keys())[0]
    #     sequence.append(transition)
    #     temp = transition
    # sequence.remove("start")
    # words.append(lastword)

# Note: the output file from this program should be named hmmoutput.txt.
def begin(filePath: str()):
    # Print out the file path. This should be the untagged test data for which the tagger will attempt to tag.
    untaggedWords = open(filePath, 'r')
    modelFile = open("hmmmodel.txt", "r")
    model = json.load(modelFile)
    modelFile.close()

    emissionProbabilities = model[0]['emissionProbabilities']
    transitionProbabilities = model[1]['transitionProbabilities']

    taggedSequences = list()
    sentence = untaggedWords.readline()

    while sentence:
        backpointers = list()
        words = sentence.split()
        for i in range(len(words)):
            # Grab tags for a word.
            possibleTags = emissionProbabilities[words[i]]

            # If this is the first tag in the sequences, consider starting probabilities AND probabilities from the first sequences to the next.
            probabilityDict = dict()
            if i == 0:
                for possibleTag in possibleTags:
                    if possibleTag in transitionProbabilities["start"]:
                        # Still need checks for if a word/tag isn't found. Worry about that later.
                        # If using log probabilities, try this:
                        # probabilities[tag] = numpy.log(transitionProbabilities["start"][tag] * emissionProbabilities[words[i]][tag])
                        probability = transitionProbabilities["start"][possibleTag] * emissionProbabilities[words[i]][possibleTag]
                        probabilityDict[possibleTag] = {"start": probability}
                backpointers.append({ words[i] : probabilityDict})
            else:
                previousTransitionTags = emissionProbabilities[words[i - 1]]
                previousWord = words[i - 1]
                print("current word: ", words[i])
                for possibleTag in possibleTags: # PossibleTags are the emission probabilities for the current word. Use previousTransitionTags?
                    for previousTag in previousTransitionTags:
                        if possibleTag in transitionProbabilities[previousTag]:
                            print("possibleTag: ", possibleTag, ", previousTag: ", previousTag)
                            value = list(backpointers[i - 1][previousWord][previousTag].values())[0]
                            # print("value: ", value)
                            # print("emissionProbabilities[words[i]][possibleTag]: ", emissionProbabilities[words[i]][possibleTag])
                            # print("transitionProbabilities[possibleTag]: ", transitionProbabilities[previousTag][possibleTag])
                            probability = value * emissionProbabilities[words[i]][possibleTag] * transitionProbabilities[previousTag][possibleTag]
                            print("probability: ", probability)
                            if possibleTag not in probabilityDict:
                                probabilityDict[possibleTag] = {previousTag: probability}
                            else:
                                probabilityDict[possibleTag][previousTag] = {previousTag: probability}
                # Compute all the probabilities from possibleTag to each previousTag. keep the highest one; this is the backpointer.


                backpointers.append({ words[i] : probabilityDict})
        mostLikelySequence = reversed(decode(backpointers, words))
        index = 0
        taggedSequence = str()
        for tag in mostLikelySequence:
            if index + 1 < len(words):
                taggedSequence += words[index] + "/" + tag + " "
            else:
                taggedSequence += words[index] + "/" + tag
            index += 1
        print("tagged sequence is ", taggedSequence)
        sentence = untaggedWords.readline()
    untaggedWords.close()

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


# More throwaway...
# if possibleTag in transitionProbabilities[tag]:
#     # valueList = list(backpointers[previousWord][tag].values())
#     value = list(backpointers[i - 1][previousWord][tag].values())[0]
#     print("previous probability: ", value)
#     print("emissionProbabilities[words[i]][possibleTag]: ", emissionProbabilities[words[i]][possibleTag])
#     print("transitionProbabilities[tag][possibleTag]: ", transitionProbabilities[tag][possibleTag])
#     probability = value * emissionProbabilities[words[i]][possibleTag] * transitionProbabilities[tag][possibleTag]
#     # This is faulty. We want duplicates of words.
#     if tag not in probabilityDict:
#         probabilityDict[possibleTag] = {tag: probability}
#     else:
#         if possibleTag not in probabilityDict[tag]:
#             probabilityDict[possibleTag] = {tag: probability}
#         else:
#             probabilityDict[possibleTag][tag] = {tag: probability}

# allPrevious = list()
# for previousTag in previousTransitionTags:
#     print("possibleTag: ", possibleTag, ", previousTag: ", previousTag)
#     value = list(backpointers[i - 1][previousWord][previousTag].values())[0]
#     probability = value * previousTransitionTags[previousTag] * emissionProbabilities[words[i]][possibleTag]
#     print("computed probability: ", probability)
#     if possibleTag not in probabilityDict:
#         probabilityDict[possibleTag] = {previousTag: probability}
#     else:
#         probabilityDict[possibleTag][previousTag] = {previousTag: probability}