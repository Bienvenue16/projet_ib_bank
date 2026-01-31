from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# 1. CHARGER LE .ENV ICI EN PREMIER
load_dotenv()

# 2. ENSUITE IMPORTER LES ROUTES
from routes.chat import chat_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(chat_bp)

@app.route("/")
def health_check():
    return jsonify({"status": "IB Bank Backend is running"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)