from commandDeconstructor import commandIdentifier
from nltk.corpus import wordnet
import sqlite3

#Setup Dictionary
conn = sqlite3.connect('commandDB')
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

commandDicPrimary = {}
commandDicScore = {}
previousCommand = ""
for row in db.fetchall():
        if previousCommand == "":
                previousCommand = row[0]
                synsetList = []
        elif previousCommand != row[0]:
                #Add the list of the dictionary
                commandDicPrimary[previousCommand] = synsetList
                commandDicScore[previousCommand] = 0
                previousCommand = row[0]
                synsetList = []
        
        synsetList.append(wordnet.synsets(str(row[1]), pos=str(row[2]))[int(row[3])])

commandDicPrimary[previousCommand] = synsetList
commandDicScore[previousCommand] = 0

db.execute("""
SELECT cs.StrName, c.StrName, c.StrType, c.IntIndex, f.StrFunction FROM commandsetuptbl cs
        JOIN secondarylisttbl p
        JOIN functiontbl f
        JOIN commandtbl c 
WHERE 
        cs.IntSecondaryList_Id = p.ListId and
        p.Function_Id = f.Id and
        f.Id = c.FunctionId""")

commandDicSecondary = {}
previousCommand = ""
for row in db.fetchall():
        functionName = row[4]
        if previousCommand == "":
                previousCommand = row[0]
                synsetList = []
        elif previousCommand != row[0]:
                #Add the list of the dictionary
                commandDicSecondary[previousCommand] = [functionName, synsetList]
                previousCommand = row[0]
                synsetList = []
        
        synsetList.append(wordnet.synsets(str(row[1]), pos=str(row[2]))[int(row[3])])

commandDicSecondary[previousCommand] = [functionName, synsetList]

print(commandDicPrimary)
print(commandDicScore)
print(commandDicSecondary)

sentence = "How is the weather like today?"

commandIdentifier(sentence, commandDicPrimary, commandDicScore)

print(commandDicScore)