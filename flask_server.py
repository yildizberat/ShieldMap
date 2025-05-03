from flask import Flask, jsonify, render_template
import json
from pathlib import Path

app = Flask(__name__, template_folder="templates", static_folder="static")
CSP_FILE = Path("shared/csp_suggestions.json")

@app.route("/")
def home():
    return render_template("map.html")

@app.route("/graph-data")
def graph_data():
    if not CSP_FILE.exists():
        return jsonify({"nodes": [], "links": []})
    
    raw = json.loads(CSP_FILE.read_text())
    origin = raw.get("origin", "example.com")
    categories = raw.get("categories", {})

    nodes = [{"id": origin, "group": "origin"}]
    links = []

    for directive, domains in categories.items():
        for domain in domains:
            nodes.append({"id": domain, "group": directive})
            links.append({"source": origin, "target": domain})

    return jsonify({"nodes": nodes, "links": links})

if __name__ == "__main__":
    app.run(port=5000, debug=True)