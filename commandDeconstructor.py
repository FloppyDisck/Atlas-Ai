#The program will take an input string an process it to identify what its trying to express

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

def test_tokenizer(sentence):
    return nltk.pos_tag(nltk.word_tokenize(sentence))

def extract_NN(sentence): #TODO: Study how to properly make a regexParser string
    grammar = r"""

    NBAR:
        # Nouns and Adjectives, terminated with Nouns
        {<NN.*>*<NN.*>}

    NP:
        # Above, connected with in/of/etc...
        {<NBAR><IN><NBAR>}

        {<NBAR>}
    """

    backup_grammar = r"""

    JJBAR:
        {<VB.*>}

    NP:
        {<JJBAR>}
    """
    grammar_list = [grammar, backup_grammar] #List composed of the params

    for grammar in grammar_list:

        chunker = nltk.RegexpParser(grammar, trace=0)
        ne = set()
        chunk = chunker.parse(nltk.pos_tag(nltk.word_tokenize(sentence)))
        for tree in chunk.subtrees(filter=lambda t: t.label() == 'NP'):

            for child in tree.leaves(): #this way allows for implementing the whole list
                ne.add(child)
            #ne.add(' '.join([child[0] for child in tree.leaves()]))

        if (len(ne) > 0): #If condition is not met Run the program again with the next value
            break
                
    return ne

def commandIdentifier(sentence, commandDic, commandDicScore):

    print(sentence) #Print sentence
    #print(test_tokenizer(sentence)) #Print tokenized sentence
    extractedSentence = extract_NN(sentence)

    for command, commandSynsets in commandDic.items():

        for item in extractedSentence:
            #print(item) #Print the list with both the word and type
            try:
                for word in wordnet.synsets(item[0].lower(), pos=item[1][0].lower()): #Parse the word
                    #print(word) #Print the wordnet word related to the item list

                    for commandSynsets in commandSynset:

                        simScore = commandSynset.wup_similarity(word)
                        #print(simScore) #Print the similarity score achieved (max 1.0)

                        if (not simScore):
                            #print("Not related")
                            pass

                        elif (commandDicScore[command] < simScore):
                            commandDicScore[command] = simScore

            except KeyError as errorCode:
                #print("Did not find {} in the wordnet!".format(item)) #Error code when word is not found
                pass

        if (commandDicScore[command] >= 0.8):
            print("This sentence is related to {}".format(command))
        else:
            print("This sentence is not related to {}".format(command))


if __name__ == "__main__":
    sentence_list = [
        "is it going to rain?",
        "how is the weather",
        "what's today's forecast",
        "Is today going to rain?",
        "What is the weather in Chicago?",
        "Is it hot or cold?",
        "Is it sunny, should I take sunglasses?",
        "Is it raining outside?",
        "Should I take my umbrella?",
        "What's the weather forecast?",
        "What’s the weather expected to be tomorrow?",
        "What’s the temperature?",
        "How’s the weather?",
        "What’s it like outside?",
        "How's the weather?",
        "Do you have rain?",
        "What's the temperature in Manchester?",
        "Is it a Beautiful day for a walk?"
        "What's the weather forecast for the rest of the week?",
        "what is the weather like tomorrow?",
        "What will the weather be like tomorrow?",
        "What is the weather going to be like tomorrow?",
        "What is the weather forecast for tomorrow?",
        "Are we gonna play a game today?",
        "Do you wanna go out and eat?",
        "Are you bored or just tired?"
    ]

    #make this function work everything out and decide a similarity score out of the provided dictionaryaaa
    #nltk.download('wordnet')
    #nltk.download('punkt')
    #nltk.download('averaged_perceptron_tagger')
    #For Testing efficiency

    #The program will initialize with these set of variables, they take long so keeping them in ram is good
    commandDic = {
        'Weather':wordnet.synsets("weather", pos='n')[0], #anythin related to weather requests
        'Time':wordnet.synsets("time", pos='n')[4], #try to catch anythin related to time
        'Prognosis':wordnet.synsets("prognosis", pos='n')[0], #weather prediction (forecast)
        'Atmosphere':wordnet.synsets("atmosphere", pos='n')[3]}
    
    commandDicScore = {'Weather':0, 'Time':0, 'Prognosis':0, 'Atmosphere':0} #Dictionary containing all the values
    

    import time
    start = time.time()
    for sentence in sentence_list:
        commandIdentifier(sentence, commandDic, commandDicScore)
        print("-----------------------------------------------------------------------------------------------------------------------------------")
    print(time.time()-start)
    start = time.time()