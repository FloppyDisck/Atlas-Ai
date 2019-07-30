#!/bin/bash
#run giving the .tar.gz file link as argument
rm models/run/ --recursive || true
mkdir models/run/
tar xvzf $1 -C models/run/
python main.py