from flask import Flask
from flask_apscheduler import APScheduler
import argparse
import subprocess
from twilio.rest import Client
import requests
import re
import socket

# TWILIO CREDS
account_sid = 'AC7eb2c71840d90d1d2531a6d14dc5c61e'
auth_token = 'e6632c0b4940a9c99e31d144ba271c36'

sysadmins = ['+15089017299', '+19789609162']

client = Client(account_sid, auth_token)
#########################################


parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port-number', default=4999, type=int, help='Port number to run the server on')
args = parser.parse_args()


app = Flask(__name__)
scheduler = APScheduler()

def pingTask():
    try:
        pingHost = subprocess.check_output("ping -c 3 google.com", shell=True)
        pingHost = pingHost.decode("utf-8")
        print(pingHost)
    except subprocess.CalledProcessError:
        print("Connection error, please check your connection and try again.")
        externalip = requests.get('https://checkip.amazonaws.com').text.strip()
        externalip = (externalip+":"+str(args.port_number))
        internalip = socket.gethostbyname(socket.gethostname())
        print('Host: (External IP) - ' + externalip + "\n(Internal IP) - " + internalip + " is down (ping to google.com)")
        #for x in sysadmins:
        #    message = client.messages.create(
         #       from_='+19402837299',
        # #       body ='Host: ' + ip + " is down (ping to google.com)",
         #       to = x
          #      )
            #print(message.sid)
            
    else:
        print("Connection successful.")


def dfTask():
    dfHost = subprocess.check_output("df -h", shell=True)
    dfHost = dfHost.decode("utf-8")
    res = re.findall(r'\d\d%', dfHost)
    print(res)
    res = [s.replace("%", "") for s in res]
    print(res)
    if any(int(x) > 75 for x in res):
        print("Disk space is above 75%")
        #for x in sysadmins:
         #   message = client.messages.create(
        #        from_='+19402837299',
       #         body ='Host: ' + str(selectedSystem) + '\nHas reached disk space threshold of 75%',
      #          to = x
     #           )
    #print(message.sid)

if __name__ == '__main__':
    scheduler.add_job(id = 'Regular Ping Check', func=pingTask, trigger="interval", seconds=10)
    scheduler.add_job(id = 'Regular Disk Space Check', func=dfTask, trigger="interval", seconds=15)
    scheduler.start()
    app.run(host="0.0.0.0", port=args.port_number)