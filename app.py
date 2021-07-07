import subprocess

import flask
from flask import request, jsonify

import requests

from commands import commands

app = flask.Flask(__name__)
app.config["DEBUG"] = True

import boto3
import os


client = boto3.client('s3')
resource = boto3.resource('s3')

def download_dir(bucket_name, dir_name):
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix = dir_name):
        if not os.path.exists(os.path.dirname(obj.key)):
            os.makedirs(os.path.dirname(obj.key))
        bucket.download_file(obj.key, obj.key) # save to same path



@app.route('/', methods=["POST"])
def build():
    data = request.get_json()
    langage = data["langage"]
    version = data["version"]
    path = data["path"]

    download_dir("d-host", path)
    process = subprocess.Popen(commands[langage].format(path).split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    return jsonify("{}:{}".format(output, version)), 200

app.run(host='0.0.0.0', port=80)
