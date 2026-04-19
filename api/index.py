from flask import Flask, request, jsonify
import os, redis, datetime

app = Flask(__name__)
kv = redis.from_url(os.environ.get("KV_URL"), decode_responses=True)

@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.json
    user = data.get('username')
    pts = data.get('points')
    date_key = datetime.datetime.now().strftime("%Y-%m-%d")

    # 1. Update Live Rankings
    kv.zadd("leaderboard:latest", {user: pts})
    
    # 2. Save Snapshot for Wayback (Snapshot of the day)
    kv.zadd(f"leaderboard:{date_key}", {user: pts})
    
    # Keep track of which dates we have data for
    kv.sadd("leaderboard_dates", date_key)
    
    return jsonify({"status": "success"})

@app.route('/api/data', methods=['GET'])
def get_data():
    date = request.args.get('date', 'latest')
    key = f"leaderboard:{date}"
    
    raw = kv.zrevrange(key, 0, 49, withscores=True)
    players = [{"username": p[0], "points": int(p[1])} for p in raw]
    
    # Also return all available dates for the dropdown
    dates = list(kv.smembers("leaderboard_dates"))
    
    return jsonify({"players": players, "available_dates": dates})
