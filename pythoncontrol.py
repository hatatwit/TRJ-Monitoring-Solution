import subprocess
from urllib import response
# from cv2 import line
import datetime
import requests
import pyrebase
import logging
import os
from pathlib import Path
import sys

optionsList = ["Uptime", "Disk Space", "Ping", "DNS Lookup", "Current Usage", "Enable Logging", "Enable Twilio Logging (to do)", "Exit"]
logFile = os.path.join(os.getcwd(), "networkInfo.log")

# Configure Firebase
config = {
    "apiKey": "AIzaSyDGMDGyOroE6UlVz33VbXRXc2A1VuRWWfA",
    "authDomain": "trj-monitoring-solution.firebaseapp.com",
    "databaseURL": "https://trj-monitoring-solution-default-rtdb.firebaseio.com",
    "projectId": "trj-monitoring-solution",
    "storageBucket": "trj-monitoring-solution.appspot.com",
    "messagingSenderId": "1082345966429",
    "appId": "1:1082345966429:web:b21c8bb1c5e122181676b4",
    "measurementId": "G-8W1JG3PFXY"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()
storage = firebase.storage()

def writeLog(content, command):
    with open(logFile, "a") as file:
        file.write(str(datetime.datetime.now()).split(".")[0] + "\n")
        file.write("----------\n" + command + "\n ----------" + "\n")
        file.write(content + "\n")


def monitorOptions(selectedOption, systemLockPass):
    if selectedOption == "Uptime":
        getUptime = requests.get("http://"+selectedSystem+"/uptime?uptime="+systemLockPass)
        print(str(getUptime.text))
        writeLog(str(getUptime.text), selectedOption.upper())
    if selectedOption == "Disk Space":
        getDF = requests.get("http://"+selectedSystem+"/df?df="+systemLockPass)
        print(getDF.text)
        writeLog(getDF.text, selectedOption.upper())
    if selectedOption == "Ping":
        getPing = requests.get("http://"+selectedSystem+"/ping?ping="+systemLockPass)
        print(getPing.text)
        writeLog(getPing.text, selectedOption.upper())
    if selectedOption == "DNS Lookup":
        dnsSite = input("Enter domain you want to test against (ex: google.com): ")
        getDNSLookup = requests.get("http://"+selectedSystem+"/dnsLookup?dnsLookup=" + dnsSite)
        print(getDNSLookup.text)
        writeLog(getDNSLookup.text, selectedOption.upper())
    if selectedOption == "Current Usage":
        getUsage = requests.get("http://"+selectedSystem+"/usage?usage="+systemLockPass)
        print(getUsage.text)
        writeLog(getUsage.text, selectedOption.upper())
    if selectedOption == "Enable Logging":
        # log file isn't existed -> create new one and upload on Firebase
        if os.path.isfile("networkInfo.log") != True:
            logging.FileHandler("networkInfo.log")
            storage.child("logfile.txt").put("networkInfo.log")
        # log file is existed -> upload/rewrite on Firebase
        else:
            storage.child("logfile.txt").put("networkInfo.log")


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
    isSystemSecure = input("Does this system have a lockpass? (y/n): ")
    if isSystemSecure.upper() == "Y":
        systemLockPass = input("Enter System lockpass (Leave blank for default): ")
        if systemLockPass == "":
            systemLockPass = "secret"
    else:
        systemLockPass = "secret"
    getHostname = requests.get("http://"+selectedSystem+"/hostname?hostname=" + systemLockPass)
    if str(getHostname.status_code) != "200" or getHostname.raise_for_status():
        print("Error: Couldn't establish hostname.")
        print("You selected: " + selectedSystem)
    else:
        print("You selected: " + str(getHostname.text) + "[" + selectedSystem + "]")
    while True:
        selectedOption = optionSelect(optionsList)
        print("You selected: " + selectedOption)
        outOption = monitorOptions(selectedOption, systemLockPass)
        if outOption == "Exit":
            break


