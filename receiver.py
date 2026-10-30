"""Local receiver: accepts CI test-report JSON and saves test-report.json."""
import hmac
import os
from flask import Flask, request, jsonify

app = Flask(__name__)
TOKEN = os.environ.get("REPORT_TOKEN", "")

@app.post("/report")
def receive_report():
    if TOKEN:
        supplied = request.headers.get("X-Report-Token", "")
        if not hmac.compare_digest(supplied, TOKEN):
            return jsonify({"error": "unauthorized"}), 401
    report = request.get_json(silent=True)
    if not isinstance(report, dict) or "tests" not in report or "summary" not in report:
        return jsonify({"error": "invalid report format"}), 400
    with open("test-report.json", "w", encoding="utf-8") as f:
        import json
        json.dump(report, f, indent=2)
        f.write("\n")
    return jsonify({"message": "report saved", "status": report.get("summary", {}).get("status")}), 200

@app.get("/health")
def health():
    return jsonify({"status": "running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
