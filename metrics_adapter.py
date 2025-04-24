import os

from flask import Flask, Response
import requests

app = Flask(__name__)
METRICS_URL = os.getenv("METRICS_URL")

@app.route('/metrics')
def proxy_maas_metrics():
    resp = requests.get(METRICS_URL)
    return Response(resp.text, mimetype='text/plain')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)