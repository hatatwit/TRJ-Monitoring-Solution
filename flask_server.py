from crypt import methods
from tabnanny import check
from flask import Flask, request, jsonify, render_template
import pyrebase
import subprocess
import argparse
from flask_cors import CORS

# Allows you to define a different port number using -p <port>
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port-number', default=5000)
parser.add_argument('-l', '--lock-pass', default="secret")
args = parser.parse_args()


app = Flask(__name__)
CORS(app)

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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/remote.js")
def remoteJS():
    return render_template("remote.js")

@app.route("/remote.css")
def remoteCSS():
    return render_template("remote.css")

@app.route("/features")
def features():
    return render_template("features.html")

@app.route("/logfile")
def logfile():
    logURL = storage.child("logfile.txt").get_url(None)
    return render_template("logfile.html", logURL=logURL)

@app.route('/uptime', methods=['POST', 'GET'])
def getUptime():
    uptimeRequest = request.args.get('uptime')
    if uptimeRequest == str(args.lock_pass):
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
    if hostnameRequest == str(args.lock_pass):
        userHost = subprocess.check_output("whoami", shell=True)
        hostname = subprocess.check_output("hostname", shell=True)
        return str(userHost)[2:-3] + "@" + str(hostname)[2:-3]
    else:
        return "Permission denied.\n"


@app.route('/df', methods=['POST', 'GET'])
def getDF():
    dfRequest = request.args.get('df')
    if dfRequest == str(args.lock_pass):
        dfHost = subprocess.check_output("df -h", shell=True)
        return dfHost
    else:
        return "Permission denied.\n"


@app.route('/ping', methods=['POST', 'GET'])
def getPing():
    pingRequest = request.args.get('ping')
    remoteIP = request.remote_addr
    if pingRequest == str(args.lock_pass):
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
    if usageRequest == str(args.lock_pass):
        usageHost = subprocess.check_output("top -b -n 1 | head -n 20  | tail -n 19", shell=True)
        return usageHost
    else:
        return "Permission denied.\n"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=args.port_number)

