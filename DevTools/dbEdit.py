import os
import sqlite3

from nltk.corpus import wordnet

# dbEdit is a command line app that allows editing of the AI database

#How it works

#commandsetuptbl is what groups each command
#   Id is the int that defines it
#   StrName is the name of the command
#   IntPrimaryList_Id is the int that defines which list is used
#   IntSecondaryList_Id is the same as above 
#   NOTE: these two can have duplicated that point to multiple functionTbls

#FunctionTbl is where functions are setup (known as lists of synsets)
#   Id is the int that defines it
#   StrFunction is the name of it

#commandtbl is where the synsets are stored
#   Id refers to the int that defines it
#   StrName is the synset word
#   StrType is the word type, default n
#   IntIndex is the number in the list
#   Function_Id is the id that points to FunctionTbl.Id

#primarylisttbl and secondarylisttbl
#   ListId points to commandsetuptbl.Int(Primary, Secondary)List_Id
#   Function_Id points to FunctionTbl.Id 
#   NOTE: there could be duplicated in ListID and point to different 
#       Function_Id making the intended use of a list justified




def display_title_bar():
    # Displays a title bar.
              
    print("*******************************")
    print("*** Atlas-Ai SQLite3 Editor ***")
    print("*******************************")

def functionStandard(oldString):
    newString = oldString.lower()
    newString = newString.replace(newString[0], newString[0].upper(), 1)
    return newString

def check_List():
    pass

#Setup DB path
dbName = 'Modules/DataBases/commandDB'
dbPath = os.getcwd() + '/' + dbName

#Initialize path
conn = sqlite3.connect(dbPath)

display_title_bar()

notExit = True

while notExit:
    #Take a command and split it by space bars
    command = input()
    command = str(command).split(" ")

    if command[0] in ['fix', 'f']:
        if command[1] in ['path', 'p']:
            #dbPath = os.getcwd() + '/' + dbName
            pass

    if command[0] in ['show', 's']:
        db = conn.cursor() 
        if command[1] in ['path', 'p']:
            print(dbPath)
        if command[1] in ['data', 'd']: #show data in a raw form
            print(f'\nShowing all data in tables of {dbName}')
            db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
            
            for row in db.fetchall():#iterate through everything and print the values
                print(f'\t{row}')
                queryData = db.execute(f"SELECT * FROM {row[0]}")
                for row in queryData:
                    print(f'\t\t{row}')

        if command[1] in ['functions', 'func', 'f']:#show the function table and its values
            print(f'\nShowing all functions in {dbName}')
            db.execute('SELECT * FROM functiontbl')
            functiontbl = []
            for row in db.fetchall():
                functiontbl.append(row)

            db.execute('SELECT * FROM commandtbl')
            commandtbl = []
            for row in db.fetchall():
                commandtbl.append(row)

            for functionValue in functiontbl:
                print(f"\t{functionValue[1]}:")
                for commandValue in commandtbl:
                    if functionValue[0] == int(commandValue[4]):
                        print(f"\t|-> {commandValue[1]}.{commandValue[2]}.{commandValue[3]}")
                print("")

        if command[1] in ['data+', 'd+', 'dp']:#show all the data in a pretty edited form (same as 'show data')
            print(f'\nShowing all pretty data in {dbName}')
            db.execute('SELECT * FROM commandsetuptbl')
            commandsetuptbl = []
            for row in db.fetchall():
                commandsetuptbl.append(row)

            db.execute('SELECT * FROM functiontbl')
            functiontbl = []
            for row in db.fetchall():
                functiontbl.append(row)

            db.execute('SELECT * FROM commandtbl')
            commandtbl = []
            for row in db.fetchall():
                commandtbl.append(row)

            db.execute('SELECT * FROM primarylisttbl')
            primarylisttbl = []
            for row in db.fetchall():
                primarylisttbl.append(row)

            db.execute('SELECT * FROM secondarylisttbl')
            secondarylisttbl = []
            for row in db.fetchall():
                secondarylisttbl.append(row)

            for commandsetupVal in commandsetuptbl:
                print(f'\t{commandsetupVal[1]}:\n\t|-> Primary List:')
                for primarylistVal in primarylisttbl:
                    if primarylistVal[0] == commandsetupVal[2]:
                        for functionVal in functiontbl:
                            if functionVal[0] == primarylistVal[1]:
                                print(f'\t|   |-> {functionVal[1]}:')
                                for commandValue in commandtbl:
                                    if functionVal[0] == int(commandValue[4]):
                                        print(f"\t|   |   |-> {commandValue[1]}.{commandValue[2]}.{commandValue[3]}")
                print('\t|-> Secondary List:')
                for secondarylistVal in secondarylisttbl:
                    if secondarylistVal[0] == commandsetupVal[3]:
                        for functionVal in functiontbl:
                            if functionVal[0] == secondarylistVal[1]:
                                print(f'\t|   |-> {functionVal[1]}:')
                                for commandValue in commandtbl:
                                    if functionVal[0] == int(commandValue[4]):
                                        print(f"\t|   |   |-> {commandValue[1]}.{commandValue[2]}.{commandValue[3]}")

    if command[0] in ['create', 'c']:#This stems to everything related to data creation in the database
        db = conn.cursor() 
        if command[1] in ['function', 'func', 'f']:#it creates a function and its values if added with them

            #Check if function exists, if not create it
            strFunction = functionStandard(command[2])

            db.execute('SELECT * FROM functiontbl f WHERE f.StrFunction = ?', [strFunction])
            if not db.fetchall():
                db.execute('INSERT INTO functiontbl (StrFunction) VALUES (?)', [strFunction])
                print(f'Successfully added {strFunction}')
            else:
                print(f'{strFunction} already in db')
            
            #Check if aditional arguments are added, then check if those synsets exist, if not add them
            if len(command) >= 4:
                #name.type.index
                #c f name.type.index name.type.index name.type.index
                #or c f 
                for index in range(3, len(command)):
                    rawCommand = command[index]
                    while rawCommand != 'skip':
                        synCommand = str(rawCommand).split(".")
                        synCommand[1] = synCommand[1].lower()
                        if len(synCommand)  == 3 :
                            try:
                                wordnet.synsets(str(synCommand[0]), pos=str(synCommand[1]))[int(synCommand[2])]

                                db.execute('SELECT * FROM functiontbl f WHERE f.StrFunction = ?', [strFunction])
                                functionIndex = db.fetchone()[0]

                                commandSet = [synCommand[0], synCommand[1], synCommand[2], functionIndex]

                                db.execute('INSERT INTO commandtbl (StrName, StrType, IntIndex, FunctionId) VALUES (?, ?, ?, ?)', commandSet)
                                rawCommand = 'skip' #no errors found skipping

                            except IndexError:
                                print(f'{synCommand[0]} is not a valid word found in the synset or expected "name.type.index" and received {rawCommand}')
                                rawCommand = input('Please enter the correct value or type skip to ignore this value: ')
                                
        if command[1] in ['command', 'c']:

            #Check if the required ammout of arguments are provided
            if len(command) == 5:
                strCommand = functionStandard(command[2])

                #Check if the provided lists exist, command[3] and command[4]
                forContinue = True
                listlist = ['primarylisttbl', 'secondarylisttbl']
                for index in range(3, 5):
                    db.execute(f'SELECT * FROM {listlist[index - 3]} l WHERE l.ListId = ?', [command[index]])
                    if not db.fetchall():
                        forContinue = False
                        print(f'{listlist[index - 3]} index {command[index]} does not exist.')

                #When the lists are proven to exist check if the commandsetup exists, if so update it, if not create it
                if forContinue == True:
                    db.execute('SELECT * FROM commandsetuptbl c WHERE c.StrName = ?', [strCommand])
                    if not db.fetchall():
                        db.execute('INSERT INTO commandsetuptbl (StrName, IntPrimaryList_Id, IntSecondaryList_Id) VALUES (?, ?, ?)', [strCommand, command[3], command[4]])
                        print(f'Successfully added {strCommand}.')
                    else:
                        print(f'Successfully updated {strCommand}.')
                        db.execute('UPDATE commandsetuptbl SET IntPrimaryList_Id = ?, IntSecondaryList_Id = ? WHERE StrName = ?', ([command[3]], [command[4]], [strCommand]))
            else:
                print('Command criteria not met! expected: "create command name primary secondary"')

        if command[1] in ['list', 'l']: #c l listType index functionIndex
            if command[2] in ['primary', 'p']:
                listlist = 'primarylisttbl'
            elif command[2] in ['secondary', 's']:
                listlist = 'secondarylisttbl'
            else:
                print(f'Received {command} expected: c l [p, s] i n')
                continue
            
            try:
                command[3] = int(command[3])
            except Exception as e:
                print(f'{command[3]} is not valid, expected integer')
            else:
                for index in range(4, len(command)):
                    db.execute('SELECT * FROM functiontbl f WHERE f.Id = ?', [command[index]])
                    if not db.fetchall():
                        print(f'Index {command[index]} not found in functiontbl, skipping.')
                        continue
                    db.execute(f'SELECT * FROM {listlist} l WHERE l.ListId = ? AND l.Function_Id = ?', (command[3], command[index]))
                    if not db.fetchall():
                        db.execute(f'INSERT INTO {listlist} (ListId, Function_Id) VALUES (?, ?)', (command[3], command[index]))
                        print(f'Successfully added {[command[3], command[index]]}.')

    if command[0] in ['delete', 'd']:
        db = conn.cursor() 
        if command[1] in ['function', 'func', 'f']: #delete functions and if allowed delete the individual commands
            strFunction = functionStandard(command[2])
            if len(command) == 3:
                try:
                    db.execute('DELETE FROM functiontbl f WHERE f.StrFunction = ?', [strFunction])
                except Exception as e:
                    print(f'{strFunction} could not be deleted, either it doesnt exist or an unexpected error happened!')
                else:
                    print(f'{strFunction} has been deleted!')
            else:
                for index in range(3, len(command)):
                    synCommand = str(command[index]).split(".")
                    synCommand[1] = synCommand[1].lower()
                    try:
                        commandSet = [synCommand[0], synCommand[1], synCommand[2], functionIndex]
                        db.execute('SELECT * FROM functiontbl f WHERE f.StrFunction = ?', [strFunction])
                        functionIndex = db.fetchone()[0]

                        
                        db.execute('DELETE FROM commandtbl c WHERE StrName = ? AND StrType = ? AND IntIndex = ? AND FunctionId = ?)', commandSet)

                        print(f'{command[index]} found in {strFunction} was deleted successfully.')
                    except Exception as e:
                        print(f'{command[index]} found in {strFunction} was not deleted successfully.')

        if command[1] in ['command', 'c']:
            strCommand = functionStandard(command[2])
            try:
                db.execute('DELETE FROM commandsetuptbl c WHERE c.StrName = ?', [strCommand])
            except Exception as e:
                print(f'{strCommand} could not be deleted, either it doesnt exist or an unexpected error happened!')
            else:
                print(f'{strCommand} has been deleted!')
                
        if command[1] in ['list', 'l']: 
            if command[2] in ['primary', 'p']:
                listlist = 'primarylisttbl'
            elif command[2] in ['secondary', 's']:
                listlist = 'secondarylisttbl'
            else:
                print(f'Received {command} expected: c l [p, s] i n')
                continue
            
            if len(command) == 4:
                try:
                    db.execute(f'DELETE FROM {listlist} l WHERE l.ListId = ?', (command[3]))
                except Exception as e:
                    print(f'Could not delete {command[2]} list {command[3]}')
                    print(e)
                else:
                    print(f'Deleted {command[2]} list {command[3]}')
            else:
                for index in range(4, len(command)):
                    try:
                        db.execute(f'DELETE FROM {listlist} l WHERE l.ListId = ? AND l.Function_Id = ?', (command[3], command[index]))
                    except Exception as e:
                        print(f'Could not delete {command[2]} list [{command[3]}, {command[index]}]')
                        print(e)
                    else:
                        print(f'Deleted {command[2]} list [{command[3]}, {command[index]}]')

    if command[0] == 'commit':
        try:
            conn.commit()
            print('Changes saved.')
        except Exception as e:
            print('An unexpected error was found, settings were not commited.')
            print(e)

    if command[0] in ['reset', 'r']:
        db.close()
        conn.close()
        conn = sqlite3.connect(dbPath)
        print('Program was reset!')

    if command[0] == 'quit':
        notExit = False