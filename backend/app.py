from flask import Flask, request, jsonify
from services.job_service import search_jobs  # adjust path as needed
import requests

app = Flask(__name__)

@app.route("/api/jobs", methods=["GET"])
def get_jobs():
    query = request.args.get("query", "")
    location = request.args.get("location", "")
    remote = request.args.get("remote", "false").lower() == "true"

    jobs = search_jobs(query, location, remote)
    return jsonify(jobs)

if __name__ == "__main__":
    app.run(debug=True, port=5050)

