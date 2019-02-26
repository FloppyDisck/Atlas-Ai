from commandDeconstructor import commandIdentifier
from nltk.corpus import wordnet
import sqlite3

#Setup Dictionary
conn = sqlite3.connect('commandDB')
db = conn.cursor()
db.execute("""
SELECT cs.StrName, c.StrName, c.StrType, c.IntIndex FROM commandsetuptbl cs
        JOIN primarylisttbl p
        JOIN commandtbl c 
WHERE 
        cs.IntPrimaryList_Id = p.ListId and
        p.IntCommand_Id = c.Id""")

commandDic = {}
commandDicScore = {}

previousCommand = ""
for row in db.fetchall():
        if previousCommand == "":
                previousCommand = row[0]
                synsetList = []
        elif previousCommand != row[0]:
                #Add the list of the dictionary
                commandDic[previousCommand] = synsetList
                commandDicScore[previousCommand] = 0
                previousCommand = row[0]
                synsetList = []
        
        synsetList.append(wordnet.synsets(str(row[1]), pos=str(row[2]))[int(row[3])])

commandDic[previousCommand] = synsetList
commandDicScore[previousCommand] = 0

print(commandDic) 

sentence = "is it going to rain tomorrow?"

commandIdentifier(sentence, commandDic, commandDicScore)