import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

lineBreak = "-" * 100

#Breakdown sentence and tokenize each word
sentence = "Could you tell me how the weather is looking?"
words = word_tokenize(sentence)

print("""
{}
Breaking down this sentence: \"{}\"

{}
{}
""".format(lineBreak, sentence, nltk.pos_tag(words), lineBreak))

#Clean the sentence
#print(stopwords.words('english'))
words_filtered = [word for word in words if word not in stopwords.words('english')]

print("""
{}
Filtered broken down sentence:
{}

{}
""".format(lineBreak, nltk.pos_tag(words_filtered), lineBreak))

#Find word definition and other functions
for word_filtered in words_filtered:
    syn = wordnet.synsets(word_filtered)

    print("""{}
    Wordnet function on \"{}\"

    Word related: 
    {}
    """.format(lineBreak,word_filtered, syn))

    for word in syn:
        print("~"*100)
        print("""
        Word: {}
        Definition: {}
        """.format(word.name(), word.definition()))
        for hypernym in word.hypernyms():
            print("""    Hypernym: {}""".format(hypernym))
        if (len(word.hypernyms()) > 0):
            print(" ")

        for hyponym in word.hyponyms():
            print("""    Hyponym: {}""".format(hyponym))
        if (len(word.hyponyms()) > 0):
            print(" ")

        for similar in word.lemmas():
            print("""    Similar Word: {}""".format(similar))
            if (similar.antonyms()):
                print("""    Antonym: {}""".format(similar.antonyms()))
        if (len(word.lemmas()) > 0):
            print(" ")

        for example in word.examples():
            print("""    Example: {}""".format(example))

    print(lineBreak)

#nltk.help.upenn_tagset() #See what the tokenized tags mean