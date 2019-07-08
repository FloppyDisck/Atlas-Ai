import simplejson as json
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu.model import Interpreter
from rasa_nlu import config
from rasa_nlu.test import run_evaluation

# loading the nlu training samples
training_data = load_data("data/nlu.md")

# trainer to educate our pipeline
trainer = Trainer(config.load("config.yml"))

# train the model!
interpreter = trainer.train(training_data)

# store it for future use
model_directory = trainer.persist("./models/nlu", fixed_model_name="current")

# open current model
#interpreter = Interpreter.load(nlu_path)

#quick test to see if it was trained correctly
def pprint(o): 
    #out = json.loads(o)
    print(f'''
    Sentence: {o["text"]}
    Intent: {o["intent"]["name"]}
    Confidence: {o["intent"]["confidence"]}
    Entities: {[i["value"] for i in o["entities"]]}''')
    #print(json.dumps(o, indent=2))
    
pprint(interpreter.parse("Will it be raining today"))
pprint(interpreter.parse("Will it be hot"))
pprint(interpreter.parse("How much more will it rain in Africa"))
pprint(interpreter.parse("How clowdy is it in San Francisco"))

#More robust metrics report
run_evaluation("data/nlu.md", model_directory) #Recommended to have a custom test set


#TODO: check if dividing my connectors (and, or) could solve the structured request problem
#TODO: trained model not properly detecting location data