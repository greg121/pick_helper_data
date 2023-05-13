from flask import Flask, render_template, request, g, jsonify
import json
import os
import git
import hmac
import hashlib
import configparser

app = Flask(__name__)

@app.route('/')
def index():
    file_path = os.path.join(os.path.dirname(os.getcwd()), 'data_collector', 'data', 'match_data.json')
    with open(file_path) as f:
        match_data = json.load(f)
    g.match_data = match_data
    return render_template('index.html', match_data=match_data)

def is_valid_signature(secret_key, signature, payload):
    secret_key = secret_key.encode() # Convert secret_key to bytes
    expected_signature = hmac.new(secret_key, payload, hashlib.sha1).hexdigest()
    return hmac.compare_digest(signature, 'sha1=' + expected_signature)

@app.route('/update', methods=['POST'])
def webhook():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(os.getcwd()), 'data_collector', 'config.ini'))
    w_secret = config.get('General', 'secret')
    if request.method == 'POST':
        x_hub_signature = request.headers.get('X-Hub-Signature')
        #TODO sicher machen
        if is_valid_signature(x_hub_signature, request.data, w_secret):
            repo = git.Repo('/home/greg121/lol_pick_helper')
            origin = repo.remotes.origin
            origin.pull()
            return 'Updated PythonAnywhere successfully', 200
        else:
            return 'Invalid signature', 420
    else:
        return 'Wrong event type', 400
    
def perform_analysis(match_id):    
    # Find the match with the specified ID
    match = next((m for m in g.match_data if m['match_id'] == match_id), None)
    if match is None:
        return {'error': 'Match not found'}

    # Extract the relevant data from the match object
    gold_lead_15 = match['gold_lead_15']
    build_order = match['build_order']

    # Perform analysis on the extracted data
    # ...

    # Return the analysis result
    return {'gold_lead_15': gold_lead_15, 'build_order': build_order}

@app.route('/analyze', methods=['POST'])
def analyze_match():
    match_id = request.form['match_id']
    # Use match_id to perform analysis
    analysis_result = perform_analysis(match_id)
    return jsonify(analysis_result)

if __name__ == '__main__':
    app.run(debug=True)