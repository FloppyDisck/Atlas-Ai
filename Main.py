from commandDeconstructor import CommandProcessing
from nltk.corpus import wordnet
import sqlite3

#Dictionary Setup - Use the db to create the dictionary every bootup
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

commandDic = {}

for row in db.fetchall():
        if (row[0] not in commandDic):
                commandDic[row[0]] = [[wordnet.synsets(str(row[1]), pos=str(row[2]))[int(row[3])]], {}]
        else:
                commandDic[row[0]][0].append(wordnet.synsets(str(row[1]), pos=str(row[2]))[int(row[3])])

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
        if (row[4] not in commandDic[row[0]][1]):
                commandDic[row[0]][1][row[4]] = [wordnet.synsets(str(row[1]), pos=str(row[2]))[int(row[3])]]
        else:
                commandDic[row[0]][1][row[4]].append(wordnet.synsets(str(row[1]), pos=str(row[2]))[int(row[3])])

#Voice to text happens here
print(commandDic)

sentence = "How is the weather like today?"
command = CommandProcessing(sentence, commandDic)
#Voice to text ends here

command.primary_command_identifier() #First passthrough of the command

print(command.secondary_command_identifier())

if (len(command.secondary_command_identifier()) > 0):
        #Continue
        pass
else:
        #Display error that command was not understood
        pass