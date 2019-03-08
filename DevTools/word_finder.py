import nltk.classify.util
from nltk.corpus import wordnet

word = input("Input the word: ")

for synword in wordnet.synsets(word):
    print(synword)
    print(synword.definition())
    print(" ")