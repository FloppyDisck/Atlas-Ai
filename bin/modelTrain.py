import simplejson as jsomln
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu.model import Interpreter
from rasa_nlu import config
from rasa_nlu.test import run_evaluation

# loading the nlu training samples
training_data = load_data("data/nlu/train/output.json")

# trainer to educate our pipeline
trainer = Trainer(config.load("config/config.yml"))
#Using duckling server for quantification classification stack exec duckling-example-exe
#c libraries https://guide.aelve.com/haskell/missing-dependency-on-a-foreign-library-vf6h3d0p

# train the model!
interpreter = trainer.train(training_data)

#quick test to see if it was trained correctly
def pprint(o): 
    #out = json.loads(o)
    print(f'''
    Sentence: {o["text"]}
    Intent: {o["intent"]["name"]}
    Confidence: {o["intent"]["confidence"]}
    Entities: {[i["value"] for i in o["entities"]]}''')
    #print(json.dumps(o, indent=2))

testSentences = ["Could you please remind me to sleep tonight?", "Can you please notify me to study at 5pm?", 
                "Remind me to activate the server", "Set a reminder for today to feed my gecko", 
                "Set reminder for tomorrow at ten thirty pm", "Remind me to turn off the lights tomorrow"]

for sentence in testSentences:
    pprint(interpreter.parse(sentence))
