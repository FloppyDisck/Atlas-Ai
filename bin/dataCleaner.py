#Program built to be used on top of chatite to make the "rasa train" command smoother
import sys
import json

def pprint(comment):
    print(f"[dataCleaner] {comment}")

try:
    commands = sys.argv[1:]
except IndexError:
    pprint("Arguments must be supplied")

for index in range(0, len(commands)):
    command = commands[index]
    if (command == "--nlu-in"):
        raw_nlu = commands[index+1] + "/train/output.json" # chattete_out
        raw_nlu_test = commands[index+1] + "/test/output.json"
    if (command == "--nlu-out"):
        out_nlu = commands[index+1] + "/nlu.json"
        out_nlu_test = commands[index+1] + "/nlu_test.json"


lookup_tables = [["location", "data/locations/countriesLookupNOCAPS.txt"]]

pprint(f"Opening {raw_nlu} & {raw_nlu_test}")

nlu_open = open(raw_nlu, "r")
train_data = json.load(nlu_open)
nlu_open.close()

nlu_open_train = open(raw_nlu_test, "r")
test_data = json.load(nlu_open_train)
nlu_open_train.close()

lookup_tables = []
for value in lookup_tables:
    lookup_tables.append({"name": value[0], "elements": value[1]})

train_data['rasa_nlu_data']['lookup_tables'] = lookup_tables
test_data['rasa_nlu_data']['lookup_tables'] = lookup_tables

pprint(f"Writing to {out_nlu}")
with open(out_nlu, "w") as nlu_open:
    json.dump(train_data, nlu_open)

with open(out_nlu_test, "w") as nlu_test_open:
    json.dump(test_data, nlu_test_open)