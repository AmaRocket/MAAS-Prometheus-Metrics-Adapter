# Flask Metrics Proxy

This Flask application serves as a proxy for standard Prometheus metrics from a MAAS server. It fetches the metrics from a specified URL and serves them via the /metrics endpoint.

# Features
	•	Metrics Proxy: The application proxies metrics from MAAS and serves them at the /metrics endpoint.
	•	Environment Variable: The target URL for fetching metrics is configurable via the METRICS_URL environment variable.

# Requirements
	•	Python 3.6 or higher
	•	Flask (pip install flask)
	•	Requests (pip install requests)

# Setup

1. Clone the Repository
```commandline
git clone <repository_url>
cd <repository_directory>
```

2. Install Dependencies

Ensure you have Python 3.x and install required libraries:
```commandline
pip install -r requirements.txt
```
3. Set Environment Variables

Set the METRICS_URL environment variable to the URL of the remote server from which you want to fetch the metrics.

On Linux/MacOS:
```commandline
export METRICS_URL="http://example.com/metrics"
```

# 4. Run the Application

You can start the Flask app by running the following command:
```commandline
python metrics_adapter.py
```

# 5. Access Metrics

After the app is running, you can access the proxied metrics by visiting:
```commandline
http://localhost:8001/metrics
```
