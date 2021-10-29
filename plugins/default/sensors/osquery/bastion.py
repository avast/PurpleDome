#!/usr/bin/env python3

""" The remote bastion for the sensor. Used to control the osquery on the target. Opens a web command shell.
This is not meant to be secure and MUST NOT be used in a productive environment. As we use this in a hacking lab this
is reasonable.

Test with curl:

curl -X POST -F 'command=test' localhost:6666/osquery

(select timestamp from time)
"""

from flask import Flask, jsonify, request
import osquery


# TODO: Create a proper tool out of it
# TODO: Start osqueryi with proper parameters
# TODO: On the controller side: Find a collection of queries to get the system state

# TODO: Interesting tables: appcompat_shims, authenticode, autoexec, certificates, etc_hosts, logged_in_users

app = Flask(__name__)
osquery_instance = osquery.ExtensionClient('/home/vagrant/test.sock')
osquery_instance.open()


@app.route("/osquery", methods=['POST'])
def api():
    data = {}
    if request.method == 'POST':
        command = request.form["command"]
        data = {"command": command}
        client = osquery_instance.extension_client()
        data["result"] = client.query(command).response
    return jsonify(data)


if __name__ == "__main__":
    # Important: This is to be run on target hosts only. Those are hacked anyway.
    # Very bad security practice to use it in real world.
    app.run(host='0.0.0.0', port=6666)  # nosec
