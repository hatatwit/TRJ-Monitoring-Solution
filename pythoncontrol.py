import subprocess
from urllib import response
from cv2 import line
import requests
import os
from pathlib import Path
import sys

optionsList = ["Uptime", "Disk Space", "Ping", "Exit"]

def selectSystem(systemList):
    while True:
        iteration = 0
        for x in systemList:
            print("[" + str(iteration) + "] " + x)
            iteration += 1

        selection = input("\nSelect system you want to interact with: ")
        iteration = 0

        for x in systemList:
            if selection == str(iteration):
                #print("you selected: " + x)
                return x
            iteration += 1


def optionSelect(optionsList):
    iteration = 0
    for x in optionsList:
        print("[" + str(iteration) + "] " + x)
        iteration += 1

    selection = input("\nSelect an option: ")
    iteration = 0

    for x in optionsList:
        if selection == str(iteration):
            return x
        iteration += 1


if os.path.exists("systems.txt"):
    print('Server file found... continuing..')
    #system_list = open('systems.txt', 'a+')
else:
    createNew = input("No system list found. Add the file?: (y/n) ")
    if createNew.upper() == "Y" or createNew.upper() == "YES":
        tempFile = Path('systems.txt')
        tempFile.touch(exist_ok=True)
    else:
        print("Closing program...")
        sys.exit()

optionalAdd = input("Add a new system?: (y/n) ")
if optionalAdd.upper() == "Y" or optionalAdd.upper == "YES":
    newSystem = input("Enter ip:port of system: ")
    with open('systems.txt', 'a+') as systemFile:
        systemFile.seek(0)
        lines = systemFile.read().splitlines()
        if newSystem in lines:
            print("Duplicate found, not saving...")
        else:
            systemFile.write(newSystem+'\n')


with open("systems.txt") as file:
    systemList = file.read().splitlines()

#print(systemList[1])

selectedSystem = selectSystem(systemList)

getHostname = requests.get("http://"+selectedSystem+"/hostname?hostname=secret")

if str(getHostname.status_code) != "200" or getHostname.raise_for_status():
    print("Error: Couldn't establish hostname.")
    print("You selected: " + selectedSystem)
else:
    print(str(getHostname.text))
    print("You selected: " + str(getHostname.text) + "[" + selectedSystem + "]")



selectedOption = optionSelect(optionsList)

print("You selected: " + selectedOption)

if selectedOption == "Exit":
    selectedSystem = selectSystem(systemList)