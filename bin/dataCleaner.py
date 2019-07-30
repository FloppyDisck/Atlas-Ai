#Program built to be used on top of chatite to make the "rasa train" command smoother

import json

def pprint(comment):
    print(f"[dataCleaner] {comment}")

rawNLU = "data/nlu/train/output.json"
outNLU = "data/nlu.json"
lookupTables = [["location", "data/locations/countriesLookupNOCAPS.txt"]]

pprint(f"Opening {rawNLU}")

openFile = open("data/nlu/train/output.json", "r")
trainData = json.load(openFile)
openFile.close()

lookup_tables = []
for value in lookupTables:
    lookup_tables.append({"name": value[0], "elements": value[1]})

trainData['rasa_nlu_data']['lookup_tables'] = lookup_tables

pprint(f"Writing to {outNLU}")
with open(outNLU, "w") as openFile:
    json.dump(trainData, openFile)