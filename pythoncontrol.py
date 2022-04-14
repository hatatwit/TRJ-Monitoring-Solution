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
from twilio.rest import Client
import re

# TWILIO CREDS
account_sid = 'AC7eb2c71840d90d1d2531a6d14dc5c61e'
auth_token = 'e6632c0b4940a9c99e31d144ba271c36'

sysadmins = ['+15089017299', '+19789609162']

client = Client(account_sid, auth_token)
#########################################

optionsList = ["Uptime", "Disk Space", "Ping", "DNS Lookup", "Current Usage", "Enable Logging", "Enable Passive Monitor", "Exit"]
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
        res = re.findall(r'\d\d%', getDF.text)
        print(res)
        res = [s.replace("%", "") for s in res]
        print(res)
        if any(int(x) > 75 for x in res):
            print("Disk space is above 75%")
            for x in sysadmins:
                message = client.messages.create(
                    from_='+19402837299',
                    body ='Host: ' + str(selectedSystem) + '\nHas reached disk space threshold of 75%',
                    to = x
                    )
            print(message.sid)
            sys.exit()

        writeLog(getDF.text, selectedOption.upper())
    if selectedOption == "Ping":
        getPing = requests.get("http://"+selectedSystem+"/ping?ping="+systemLockPass)
        print(getPing.text)
        if getPing.text.find("100% packet loss") != -1 or getPing.text.find("Internet ping (google.com) failed.") != -1:
            for x in sysadmins:
                message = client.messages.create(
                    from_='+19402837299',
                    body ='Host: ' + str(selectedSystem) + '\nUnable to ping google.com',
                    to = x
                    )
            print(message.sid)
            print("Ping FAILURE")
            sys.exit()
        else:
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
    if selectedOption == "Enable Passive Monitor":
        startPassive = requests.get("http://"+selectedSystem+"/passive?passive="+systemLockPass)
        print(startPassive.text)



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
    
    try:
        getHostname = requests.get("http://"+selectedSystem+"/hostname?hostname=" + systemLockPass)
    except requests.exceptions.ConnectionError:
        print("Connection error, please check your connection and try again.")

        for x in sysadmins:
            message = client.messages.create(
                from_='+19402837299',
                body ='Unable to resolve host on ' + str(selectedSystem),
                to = x
                )
        print(message.sid)
        sys.exit()
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


