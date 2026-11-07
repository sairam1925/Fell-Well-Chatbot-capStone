import sys

if hasattr(sys.stdout, "reconfigure") and sys.stdout and not sys.stdout.closed:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure") and sys.stderr and not sys.stderr.closed:
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from flask import Flask, render_template, request, jsonify
from chatbot import Chatbot

app = Flask(__name__)
bot = Chatbot()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"response": "Please enter a message!"}), 400

    reply = bot.respond(user_message)
    return jsonify({"response": reply})

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("LIVE CHATBOT SERVER RUNNING LOCALLY")
    print("Open your browser and navigate to: http://127.0.0.1:5000")
    print("=" * 60 + "\n")
    app.run(host="127.0.0.1", port=5000, debug=False)
