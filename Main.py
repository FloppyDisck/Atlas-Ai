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
