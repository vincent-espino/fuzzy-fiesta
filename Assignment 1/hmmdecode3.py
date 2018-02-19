import sys
import json
import operator

backpointers = dict()
probabilities = dict()

def getProbability(possibleState: str(), time: int) -> float:
    if (possibleState, time) in probabilities:
        return probabilities[(possibleState, time)]
    else:
        return 0.0

def getMostProbableStateSequence(backpointers: dict(), time: int) -> list:
    sequence = list()
    # Note that it's possible for a time of 1 to still have multiple backpointer entries.
    if backpointers.__len__() == 1:
        sequence.append(list(backpointers.keys())[0][0])
        return sequence
    if time == 1:
        sequence.append(list(backpointers.keys())[0][0])
        return sequence
    lastPointers = dict()
    for item in probabilities:
        if item[1] == time:
            # lastPointers.append({item: probabilities[item]})
            lastPointers[item] = probabilities[item]
    # Get max pointer from the last dictionary entry. Use this pointer to backtrace.
    # This sorts the probabilities as I want them! Now, get the last key, and use this key to backtrace!
    sortedProbabilities = sorted(lastPointers.items(), key=operator.itemgetter(1))
    # Last element in sortedProbabilities should contain the tuple we want.
    highestLastPointer = sortedProbabilities[len(sortedProbabilities) - 1][0]
    sequence.append(highestLastPointer[0])
    penultimateTransition = backpointers[highestLastPointer]
    time -= 1
    temp = backpointers[(penultimateTransition, time)]
    for item in backpointers:
        if time > 0:
            temp = (penultimateTransition, time)
            sequence.append(temp[0])
            penultimateTransition = backpointers[temp]
        else:
            break
        time -= 1

    return sequence

# Note: the output file from this program should be named hmmoutput.txt.
def begin(filePath: str()):
    # Print out the file path. This should be the untagged test data for which the tagger will attempt to tag.
    untaggedWords = open(filePath, 'r')
    modelFile = open("hmmmodel.txt", "r")
    model = json.load(modelFile)
    modelFile.close()

    outputFile = open("hmmoutput.txt", "w")

    global emissionProbabilities
    emissionProbabilities = model[0]['emissionProbabilities']

    global transitionProbabilities
    transitionProbabilities = model[1]['transitionProbabilities']

    taggedSequences = list()
    sentence = untaggedWords.readline()
    # global backpointers
    # backpointers = dict()
    # global probabilities
    # probabilities = dict()

    while sentence:
        words = sentence.split()
        # Viterbi algorithm

        # Initialization step. States are tags, observations are words.
        startTransitionProbabilities = transitionProbabilities["start"]
        time = 1
        for possibleState in emissionProbabilities[words[0]]:
            # Question: Is it possible that a first word will have been seen with a state not considered as a start state?
            # if words[0] == "\"":
            #     print()
            # print("emissionProbabilities[words[0]][possibleState]: ", emissionProbabilities[words[0]][possibleState])
            # print("startTransitionProbabilities[possibleState]: ", startTransitionProbabilities[possibleState])
            # probability = startTransitionProbabilities[possibleState] * emissionProbabilities[words[0]][possibleState]
            # {}.get(k, 0)
            if possibleState in startTransitionProbabilities:
                tuple = (possibleState, time)
                probability = startTransitionProbabilities[possibleState] * emissionProbabilities[words[0]][possibleState]
                probabilities[tuple] = probability
                backpointers[tuple] = "start"
        # End init step.

        # Recursive step for remaining time points.
        index = 1
        for index in range(index, len(words)):
            currentWord = words[index]
            previousWord = words[index - 1]
            possibleStates = emissionProbabilities[currentWord]
            previousTransitionStates = emissionProbabilities[previousWord]
            time += 1 # Might need to move this?
            for possibleState in possibleStates:
                maxProbability = 0.0
                highestState = ""
                for possiblePreviousState in previousTransitionStates:
                    # If such a transition doesn't exist, do not record it. This might require smoothing?
                    if possibleState in transitionProbabilities[possiblePreviousState]:
                        # print("Previous state ", possiblePreviousState, " to current state ", possibleState, ".")
                        highestProbability = getProbability(possiblePreviousState, time - 1)
                        # print("Transition probability: ", transitionProbabilities[possiblePreviousState][possibleState])
                        # print("Emission probability: ", emissionProbabilities[currentWord][possibleState])
                        probability = highestProbability * transitionProbabilities[possiblePreviousState][possibleState] * emissionProbabilities[currentWord][possibleState]
                        # print("computed probability: ", probability)
                        if probability > maxProbability:
                            # print("old max: ", maxProbability)
                            maxProbability = probability
                            # print("New higher probability found: ", maxProbability)
                            highestState = possiblePreviousState
                # print("Highest previous probability for state ", possibleState, " found was ", maxProbability, " by state ", highestState)
                highestTuple = (possibleState, time)
                backpointers[highestTuple] = highestState
                probabilities[highestTuple] = maxProbability

        mostLikelySequence = list()
        if backpointers.__len__() == 0:
            possibleProbabilities = emissionProbabilities[words[0]]
            sortedProbabilities = sorted(possibleProbabilities.items(), key=operator.itemgetter(1))
            highestProbability = sortedProbabilities[len(sortedProbabilities) - 1]
            mostLikelySequence.append(highestProbability[0])
            taggedSequence = str()
            taggedSequence = words[0] + "/" + highestProbability[0] + "\n"
        else:
            mostLikelySequence = reversed(getMostProbableStateSequence(backpointers, time))
            index = 0
            taggedSequence = str()
            for tag in mostLikelySequence:
                if index + 1 < len(words):
                    taggedSequence += words[index] + "/" + tag + " "
                else:
                    taggedSequence += words[index] + "/" + tag + "\n"
                index += 1
        # print("tagged sequence is ", taggedSequence)
        outputFile.write(taggedSequence)
        sentence = untaggedWords.readline()
        backpointers.clear()
        probabilities.clear()
    untaggedWords.close()
    outputFile.close()

# Open the model for processing. Open a file called hmmmodel.txt
if len(sys.argv) == 0:
    exit(0)
else:
    begin(sys.argv[1])
