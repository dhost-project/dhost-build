import subprocess

import flask
from flask import request, jsonify

import requests

from commands import commands

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=["POST"])
def build():
    data = request.get_json()
    langage = data["langage"]
    version = data["version"]
    path = data["path"]

    process = subprocess.Popen(commands[langage].format(path).split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    return jsonify("{}:{}".format(output, version)), 200

app.run(host='0.0.0.0', port=80)
