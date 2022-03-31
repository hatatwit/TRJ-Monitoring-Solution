from crypt import methods
from tabnanny import check
from flask import Flask, request, jsonify
import subprocess
import argparse

# Allows you to define a different port number using -p <port>
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port-number', default=5000)
args = parser.parse_args()

app = Flask(__name__)

@app.route('/uptime', methods=['POST', 'GET'])
def getUptime():
    uptimeRequest = request.args.get('uptime')
    if uptimeRequest == "secret":
        userHost = subprocess.check_output("whoami", shell=True)
        hostname = subprocess.check_output("hostname", shell=True)
        uptimeOut = subprocess.check_output("uptime -p", shell=True)
        #return "<h1>Host: " + str(userHost)[2:-3] + "@" + str(hostname)[2:-3] + "</h1> <h3>Has been up for: " + str(uptimeOut)[4:-3] + "</h3>"
        return "Host: " + str(userHost)[2:-3] + "@" + str(hostname)[2:-3] + "\nHas been up for:" + str(uptimeOut)[4:-3] + "\n"
    else:
        return "Permission denied.\n"


@app.route('/hostname', methods=['POST', 'GET'])
def getHostname():
    hostnameRequest = request.args.get('hostname')
    if hostnameRequest == "secret":
        userHost = subprocess.check_output("whoami", shell=True)
        hostname = subprocess.check_output("hostname", shell=True)
        return str(userHost)[2:-3] + "@" + str(hostname)[2:-3]
    else:
        return "Permission denied.\n"


@app.route('/df', methods=['POST', 'GET'])
def getDF():
    dfRequest = request.args.get('df')
    if dfRequest == 'secret':
        dfHost = subprocess.check_output("df -h", shell=True)
        return dfHost
    else:
        return "Permission denied.\n"


@app.route('/ping', methods=['POST', 'GET'])
def getPing():
    pingRequest = request.args.get('ping')
    remoteIP = request.remote_addr
    if pingRequest == "secret":
        pingHost = subprocess.check_output("ping -c 3 "+ remoteIP, shell=True)
        return pingHost
    else:
        return "Permission denied.\n"


@app.route('/dnsLookup', methods=['POST', 'GET'])
def getDNSLookup():
    dnsLookupRequest = request.args.get('dnsLookup')
    dnsLookupHost = subprocess.check_output("nslookup " + dnsLookupRequest, shell=True)
    return dnsLookupHost


@app.route('/usage', methods=['POST', 'GET'])
def getUsage():
    usageRequest = request.args.get('usage')
    if usageRequest == "secret":
        usageHost = subprocess.check_output("top -b -n 1 | head -n 20  | tail -n 19", shell=True)
        return usageHost
    else:
        return "Permission denied.\n"

if __name__ == '__main__':
    app.run(debug=True, port=args.port_number)

