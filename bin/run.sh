#!/bin/bash
#run giving the .tar.gz file link as argument and optional run method
if [ $2 = "learn" ]; then
    rasa run actions --actions actions&
    rasa interactive --model $1 --endpoints config/endpoints.yml
else
    rm models/run/ --recursive || true
    mkdir models/run/
    tar xvzf $1 -C models/run/
    python main.py
fi