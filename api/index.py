from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # This allows your mod to talk to the site

# This is where the rankings stay while the server is awake
leaderboard = []

@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.json
    # data = {"username": "zion", "points": 500}
    
    # Update existing player or add new one
    for p in leaderboard:
        if p['username'] == data['username']:
            p['points'] = data['points']
            break
    else:
        leaderboard.append(data)
    
    # Sort: Highest points at Rank #1
    leaderboard.sort(key=lambda x: x['points'], reverse=True)
    
    return jsonify({"status": "success", "your_rank": leaderboard.index(data) + 1})

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(leaderboard)
