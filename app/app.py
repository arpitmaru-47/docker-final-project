from flask import Flask, jsonify, request
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os

app = Flask(__name__)

mongo_uri = os.environ["MONGO_URI"]

client = MongoClient(
    mongo_uri,
    serverSelectionTimeoutMS=5000
)

db = client["dev_db"]
users = db["users"]

@app.route("/")
def home():
    return jsonify({
        "message": "Docker Final Project Running"
    })

@app.route("/health")
def health():
    try:
        client.admin.command("ping")
        return jsonify({"status": "healthy"}), 200
    except PyMongoError:
        return jsonify({"status": "unhealthy"}), 503
                
@app.route("/users", methods=["GET"])
def get_users():
    result = list(users.find({}, {"_id": 0}))
    return jsonify(result)

@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json(silent=True) or {}

    if not data.get("name") or not data.get("email"):
        return jsonify({
            "error": "Name and email are required"
        }), 400

    users.insert_one({
        "name": data["name"],
        "email": data["email"]
    })

    return jsonify({
        "message": "User added successfully"
    }), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
