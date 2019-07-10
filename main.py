#pip install rasa_nlu[spacy]
#python3 -m spacy download en
#python3 -m spacy download en_core_web_md
#python3 -m spacy link en_core_web_md en
#(pipeline)pip install rasa_nlu[tensorflow]

#Starting the Bot

from rasa_core.agent import Agent
from rasa_core import utils
from rasa_core.utils import EndpointConfig

actionConfig = utils.read_yaml_file('configs/endpoints.yml')
action_endpoint_url = actionConfig["action_endpoint"]["url"]
agent = Agent.load('models/dialogue', interpreter='models/current/nlu', action_endpoint=EndpointConfig(url=action_endpoint_url))

print("Testing the bot...")
while True:
    a = input()
    if a == 'stop':
        break
    responses = agent.handle_message(a)
    for response in responses:
        print(response)