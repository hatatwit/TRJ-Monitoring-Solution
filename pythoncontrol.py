import subprocess
from urllib import response
from cv2 import line
import requests
import os
from pathlib import Path
import sys

optionsList = ["Uptime", "Disk Space", "Ping", "DNS Lookup", "Current Usage", "Exit"]

def monitorOptions(selectedOption):
    if selectedOption == "Uptime":
        getUptime = requests.get("http://"+selectedSystem+"/uptime?uptime=secret")
        print(str(getUptime.text))
    if selectedOption == "Disk Space":
        getDF = requests.get("http://"+selectedSystem+"/df?df=secret")
        print(getDF.text)
    if selectedOption == "Ping":
        getPing = requests.get("http://"+selectedSystem+"/ping?ping=secret")
        print(getPing.text)
    if selectedOption == "DNS Lookup":
        dnsSite = input("Enter domain you want to test against (ex: google.com): ")
        getDNSLookup = requests.get("http://"+selectedSystem+"/dnsLookup?dnsLookup=" + dnsSite)
        print(getDNSLookup.text)
    if selectedOption == "Current Usage":
        getUsage = requests.get("http://"+selectedSystem+"/usage?usage=secret")
        print(getUsage.text)
    if selectedOption == "Exit":
        return "Exit"


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

while True:
    with open("systems.txt") as file:
        systemList = file.read().splitlines()
    selectedSystem = selectSystem(systemList)
    getHostname = requests.get("http://"+selectedSystem+"/hostname?hostname=secret")
    if str(getHostname.status_code) != "200" or getHostname.raise_for_status():
        print("Error: Couldn't establish hostname.")
        print("You selected: " + selectedSystem)
    else:
        print("You selected: " + str(getHostname.text) + "[" + selectedSystem + "]")
    while True:
        selectedOption = optionSelect(optionsList)
        print("You selected: " + selectedOption)
        outOption = monitorOptions(selectedOption)
        if outOption == "Exit":
            break


