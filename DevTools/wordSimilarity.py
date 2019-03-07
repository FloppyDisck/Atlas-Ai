import nltk.classify.util
from nltk.corpus import wordnet

word1 = input("Input the first word: ")
word2 = input("Input the second word: ")
threshold = float(input("Similarity threshold: "))

word1 = wordnet.synsets(word1)
word2 = wordnet.synsets(word2)

for synword1 in word1:
    for synword2 in word2:
        similarity = synword1.wup_similarity(synword2)
        if not similarity:
                pass
        elif similarity >= threshold:
                print('''
                First word: {}
                Definition: {}
                
                Second word: {}
                Definition: {}
                
                Similarity: {}
                '''.format(synword1, synword1.definition(), 
                synword2, synword2.definition(), similarity))