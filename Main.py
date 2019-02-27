from commandDeconstructor import commandIdentifier
from nltk.corpus import wordnet
import sqlite3

#Dictionary Setup - Use the db to create the dictionary every bootup
conn = sqlite3.connect('commandDB')
db = conn.cursor()
db.execute("""
SELECT cs.StrName, c.StrName, c.StrType, c.IntIndex FROM commandsetuptbl cs
        JOIN primarylisttbl p
        JOIN commandtbl c 
WHERE 
        cs.IntPrimaryList_Id = p.ListId and
        p.IntCommand_Id = c.Id""")

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
SELECT cs.StrName, c.StrName, c.StrType, c.IntIndex FROM commandsetuptbl cs
        JOIN secondarylisttbl p
        JOIN commandtbl c 
WHERE 
        cs.IntSecondaryList_Id = p.ListId and
        p.IntCommand_Id = c.Id""")

commandDicSecondary = {}
previousCommand = ""
for row in db.fetchall():
        if previousCommand == "":
                previousCommand = row[0]
                synsetList = []
        elif previousCommand != row[0]:
                #Add the list of the dictionary
                commandDicSecondary[previousCommand] = synsetList
                previousCommand = row[0]
                synsetList = []
        
        synsetList.append(wordnet.synsets(str(row[1]), pos=str(row[2]))[int(row[3])])

commandDicSecondary[previousCommand] = synsetList

sentence = "How is the weather like today?"
commandIdentifier(sentence, commandDicPrimary, commandDicScore)
print(commandDicScore)