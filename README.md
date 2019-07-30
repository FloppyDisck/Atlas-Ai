# Atlas-Ai

Atlas AI is a proof of concept for a completely open source home automation assistant with features aimed at facilitating the process of adding more features and commands. The concept is to incorporate the Rasa framework to an easy learning experience for the user and the assistant.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

NOTE: This program has been tested with python 3.6 only

Before starting you'll need to have a few libraries installed. First open console in the main program folder and then copy the line below and run it.

It is recomended to setup a vm for this python version, first install miniconda. Then setup a python vm.
```
conda create -n env-name python=3.6
```
Then to start using your vm.
```
conda activate env-name
```
Finally install the required python packages.
```
pip install -r requirements.txt
```

NOTE: Some actions require enviroment variables to be setup (for the APIs)
In linux input the following command
```
sudo -H gedit /etc/enviroment
```
Then inside the file write
```
ENV_VARIABLE_NAME="variableValue"
```
Save and then log out of the account so the variables are started.

### Training

Before training you'll need to setup the datasets and understand how they work.
First you need to train the model to understand the specific intent, head over to /data/nlu.md
A great tutorial for the nlu.md file can be found [here](https://rasa.com/docs/rasa/nlu/training-data-format/)

Once this is done you'll need to work on the /data/stories.md and /configs/domain.yml
Information on [stories](https://rasa.com/docs/rasa/core/stories/) and [domain](https://rasa.com/docs/rasa/core/domains/) can be found in their respective links.

Later if you have any custom actions defined they'll be edited on the actions.py file. Information on actions can be found [here](https://rasa.com/docs/rasa/core/actions/).

Once all of this is set and youre ready to begin training just run train.sh file and it should train everything.
```
bash /bin/train.py
```

If you just want to test the latest NLU training data with some written examples found in /bin/modelTrain.py
```
bash /bin/train.py model
```

## Testing Atlas

Before testing, download and compile [duckling](https://github.com/facebook/duckling). (This is used for time, date and distance recognition)

After compilation in the duckling directory open an example file.
```
stack exec duckling-example-exe
```

Now run the actions local server and dialogue program
```
bash /bin/run.sh /models/--latest--.tar.gz
```

If you want to train while you test run is like this.
```
bash /bin/run.sh /models/--latest--.tar.gz learn
```

## Authors

* **Guy S Garcia** - *Initial work* - [FloppyDisck](https://github.com/FloppyDisck)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* This project would not be even close to possible without the Rasa framework and Spacy
