from Modules import module_manager
from Modules import command_deconstructor

command = command_deconstructor.CommandProcessing("Modules/DataBases/commandDB")
moduleManager = module_manager.Module_Manager()
moduleManager.boot_manager()

sentence = "What is the weather in Spain tomorrow"
print(sentence)

#TODO: 
#If wifi enabled
#       GetVPNServer.py runs to connect in a secure way

#TODO: make this loop so incomplete calls can be completed with subsequent sentences
#TODO: every call returns [status, sentence] status can mean call completed or call incomplete

analizedSentence = command.analize_sentence(sentence)
analizedSentence_secondary = command.analize_sentence(sentence, True, 'Weather')
#Voice to text ends here

#Returns a dictionary where the key is the command and the value is a list with 
# 0.Dictionary with key = secondary command and value = word 
# 1.Sentence list broken into lists where the second value is the secondary command
#Example:
#       In: What is the weather in Spain tomorrow
#       Out: {'Weather': [{'Time': {'Tomorrow'}}, [['What'], ['is'], ['the'], ['weather'], ['in'], ['Spain'], ['tomorrow', 'Time']]]}
print(analizedSentence, analizedSentence_secondary)

if (len(analizedSentence) > 0):
        #Continue
        pass
        #moduleManager.runtime_manager(analizedSentence, sentence)
        
else:
        #Display error that command was not understood
        pass