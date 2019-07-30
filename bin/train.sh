#!/bin/bash
#If user inputs model at the end it runs a simpler trainer with a sentence reviewer
python -m chatette data/generator/master.chatito -o data/nlu
python bin/dataCleaner.py
if [ $1 = "model" ]; then
    python bin/modelTrain.py
else
    rasa train -c config/config.yml -d config/domain.yml
fi