#!/bin/bash

##### Variables

# rasa variables
config="config/config.yml"
domain="config/domain.yml"
endpoints="config/endpoints.yml"
model_name="ATLAS_TRAINED_MODEL"
model_path="models/ATLAS_TRAINED_MODEL"

##### Functions

function train_model {

    # chatette variables
    chatette_in="data/generator/master.chatito"
    chatette_out="data/nlu"

    # other settings
    use_python_train=0
    augmentation=50
    cleanup=1

    # process command
    while [ "$1" != "" ]; do
        case $1 in
            -c | --config )     shift
                                config=$1
                                ;;
            -d | --domain )     shift
                                domain=$1
                                ;;
            -n | --model-name ) shift
                                model_name=$1
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
        esac
        shift
    done

    #run chattete and data cleaner
    python -m chatette "$chatette_in" -o "$chatette_out"
    python bin/dataCleaner.py # TODO: integrate with this system (take the json path in and out)

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
        rm data/nlu.json
    fi

}

function run_model {
    
    # settings
    set_interactive=0

    # process command
    while [ "$1" != "" ]; do
        case $1 in
            -c | --config )     shift
                                config=$1
                                ;;
            -d | --domain )     shift
                                domain=$1
                                ;;
            -e | --endpoints )  shift
                                endpoints=$1
                                ;;
            -n | --model-path ) shift
                                model_path=$1
                                ;;
            --interactive )     set_interactive=1
                                ;;
        esac
        shift
    done

    # run actions server
    rasa run actions --actions actions&

    # run
    if [ "$set_interactive" = 1 ]; then
        rasa interactive --model "$model_path" --endpoints "$endpoints" --config "$config" --domain "$domain"
    else
        rasa shell -m "$model_path" --endpoints "$endpoints"
    fi

}

##### Main

if [ "$1" = "--train" ] || [ "$1" = "-t" ]; then
    shift
    train_model
else
    run_model
fi