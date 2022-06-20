import os
import requests
import json

from flask import Flask, jsonify, request

# read environment variables
GITEA_SERVER_URL = os.environ.get("GITEA_SERVER_URL", None)
GITEA_USER = os.environ.get("GITEA_USER", None)
GITEA_PASSWORD = os.environ.get("GITEA_PASSWORD", None)


def delete_gitea_repo(repo_name):
    app.logger.info("Deleting repo " + repo_name)
    session = requests.Session()
    session.auth = (GITEA_USER, GITEA_PASSWORD)

    response = session.delete(GITEA_SERVER_URL + "/api/v1/repos/" + GITEA_USER + "/" + repo_name, headers={
        "accept": "application/json",
        "Content-Type": "application/json"
    })

    app.logger.info(response.status_code)
    app.logger.info(response.text)

    if response.status_code >= 400 and response.status_code <= 599:
        return False
    
    return True

def create_gitea_repo(repo_name):
    app.logger.info("Creating repo " + repo_name)
    session = requests.Session()
    session.auth = (GITEA_USER, GITEA_PASSWORD)

    data = {
        "auto_init": True,
        "default_branch": "master",
        "description": "Automatically provisioned repo for Keptn",
        "license": "ISC",
        "name": repo_name,
        "private": True,
        "template": False,
        "trust_model": "default"
    }

    app.logger.info(data)

    response = session.post(GITEA_SERVER_URL + "/api/v1/user/repos", json.dumps(data), headers={
        "accept": "application/json",
        "Content-Type": "application/json"
    })

    app.logger.info(response.status_code)
    app.logger.info(response.text)

    if response.status_code >= 400 and response.status_code <= 599:
        return None

    json_response = json.loads(response.text)
    
    return {
        "gitRemoteURL": GITEA_SERVER_URL + "/" + json_response['full_name'] + ".git",
        "gitUser": GITEA_USER,
        "gitToken": GITEA_PASSWORD
    }


if not GITEA_SERVER_URL:
    print("Please set GITEA_SERVER_URL as an environment variable")
    os.exit(1)
if not GITEA_USER:
    print("Please set GITEA_USER as an environment variable")
    os.exit(1)
if not GITEA_PASSWORD:
    print("Please set GITEA_PASSWORD as an environment variable")
    os.exit(1)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Docker!'

@app.route('/health')
def health():
    return 'OK'

@app.route('/ready')
def ready():
    return 'OK'

@app.route('/repository', methods=['POST'])
def create_repository():
    json_request_data = json.loads(request.data)

    app.logger.info(json_request_data)

    if not "project" in json_request_data:
        return (jsonify({"error": "Please provide project in payload"}), 400)

    project_name = json_request_data["project"]

    resp = create_gitea_repo(project_name)

    if not resp:
        return (jsonify({"error": "Could not create repo"}), 409)

    app.logger.info("----")
    app.logger.info(resp)
    
    return (jsonify(resp), 201)

@app.route('/repository', methods=['DELETE'])
def delete_repository():
    json_request_data = json.loads(request.data)

    app.logger.info(json_request_data)

    if not "project" in json_request_data:
        return (jsonify({"error": "Please provide project in payload"}), 400)

    project_name = json_request_data["project"]

    resp = delete_gitea_repo(project_name)

    if not resp:
        return (jsonify({"error": "Could not delete repo"}), 409)

    app.logger.info("----")
    app.logger.info(resp)
    
    return ("", 204)

app.run(host='0.0.0.0', port=8080)
