from flask import Flask, request, jsonify
from flask_cors import CORS
import os, redis, datetime

app = Flask(__name__)
CORS(app)

kv = redis.from_url(os.environ.get("KV_URL"), decode_responses=True)

@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.json
    user = data.get('username')
    pts = data.get('points')
    date_key = datetime.datetime.now().strftime("%Y-%m-%d")

 
    kv.zadd("leaderboard:latest", {user: pts})
    

    kv.zadd(f"leaderboard:{date_key}", {user: pts})
    kv.sadd("leaderboard_dates", date_key)
    
    return jsonify({"status": "success"})

@app.route('/api/data', methods=['GET'])
def get_data():
    date = request.args.get('date', 'latest')
    raw = kv.zrevrange(f"leaderboard:{date}", 0, 49, withscores=True)
    players = [{"username": p, "points": int(s)} for p, s in raw]
    dates = sorted(list(kv.smembers("leaderboard_dates")), reverse=True)
    
    return jsonify({"players": players, "dates": dates})
