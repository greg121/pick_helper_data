from flask import Flask, render_template
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    file_path = os.path.join(os.path.dirname(os.getcwd()), 'data_collector', 'data', 'match_data.json')
    with open(file_path) as f:
        match_data = json.load(f)
    return render_template('index.html', match_data=match_data)

if __name__ == '__main__':
    app.run(debug=True)