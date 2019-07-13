import os

def get_var(variable):
    #Check if the enviroment variable exists
    var = os.environ["variable"]
    return var