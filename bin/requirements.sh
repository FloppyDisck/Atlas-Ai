#!/bin/bash
pip install rasa_nlu
pip install rasa_nlu[spacy]
python -m spacy download en
python -m spacy download en_core_web_md
python -m spacy link en_core_web_md en --force
pip install rasa_nlu[tensorflow]
pip install rasa_core
pip install rasa-x --extra-index-url https://pypi.rasa.com/simple