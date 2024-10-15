import os
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"

BLOCKED_JSON_PATH = 'blocked.json'

def read_blocked_urls():
    if not os.path.exists(BLOCKED_JSON_PATH):
        with open(BLOCKED_JSON_PATH, 'w') as f:
            json.dump([], f)
    with open(BLOCKED_JSON_PATH, 'r') as f:
        return json.load(f)

def write_blocked_urls(urls):
    with open(BLOCKED_JSON_PATH, 'w') as f:
        json.dump(urls, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_blocked_urls', methods=['GET'])
def get_blocked_urls():
    return jsonify(read_blocked_urls())

@app.route('/add_url', methods=['POST'])
def add_url():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    blocked_urls = read_blocked_urls()
    if url not in blocked_urls:
        blocked_urls.append(url)
        write_blocked_urls(blocked_urls)
        return jsonify({'message': 'URL added successfully'}), 201
    else:
        return jsonify({'error': 'URL already exists'}), 409

@app.route('/remove_url', methods=['POST'])
def remove_url():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    blocked_urls = read_blocked_urls()
    if url in blocked_urls:
        blocked_urls.remove(url)
        write_blocked_urls(blocked_urls)
        return jsonify({'message': 'URL removed successfully'}), 200
    else:
        return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
