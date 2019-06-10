import os
import sqlite3
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

#TODO: replace variables with primaryKey and secondaryKey

class CommandProcessing:

    def __init__(self, dbPath = 'Modules/DataBases/commandDB'):
        """
        Initializes an instance of the command processor

        When the object is created it makes a map called commands
        this map contains all the main commands and sub commands
        recognized by the processor 

        Args:
            dbPath: The path for the database

        Returns:
            Nothing
        """

        #Map Setup - Use the db to create the dictionary every bootup
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

        #Begin an empty map of commands
        self.commands = {}

        #Populate the commands
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

        #Populate sub commands
        for row in db.fetchall():
            if (row[4] not in self.commands[row[0]][1]):
                self.commands[row[0]][1][row[4]] = [wordnet.synsets(str(row[1]), pos=str(row[2]))[int(row[3])]]
            else:
                self.commands[row[0]][1][row[4]].append(wordnet.synsets(str(row[1]), pos=str(row[2]))[int(row[3])])

    def __test_tokenizer(self):
        """
        Uses the NLTK library to tokenize the sentence variable

        Args:
            self.sentence: This is the input sentence.

        Returns:
            Returns the tokenized sentence.
        """
        # Will tokenize the sentence with the NLTK library
        return nltk.pos_tag(nltk.word_tokenize(self.sentence))

    def extract_NN(self): #TODO: Study how to properly make a regexParser string
        """
        This function further filters the sentence.

        The sentence is passed through this regex parser
        to remove the uneeded junk words and improve
        time efficiency.

        Args:
            self.sentence: This is the input sentence.

        Returns:
            The parsed sentence.
        """

        #Parsers
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
        grammar_list = [grammar, backup_grammar]

        #Create empty set to be popuated
        ne = set()

        #While the set has not been populated keep trying parsers
        while len(ne) == 0:

            chunker = nltk.RegexpParser(grammar, trace=0)
            ne.clear()
            chunk = chunker.parse(nltk.pos_tag(nltk.word_tokenize(self.sentence)))
            for tree in chunk.subtrees(filter=lambda t: t.label() == 'NP'):

                #ne.add(' '.join([child[0] for child in tree.leaves()]))
                for child in tree.leaves(): # This way allows for implementing the whole list
                    ne.add(child)
                    
        return ne

    def analize_sentence(self, sentence, onlySecondary=False, mainCommand=None):
        """
        Clean up and analize the sentence to find its objective,

        The input sentence will be passed through a regex,
        then scored in comparison to the different commands
        and when the main command is spotted the sub commands
        will be analized to find the arguments.

        Args:
            sentence: This is the input sentence.
            onlySecondary: Asks to skip the first part to run the secondary command identifier
            mainCommand: The replacement key when we put onlySecondary = True

        Returns:
            Returnds a map where the key is the main command found
            then the value is another map where each key is an
            argument or subcommand that has a value of the word
            related to it.
        """
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
                pass

        #Primary Command Pass NOTE:onlySecondary has to be False
        # Iterate through all the values of the dictionary "commands"
        #TODO: graph both maps and look for better iteration methods
        if (onlySecondary == False): 

            for command, commandSynsets in self.commands.items():
                # Go through all the values in the sentence dictionary
                #TODO: Can we shorten this loop?
                for wordSynsets in self.extractedSentenceDic.values():
                    # Go through each synset in the list
                    for wordSynset in wordSynsets:

                        # Go through each test synset to identify the sentence goal
                        #TODO: why loop two times in map?
                        for commandSynset in commandSynsets[0]:

                            #The wup_similarity function returns either none or a 
                            # value from 0 to 1.0
                            simScore = commandSynset.wup_similarity(wordSynset)

                            #If the simscore is none then ignore
                            if (not simScore):
                                # print("Not related")
                                pass

                            #If the simScore is over 0.8 then continue
                            elif (simScore >= 0.8):
                                #If the current command is not in the score dic then 
                                # add it
                                if (command not in self.commandScore.keys()):
                                    #Add the value
                                    self.commandScore[command] = simScore
                                #If the current command's score (simScore) is greater 
                                # than the dic
                                elif (self.commandScore[command] < simScore):
                                    #Replace the value
                                    self.commandScore[command] = simScore     

        returnArgs = {}
        subArgs = {}
        sentenceOUT = [[word] for word in self.sentence.split(" ")] #prepare output sentence
        
        if (len(self.commandScore) == 1) or (onlySecondary == True):
            
            # Note: mainCommand or primaryKey? which sounds better?
            mainCommand = list(self.commandScore.keys())[0] # Get the dic key

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

                            #The wup_similarity function returns either none or a 
                            # value from 0 to 1.0
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

                                #Create sentence with the secondary list identifications
                                for index in range(0, len(sentenceOUT)): #loop word by word
                                    #When the current word is found in the sentence continue
                                    if word.lower() == sentenceOUT[index][0].lower():
                                        #If the word has no argument then add one
                                        if len(sentenceOUT[index]) == 1:
                                            sentenceOUT[index].append(argument)
                                        #If not then just check if it exists to add it
                                        else:    
                                            if argument not in sentenceOUT[index][1:]:
                                                sentenceOUT[index].append(argument)

                                #If the current command's score (simScore) is 
                                # greater than the dic
                                else:
                                    subArgs[argument].add(word)
                            
                    #for item in self.extractedSentence
            returnArgs[mainCommand] = subArgs  

        elif (len(self.commandScore) == 0):
            pass
        else:
            #Fallback when multiple items are returned
            #TODO: find the most optimal command goal
            pass

        returnData = [returnArgs, sentenceOUT]        
        return returnData

if __name__ == "__main__":

    #Quick code testing with a big list
    #Make synset of sentence
    command = CommandProcessing()

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
            "Is it a Beautiful day for a walk?",
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
            analizedSentence = command.analize_sentence(sentence)

            print(analizedSentence)

    except LookupError:

        print("Performing first time setup of NLTK files")

        nltk.download('wordnet')
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')