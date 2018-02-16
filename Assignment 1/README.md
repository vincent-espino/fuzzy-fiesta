# CSCI 544 - Applied Natural Language Processing, Coding Exercise 1
A set of programs to learn a hidden Markov model and tag sequences of words based on the learned model.

This is the first coding exercise for CSCI 544 - Applied Natural Language Processing. More information on what these programs should be doing is available at http://ron.artstein.org/csci544-2018/coding-1.html.

# Overview
In this assignment, I wrote a Hidden Markov Model part-of-speech tagger for English, Chinese, and a surprise language which was not revealed prior to the assignment submission date. The training data are provided to us tokenized and tagged; the test data was be provided tokenized to us. The tagger is used to tag new words.

# Programs
The assignment comes in the form of two programs: hmmlearn3.py learns a hidden Markov model from the training data, and hmmdecode3.py uses the model to tag new words.
