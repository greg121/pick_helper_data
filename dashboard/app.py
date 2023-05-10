from flask import Flask, render_template, request
import json
import os
import git

app = Flask(__name__)

@app.route('/')
def index():
    file_path = os.path.join(os.path.dirname(os.getcwd()), 'data_collector', 'data', 'match_data.json')
    with open(file_path) as f:
        match_data = json.load(f)
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
    

#TEST
        
if __name__ == '__main__':
    app.run(debug=True)