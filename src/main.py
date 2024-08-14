import os
import json
import hmac
import hashlib
from flask import Flask, request, jsonify

def create_config_if_not_exist():
    file_path = 'deployments/config.json'

    if not os.path.exists(file_path):
        # If the file doesn't exist, create it and write {"projects":[]}
        data = {"projects": []}
        with open(file_path, 'w') as file:
            json.dump(data, file)
    else:
        # If the file exists, do nothing
        pass

app = Flask(__name__)

GITHUB_SECRET = 'your_github_webhook_secret'

def verify_signature(payload, signature):
    # Generate the HMAC SHA256 hash of the payload using the secret
    mac = hmac.new(GITHUB_SECRET.encode('utf-8'), msg=payload, digestmod=hashlib.sha256)
    return hmac.compare_digest('sha256=' + mac.hexdigest(), signature)

@app.route('/')
def index():
    return 'hypnos is server is active'


def push(app_name):

    f = open('deployments/config.json')
    data = json.load(f)
    f.close()
        
    def _match_project_name(project):
        return project['name'] == app_name
      
    projects = filter(_match_project_name, data['projects'])
    
    # TODO: is there a better way to get first item in an iterator?
    for p in projects:
        project = p
        break

    print(project)
    os.system(f'cd {project['directory']} && git pull')
    os.system(f'docker compose --file {project['compose']} up --build -d')

    return True


@app.route('/webhook', methods=['POST'])
def github_webhook():
    print('received request on webhook endpoints')
    # GitHub sends the request body as bytes, so we need to handle that
    payload = request.data
    signature = request.headers.get('X-Hub-Signature-256')

    # Verify the payload with the signature
    if signature is None or not verify_signature(payload, signature):
        return jsonify({'error': 'Invalid signature'}), 400

    # GitHub sends the event type in this header
    event = request.headers.get('X-GitHub-Event')

    print('came this far', flush=True)
    print(event)
    print(signature)

    if event == 'push':
        # Convert the payload to JSON
        data = request.json
        branch = data['ref'].split('/')[-1]

        print(data)

        # Handle the push event
        print(f"Received push event on branch: {branch}")

        # Only react to pushes on the main branch
        if branch == 'main':
            # Perform your actions here
            push(data['repository']['name'])
            print("This was a push to the main branch!")

    print('releasing all prints', flush=True)
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    create_config_if_not_exist()
    app.run(host='0.0.0.0', port=4545)
