#The program will take an input string an process it to identify what its trying to express

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

class CommandProcessing:

    def __init__(self, sentence, commands):
        self.sentence = sentence
        self.commands = commands
        self.commandScore = {}

    def test_tokenizer(self):
        return nltk.pos_tag(nltk.word_tokenize(self.sentence))

    def extract_NN(self): #TODO: Study how to properly make a regexParser string
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
            chunk = chunker.parse(nltk.pos_tag(nltk.word_tokenize(self.sentence)))
            for tree in chunk.subtrees(filter=lambda t: t.label() == 'NP'):

                for child in tree.leaves(): #this way allows for implementing the whole list
                    ne.add(child)
                #ne.add(' '.join([child[0] for child in tree.leaves()]))

            if (len(ne) > 0): #If condition is not met Run the program again with the next value
                break
                    
        return ne

    def primary_command_identifier(self):

        #print(test_tokenizer()) #Print tokenized sentence
        extractedSentence = self.extract_NN()
        for command, commandSynsets in self.commands.items():

            for item in extractedSentence:
                #print(item) #Print the list with both the word and type
                try:
                    for word in wordnet.synsets(item[0].lower(), pos=item[1][0].lower()): #Parse the word
                        #print(word) #Print the wordnet word related to the item list

                        for commandSynset in commandSynsets[0]:

                            simScore = commandSynset.wup_similarity(word)
                            #print(simScore) #Print the similarity score achieved (max 1.0)

                            if (not simScore):
                                #print("Not related")
                                pass

                            elif (simScore > 0.8):
                                if (command not in self.commandScore.keys()):
                                    self.commandScore[command] = simScore
                                
                                elif (self.commandScore[command] < simScore):
                                    self.commandScore[command] = simScore

                except KeyError:
                    #print("Did not find {} in the wordnet!".format(item)) #Error code when word is not found
                    pass

    def secondary_command_identifier(self):
        if (len(self.commandScore) == 1):
            #TODO: normally process the command identifier
            #return {"Weather":{"Time":"today", "Location":"Puerto Rico"}}
            return True
        elif (len(self.commandScore) == 0):
            return False
        else:
            #TODO: find the most optimal command goal
            return True

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