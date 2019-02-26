import nltk.classify.util
from nltk.corpus import wordnet

word1 = input("Input the first word: ")
word2 = input("Input the second word: ")

word1 = wordnet.synsets(word1)
word2 = wordnet.synsets(word2)

for synword1 in word1:
    print(synword1)
    print(synword1.definition())
    for synword2 in word2:
        print(synword2)
        print(synword2.definition())
        print(synword1.wup_similarity(synword2))
        print(" ")