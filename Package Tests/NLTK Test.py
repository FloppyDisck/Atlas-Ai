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

print(f"""
{lineBreak}
Breaking down this sentence: \"{sentence}\"

{nltk.pos_tag(words)}
{lineBreak}
""")

#Clean the sentence
#print(stopwords.words('english'))
words_filtered = [word for word in words if word not in stopwords.words('english')]

print(f"""
{lineBreak}
Filtered broken down sentence:
{nltk.pos_tag(words_filtered)}

{lineBreak}
""")

#Find word definition and other functions
for word_filtered in words_filtered:
    syn = wordnet.synsets(word_filtered)

    print(f"""{lineBreak}
    Wordnet function on \"{word_filtered}\"

    Word related: 
    {syn}
    """)

    for word in syn:
        print("~"*100)
        print(f"""
        Word: {word.name()}
        Definition: {word.definition()}
        """)
        for hypernym in word.hypernyms():
            print(f"""    Hypernym: {hypernym}""")
        if (len(word.hypernyms()) > 0):
            print(" ")

        for hyponym in word.hyponyms():
            print(f"""    Hyponym: {hyponym}""")
        if (len(word.hyponyms()) > 0):
            print(" ")

        for similar in word.lemmas():
            print(f"""    Similar Word: {similar}""")
            if (similar.antonyms()):
                print(f"""    Antonym: {similar.antonyms()}""")
        if (len(word.lemmas()) > 0):
            print(" ")

        for example in word.examples():
            print(f"""    Example: {example}""")

    print(lineBreak)

#nltk.help.upenn_tagset() #See what the tokenized tags mean