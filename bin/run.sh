#!/bin/bash

##### Variables

# process variables
run_model=1
train_model=0
test_model=0

# rasa variables
config=config/config.yml
domain=config/domain.yml
endpoints=config/endpoints.yml

model_name=ATLAS_TRAINED_MODEL # train variable
model_path=models/ATLAS_TRAINED_MODEL # run variable

# json paths
json_out=data

# chatette variables
chatette_in=data/generator/master.chatito
chatette_out=data/nlu

# dataCleaner

# other settings
use_python_train=0 # use custom python training program
augmentation=50 # the quantity of data augmentation
cleanup=1 # delete .json files; default yes
set_interactive=0 # activate interactive

##### Functions

function _train_model {

    #run chattete and data cleaner
    #echo $chat_out
    echo $chatette_out
    python -m chatette $chatette_in -o $chatette_out
    python bin/dataCleaner.py --nlu-in $chatette_out --nlu-out $json_out

    #run training
    if [ "$use_python_train" = true ]; then
        python bin/modelTrain.py
    else
        rasa train -c "$config" -d "$domain" --fixed-model-name "$model_name" --augmentation "$augmentation" --verbose # TODO still saving out of ATLAS_TRAINED_MODEL
    fi

    if [ "$cleanup" = 1 ]; then
        echo Deleting contents in "$chatette_out"
        rm -rf "$chatette_out"
        echo Removing data/nlu.json # TODO: positional argument for the dataCleaner.py out
        rm $json_out/nlu.json
        rm $json_out/nlu_test.json
    fi

}

function _test_model {
    #rasa test 
    echo rasa test has not been implemented yet
}

function _run_model {

    # run actions server
    rasa run actions --actions actions&

    # run
    if [ "$set_interactive" = 1 ]; then
        rasa interactive --model "$model_path" --endpoints "$endpoints" --config "$config" --domain "$domain"
    else
        rasa shell -m "$model_path" --endpoints "$endpoints"
    fi

}

##### Main TODO: add --help documentation

# process command
while [ "$1" != "" ]; do
    case $1 in
        -t | --train )      shift
                            train_model=1
                            run_model=0
                            ;;
        --test )            shift
                            test_model=1
                            run_model=0
                            ;;
        -c | --config )     shift
                            config=$1
                            ;;
        -d | --domain )     shift
                            domain=$1
                            ;;
        -e | --endpoints )  shift
                            endpoints=$1
                            ;;
        -n | --model-name ) shift
                            model_name=$1
                            ;;
        -n | --model-path ) shift
                            model_path=$1
                            ;;
        -a | --augment )    shift
                            augmentation=$1
                            ;;
        --chatette-in )     shift
                            chatette_in=$1
                            ;;
        --chattete-out )    shift
                            chatette_out=$1
                            ;;
        --use-python )      use_python_train=1
                            ;;
        --no-cleanup )      cleanup=0
                            ;;
        --interactive )     set_interactive=1
                            ;;
    esac
    shift
done

if [ "$train_model" = 1 ]; then
    _train_model
fi

if [ "$test_model" = 1 ]; then
    _test_model
fi

if [ "$run_model" = 1 ]; then
    _run_model
fi