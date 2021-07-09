import subprocess

import flask
from flask import request, jsonify

import requests

from commands import commands

app = flask.Flask(__name__)
app.config["DEBUG"] = True

import boto3
import os


client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
)


def download_dir(prefix, local, bucket, client):
    keys = []
    dirs = []
    next_token = ''
    base_kwargs = {
        'Bucket':bucket,
        'Prefix':prefix,
    }
    while next_token is not None:
        kwargs = base_kwargs.copy()
        if next_token != '':
            kwargs.update({'ContinuationToken': next_token})
        results = client.list_objects_v2(**kwargs)
        contents = results.get('Contents')
        for i in contents:
            k = i.get('Key')
            if k[-1] != '/':
                keys.append(k)
            else:
                dirs.append(k)
        next_token = results.get('NextContinuationToken')
    for d in dirs:
        dest_pathname = os.path.join(local, d)
        if not os.path.exists(os.path.dirname(dest_pathname)):
            os.makedirs(os.path.dirname(dest_pathname))
    for k in keys:
        dest_pathname = os.path.join(local, k)
        if not os.path.exists(os.path.dirname(dest_pathname)):
            os.makedirs(os.path.dirname(dest_pathname))
        client.download_file(bucket, k, dest_pathname)



@app.route('/', methods=["POST"])
def build():
    data = request.get_json()
    langage = data["langage"]
    version = data["version"]
    path = data["path"]
    name = data["name"]

    download_dir(name, path, "d-host", client)
    process = subprocess.Popen(commands[langage].format(version, path).split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return jsonify("{}:{}".format(output, version)), 200

app.run(host='0.0.0.0', port=80)
