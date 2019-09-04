#Program built to be used on top of chatite to make the "rasa train" command smoother

import json

def pprint(comment):
    print(f"[dataCleaner] {comment}")

raw_nlu = "data/nlu/train/output.json"
out_nlu = "data/nlu.json"
lookup_tables = [["location", "data/locations/countriesLookupNOCAPS.txt"]]

pprint(f"Opening {raw_nlu}")

open_file = open("data/nlu/train/output.json", "r")
train_data = json.load(open_file)
open_file.close()

lookup_tables = []
for value in lookup_tables:
    lookup_tables.append({"name": value[0], "elements": value[1]})

train_data['rasa_nlu_data']['lookup_tables'] = lookup_tables

pprint(f"Writing to {out_nlu}")
with open(out_nlu, "w") as open_file:
    json.dump(train_data, open_file)