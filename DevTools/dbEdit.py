import os
import sqlite3

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

dbName = 'commandDB'
dbPath = os.getcwd() + '/' + dbName

conn = sqlite3.connect(dbPath)

display_title_bar()

while True:
    command = str(input()).split(" ")

    if command[0] == 'show':
        if command[1] == 'data':
            print('\nShowing all data in tables of {}'.format(dbName))
            db = conn.cursor() 
            db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
            
            for row in db.fetchall():
                print('\t{}'.format(row))
                queryData = db.execute("SELECT * FROM {}".format(row[0]))
                for row in queryData:
                    print('\t\t{}'.format(row))
        if command[1] == 'functions':
            print('\nShowing all functions in {}'.format(dbName))
            db = conn.cursor() 
            db.execute('SELECT * FROM functiontbl')
            functiontbl = []
            for row in db.fetchall():
                functiontbl.append(row)

            db.execute('SELECT * FROM commandtbl')
            commandtbl = []
            for row in db.fetchall():
                commandtbl.append(row)

            for functionValue in functiontbl:
                print("\t{}:".format(functionValue[1]))
                for commandValue in commandtbl:
                    if functionValue[0] == int(commandValue[4]):
                        print("\t|-> {}.{}.{}".format(commandValue[1], commandValue[2], commandValue[3]))
                print("")

        if command[1] == 'commands':
            print('\nShowing all commands in {}'.format(dbName))
            db = conn.cursor() 
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
                print('\t{}:\n\t|-> Primary List:'.format(commandsetupVal[1]))
                for primarylistVal in primarylisttbl:
                    if primarylistVal[0] == commandsetupVal[2]:
                        for functionVal in functiontbl:
                            if functionVal[0] == primarylistVal[1]:
                                print('\t|   |-> {}:'.format(functionVal[1]))
                                for commandValue in commandtbl:
                                    if functionVal[0] == int(commandValue[4]):
                                        print("\t|   |   |-> {}.{}.{}".format(commandValue[1], commandValue[2], commandValue[3]))
                print('\t|-> Secondary List:')
                for secondarylistVal in secondarylisttbl:
                    if secondarylistVal[0] == commandsetupVal[3]:
                        for functionVal in functiontbl:
                            if functionVal[0] == secondarylistVal[1]:
                                print('\t|   |-> {}:'.format(functionVal[1]))
                                for commandValue in commandtbl:
                                    if functionVal[0] == int(commandValue[4]):
                                        print("\t|   |   |-> {}.{}.{}".format(commandValue[1], commandValue[2], commandValue[3]))

    if command[0] == 'create':
        newString = command[2].lower()
        newString = newString.replace(newString[0], newString[0].upper(), 1)
        if command[1] == 'function':
            pass