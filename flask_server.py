from crypt import methods
from tabnanny import check
from flask import Flask, request
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

if __name__ == '__main__':
    app.run(debug=True, port=args.port_number)

