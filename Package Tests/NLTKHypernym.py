import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet


#syn = wordnet.synsets(word_filtered)

#recursive function to finding the original word
def hypernymFinder (word_list):
    finished_list = [] #The list that will be returned
    unfinished_list = [] #The list that will be reused
    for word in word_list: 
        hypernym_list = word.hypernyms()
        if not hypernym_list:
            finished_list.append(word)
        else:
            for hypernym_word in hypernym_list:
                unfinished_list.append(hypernym_word)
    
    if not unfinished_list:
        return finished_list

    else:
        returned_words = hypernymFinder(unfinished_list)
        for word in returned_words:
            finished_list.append(word)
        return finished_list

sentence_list = [
        "is it going to rain?",
        "how is the weather",
        "what's today's forecast",
        "Is today going to rain?",
        "What is the weather in Chicago?"
    ]

#To test the recursive function
word_set = wordnet.synsets("peculiar")
#print("{}".format(hypernymFinder(word_set)))

testRun = False

if testRun == True:

    def deconstructor(sentence):
        words = word_tokenize(sentence)
        words_filtered = [word for word in words if word not in stopwords.words('english')]
        return words_filtered

    def definer(sentence):
        returnList = []
        for word in sentence:
            definition = word.definition()
            returnList.append([word, definition])
        return returnList

    for sentence in sentence_list:
        print(sentence)
        sentence = deconstructor(sentence)
        print(nltk.pos_tag(sentence))
        for words in sentence:
            syn = wordnet.synsets(words)
            print(definer(syn))


weather = wordnet.synsets("weather", pos='v')
forecast = wordnet.synsets("forecast")
random = wordnet.synsets("dog")



#WordNetlemmatizer().lemmatizer(word, 'v')

#Testing NER
nerTest = False



if nerTest == True:
    for sentence in sentence_list:
        sentence_tokenize = word_tokenize(sentence)
        stop_words = set(stopwords.words('english'))
        sentence_clean = [word for word in sentence_tokenize if not word in stop_words]
        sentence_tagged = nltk.pos_tag(sentence_clean)
        sentence_WH = [sentence_tagged, False]
        for tag_set in sentence_tagged:
            if tag_set[1] == 'WP':
                sentence_WH[1] = True
        print(nltk.ne_chunk(sentence_tagged))
        if sentence_WH[1] == True:
            print("This sentence is a question.")


test6_2_3 = False
if test6_2_3 == True:
    posts = nltk.corpus.nps_chat.xml_posts()[:10000]

    def dialogue_act_features(post):
        features = {}
        for word in nltk.word_tokenize(post):
            features['contains({})'.format(word.lower())] = True
        return features

    featuresets = [(dialogue_act_features(post.text), post.get('class'))
                    for post in posts]
    size = int(len(featuresets) * 0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print(nltk.classify.accuracy(classifier, test_set))