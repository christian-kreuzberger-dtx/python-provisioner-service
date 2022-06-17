
from flask import Flask, jsonify
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
    return (jsonify({
        "gitRemoteURL": "https://abc/keptn-sockshop.git",
        "gitToken": "xyz",
        "gitUser": "string"
    }), 201)

@app.route('/repository', methods=['DELETE'])
def delete_repository():
    return ("", 204)

app.run(host='0.0.0.0', port=8080)
