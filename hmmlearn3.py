import sys
import json

# File should be of the name hmmmodel.txt
def begin(filePath: str()):

    # Open file for parsing.
    file = open(filePath, 'r')
    sentence = file.readline()

    # This is needed for emission probabilities.
    discoveredTags = dict()
    wordTagPairs = dict()
    wordTagOccurrences = dict()

    # This is needed for transition probabilities.
    numberOfSentences = 0
    tagPairs = dict()
    transitionOccurrences = dict()
    transitionDiscoveredTags = dict()

    # We need to get both transition and emission probabilities (this is basically the model).
    # This can probably be further marginalized as follows:
    # Every time we encounter a word, add it to a map and set its count to 1 if it was not encountered before.
    # Else if the word was encountered, increment its count by 1.
    # We need the total counts of each tag for transition probabilties.
    # We also need the number of times a particular word was found with a certain tag.
    while sentence:
        numberOfSentences += 1
        # Split sentences by whitespaces.
        tags = sentence.split()
        # print("Line: ", sentence)
        numTags = len(tags)
        for i in range(0, numTags):
            # Store each word/TAG token and get the number of times each one occurs.
            # This is needed for the transition probabalities.
            if tags[i] not in wordTagPairs:
                wordTagPairs[tags[i]] = 1
            else:
                wordTagPairs[tags[i]] = wordTagPairs[tags[i]] + 1

            # Split the token by the last occurring slash, which we are told is the separator between
            # word and its part of speech tag.
            wordAndTag = tags[i].rsplit('/', 1)

            if(i + 1 < numTags):
                # If we're not at the end of the sentence, make a tuple instead!
                # Split token and add a tuple to the dictionary of tuples.
                # tuple = (wordAndTag[1], tags[i + 1].rsplit('/', 1)[1])
                tagPair = wordAndTag[1] + "/" + tags[i + 1].rsplit('/', 1)[1]
                if tagPair not in tagPairs:
                    tagPairs[tagPair] = 1
                else:
                    tagPairs[tagPair] += 1

                # Keep track of how many times the first tag of the tuple occurs.
                if wordAndTag[1] not in discoveredTags:
                    transitionDiscoveredTags[wordAndTag[1]] = 1
                else:
                    print("wordAndTag[1]: ", wordAndTag[1])
                    transitionDiscoveredTags[wordAndTag[1]] = transitionDiscoveredTags[wordAndTag[1]] + 1

            # Get the number of times each tag occurs. This is needed for the denominator portion
            # when calculating transition probabilities.
            if wordAndTag[1] not in discoveredTags:
                discoveredTags[wordAndTag[1]] = 1
            else:
                discoveredTags[wordAndTag[1]] = discoveredTags[wordAndTag[1]] + 1

        sentence = file.readline()

    file.close()
    # print("Calculating transition probabilities.")

    # We have counts for each word/TAG and the number of times each word occurs with each tag.
    # For each word, calculate the probability it occurs with a tag. This is just the
    # (number of times the word occurs with that tag) / (number of times that tag occurs).
    # The following computes the emission probabilities.

    for pair in wordTagPairs:
        wordAndTag = pair.rsplit('/', 1)
        if wordAndTag[0] not in wordTagOccurrences:
            # If the word hasn't been added to the dictionary yet,
            # add it and set its value to be its transition probability.
            # Note that the value is divded by the number of times the tag occurred in the corpus;
            # this is the probability we're looking for!
            wordTagOccurrences[wordAndTag[0]] = dict()
            wordTagOccurrences[wordAndTag[0]][wordAndTag[1]] = (wordTagPairs[pair] / discoveredTags[wordAndTag[1]])
        else:
            wordTagOccurrences[wordAndTag[0]][wordAndTag[1]] = (wordTagPairs[pair] / discoveredTags[wordAndTag[1]])

    # The following computes the transition probabilities.
    # For each tuple, divide the number of times the tuple occurs
    # by the number of times the first portion of the tuple occurred.
    # Starting transitions are easier: divide the number of times a starting tag
    # occurs by the number of given sentences.

    for pair in tagPairs:
        # print("tagPairs[pair] has count: ", tagPairs[pair])
        splitTags = pair.rsplit("/", 1)
        # print("leading tag is ", splitTags[0])
        # print("total times of first tags occurrence: ", transitionDiscoveredTags[splitTags[0]])
        transitionOccurrences[pair] = tagPairs[pair] / transitionDiscoveredTags[splitTags[0]]

    # print("Done parsing. Creating file.")
    model = open("hmmmodel.txt", "w+")

    emissionProbabilities = { "emissionProbabilities" : wordTagOccurrences }
    transitionProbabilities = { "transitionProbabilities" : transitionOccurrences }
    learnedProbabilities = []
    learnedProbabilities.append(emissionProbabilities)
    learnedProbabilities.append(transitionProbabilities)
    # Pretty print the JSON a bit! ensure_ascii=False to print in UTF-8.
    json.dump(learnedProbabilities, model, indent=4, ensure_ascii=False)




# Open the file for processing.
if len(sys.argv) == 0:
    exit(0)
else:
    begin(sys.argv[1])


# Original code I used to get things set up (and practice string parsing).
# words = test.split()
# for word in words:
#     if word.count('/') > 1:
#         print("word ", word, " has more than one slash!!!")
#     wordAndTag = word.rsplit('/', 1)
#     print("Word: ", wordAndTag[0], " has tag ", wordAndTag[1])