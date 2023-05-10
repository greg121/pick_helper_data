from flask import Flask, render_template, request, g, jsonify
import json
import os
import git

app = Flask(__name__)

@app.route('/')
def index():
    file_path = os.path.join(os.path.dirname(os.getcwd()), 'data_collector', 'data', 'match_data.json')
    with open(file_path) as f:
        match_data = json.load(f)
    g.match_data = match_data
    return render_template('index.html', match_data=match_data)

@app.route('/update', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/greg121/lol_pick_helper')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
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