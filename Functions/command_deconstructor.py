# The program will take an input string an process it to identify what its trying to express
import os
import sqlite3
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

class CommandProcessing:

    def __init__(self, dbPath = 'commandDB'):
        #Dictionary Setup - Use the db to create the dictionary every bootup
        conn = sqlite3.connect(dbPath)
        db = conn.cursor()
        db.execute("""
        SELECT cs.StrName, c.StrName, c.StrType, c.IntIndex FROM commandsetuptbl cs
                JOIN primarylisttbl p
                JOIN functiontbl f
                JOIN commandtbl c 
        WHERE 
                cs.IntPrimaryList_Id = p.ListId and
                p.Function_Id = f.Id and
                f.Id = c.FunctionId""")

        self.commands = {}

        for row in db.fetchall():
            if (row[0] not in self.commands):
                self.commands[row[0]] = [[wordnet.synsets(str(row[1]), pos=str(row[2]))[int(row[3])]], {}]
            else:
                self.commands[row[0]][0].append(wordnet.synsets(str(row[1]), pos=str(row[2]))[int(row[3])])

        db.execute("""
        SELECT cs.StrName, c.StrName, c.StrType, c.IntIndex, f.StrFunction FROM commandsetuptbl cs
                JOIN secondarylisttbl p
                JOIN functiontbl f
                JOIN commandtbl c 
        WHERE 
                cs.IntSecondaryList_Id = p.ListId and
                p.Function_Id = f.Id and
                f.Id = c.FunctionId""")

        for row in db.fetchall():
            if (row[4] not in self.commands[row[0]][1]):
                self.commands[row[0]][1][row[4]] = [wordnet.synsets(str(row[1]), pos=str(row[2]))[int(row[3])]]
            else:
                self.commands[row[0]][1][row[4]].append(wordnet.synsets(str(row[1]), pos=str(row[2]))[int(row[3])])

    def test_tokenizer(self):
        # Will tokenize the sentence with the NLTK library
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
        grammar_list = [grammar, backup_grammar] # List composed of the params

        ne = set()
       while len(ne) == 0:

            chunker = nltk.RegexpParser(grammar, trace=0)
            ne.clear()
            chunk = chunker.parse(nltk.pos_tag(nltk.word_tokenize(self.sentence)))
            for tree in chunk.subtrees(filter=lambda t: t.label() == 'NP'):

                for child in tree.leaves(): # This way allows for implementing the whole list
                    ne.add(child)
                # ne.add(' '.join([child[0] for child in tree.leaves()]))
                    
        return ne

    def analize_sentence(self, sentence):
        self.sentence = sentence # Input sentence
        self.commandScore = {} # Initialize the score of the words

        #Parse the file to remove unneeded words
        self.extractedSentence = self.extract_NN() # Cleanup the sentence
        self.extractedSentenceDic = {}
        for item in self.extractedSentence:
            try:
                #Turn the word into a synset readable by NLTK
                # Replace the first letter with a capitalized version
                betterItem = item[0].replace(item[0][0], item[0][0].upper(), 1)

                # Populate the dictionary with a list of synsets for that word
                self.extractedSentenceDic[betterItem] = wordnet.synsets(item[0].lower(), pos=item[1][0].lower())
            except KeyError:
                # print("Did not find {} in the wordnet!".format(item)) #Error code when word is not found
                pass

        #Primary Command Pass
        # Iterate through all the values of the dictionary "commands"
        for command, commandSynsets in self.commands.items():

            # Go through all the values in the sentence dictionary
            for wordSynsets in self.extractedSentenceDic.values():

                # Go through each synset in the list
                for wordSynset in wordSynsets:

                    # Go through each test synset to identify the sentence goal
                    for commandSynset in commandSynsets[0]:

                        #The wup_similarity function returns either none or a value from 0 to 1.0
                        simScore = commandSynset.wup_similarity(wordSynset)

                        #If the simscore is none then ignore
                        if (not simScore):
                            # print("Not related")
                            pass

                        #If the simScore is over 0.8 then continue
                        elif (simScore >= 0.8):
                            #If the current command is not in the score dic then add it
                            if (command not in self.commandScore.keys()):
                                #Add the value
                                self.commandScore[command] = simScore
                            #If the current command's score (simScore) is greater than the dic
                            elif (self.commandScore[command] < simScore):
                                #Replace the value
                                self.commandScore[command] = simScore

        #Secondary Command Pass
        returnArgs = {}
        subArgs = {}
        if (len(self.commandScore) == 1):
            mainCommand = list(self.commandScore.keys())[0] # Get the key of the dictionary
            #TODO: normally process the command identifier
            #return {"Weather":{"Time":"today", "Location":"Puerto Rico"}}
            arguments = self.commands[mainCommand][1] #Get the secondary commands

            # Get the arg word and arg synsets list
            for argument, argumentSynsets in arguments.items(): 
                    
                # Get the sentence word and its arguments
                for word, wordSynsets in self.extractedSentenceDic.items(): 

                    # Iterate through the list
                    for argumentSynset in argumentSynsets: 

                        # Iterate through the list of said words
                        for wordSynset in wordSynsets:

                            #The wup_similarity function returns either none or a value from 0 to 1.0
                            simScore = argumentSynset.wup_similarity(wordSynset)
                            #If the simscore is none then ignore
                            if (not simScore):
                                # print("Not related")
                                pass

                            #If the simScore is over 0.8 then continue
                            elif (simScore >= 0.8):

                                if (argument not in subArgs.keys()):
                                    #Add the value
                                    subArgs[argument] = set()
                                    subArgs[argument].add(word)
                                #If the current command's score (simScore) is greater than the dic
                                else:
                                    subArgs[argument].add(word)
                            
                    #for item in self.extractedSentence
            returnArgs[mainCommand] = subArgs          
            return returnArgs
        elif (len(self.commandScore) == 0):
            return returnArgs
        else:
            #TODO: find the most optimal command goal
            return returnArgs

if __name__ == "__main__":

    #Quick code testing with a big list

    try:

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
            "What's the weather expected to be tomorrow?",
            "What's the temperature?",
            "How's the weather?",
            "What's it like outside?",
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
        
        #Start running the sentences
        for sentence in sentence_list:

            #Make synset of sentence
            command = CommandProcessing()
            analizedSentence = command.analize_sentence(sentence)

            print(analizedSentence)

    except LookupError:

        print("Performing first time setup of NLTK files")

        nltk.download('wordnet')
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')