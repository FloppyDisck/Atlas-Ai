import os
os.system("source /etc/environment")
variableName = ""
variableValue = ""

while True:
    if variableName == "":
        variableName = input("Input the name of the variable: ")
    else:
        inputText = input("Input the value of the variable or write back to go back: ")
        if inputText == "back" or "":
            variableName = ""
        else:
            inputText = variableValue
            os.environ[variableName] = str(variableValue)
            print(f"{variableName} saved as {os.environ.get(variableName)}")
            variableValue = ""
            variableName = ""
