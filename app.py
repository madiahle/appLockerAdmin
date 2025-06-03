from flask import Flask, jsonify, request, render_template, redirect
import json
import os

app = Flask(__name__)
CONFIG_FILE = "config.json"
API_KEY = "my_secure_key_123"  # à changer

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"allowed_apps": [], "password": ""}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/config", methods=["GET"])
def get_config():
    key = request.args.get("api_key")
    if key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(load_config())

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        apps = request.form.get("allowed_apps").splitlines()
        password = request.form.get("password")
        config = {
            "allowed_apps": [a.strip() for a in apps if a.strip()],
            "password": password
        }
        save_config(config)
        return redirect("/admin")
    return render_template("admin.html", config=load_config())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
