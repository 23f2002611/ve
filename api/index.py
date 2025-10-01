from flask import Flask, request, jsonify
from flask_cors import CORS
import statistics

app = Flask(__name__)
CORS(app)

# Telemetry data
TELEMETRY_DATA = [
  {"region": "apac", "service": "analytics", "latency_ms": 210.89, "uptime_pct": 98.817, "timestamp": 20250301},
  {"region": "apac", "service": "support", "latency_ms": 226.4, "uptime_pct": 99.341, "timestamp": 20250302},
  {"region": "apac", "service": "checkout", "latency_ms": 190.78, "uptime_pct": 98.608, "timestamp": 20250303},
  {"region": "apac", "service": "checkout", "latency_ms": 104.83, "uptime_pct": 97.159, "timestamp": 20250304},
  {"region": "apac", "service": "recommendations", "latency_ms": 149.12, "uptime_pct": 97.73, "timestamp": 20250305},
  {"region": "apac", "service": "checkout", "latency_ms": 176.02, "uptime_pct": 99.497, "timestamp": 20250306},
  {"region": "apac", "service": "support", "latency_ms": 114.97, "uptime_pct": 97.425, "timestamp": 20250307},
  {"region": "apac", "service": "checkout", "latency_ms": 177.64, "uptime_pct": 97.606, "timestamp": 20250308},
  {"region": "apac", "service": "catalog", "latency_ms": 128.3, "uptime_pct": 98.358, "timestamp": 20250309},
  {"region": "apac", "service": "support", "latency_ms": 172.4, "uptime_pct": 97.374, "timestamp": 20250310},
  {"region": "apac", "service": "analytics", "latency_ms": 130.14, "uptime_pct": 97.131, "timestamp": 20250311},
  {"region": "apac", "service": "recommendations", "latency_ms": 173.18, "uptime_pct": 99.006, "timestamp": 20250312},
  {"region": "emea", "service": "analytics", "latency_ms": 139.75, "uptime_pct": 99.276, "timestamp": 20250301},
  {"region": "emea", "service": "recommendations", "latency_ms": 149.53, "uptime_pct": 97.511, "timestamp": 20250302},
  {"region": "emea", "service": "checkout", "latency_ms": 188.29, "uptime_pct": 98.71, "timestamp": 20250303},
  {"region": "emea", "service": "analytics", "latency_ms": 214.03, "uptime_pct": 97.735, "timestamp": 20250304},
  {"region": "emea", "service": "checkout", "latency_ms": 160.45, "uptime_pct": 99.455, "timestamp": 20250305},
  {"region": "emea", "service": "payments", "latency_ms": 168.15, "uptime_pct": 98.722, "timestamp": 20250306},
  {"region": "emea", "service": "analytics", "latency_ms": 191.22, "uptime_pct": 98.675, "timestamp": 20250307},
  {"region": "emea", "service": "support", "latency_ms": 186.33, "uptime_pct": 97.766, "timestamp": 20250308},
  {"region": "emea", "service": "recommendations", "latency_ms": 208.5, "uptime_pct": 97.142, "timestamp": 20250309},
  {"region": "emea", "service": "catalog", "latency_ms": 162.63, "uptime_pct": 97.494, "timestamp": 20250310},
  {"region": "emea", "service": "checkout", "latency_ms": 176.6, "uptime_pct": 99.451, "timestamp": 20250311},
  {"region": "emea", "service": "recommendations", "latency_ms": 156.26, "uptime_pct": 98.11, "timestamp": 20250312},
  {"region": "amer", "service": "catalog", "latency_ms": 159.54, "uptime_pct": 99.124, "timestamp": 20250301},
  {"region": "amer", "service": "catalog", "latency_ms": 112.89, "uptime_pct": 98.684, "timestamp": 20250302},
  {"region": "amer", "service": "catalog", "latency_ms": 197.13, "uptime_pct": 97.486, "timestamp": 20250303},
  {"region": "amer", "service": "payments", "latency_ms": 156.26, "uptime_pct": 98.946, "timestamp": 20250304},
  {"region": "amer", "service": "checkout", "latency_ms": 107.63, "uptime_pct": 98.99, "timestamp": 20250305},
  {"region": "amer", "service": "analytics", "latency_ms": 197.66, "uptime_pct": 97.498, "timestamp": 20250306},
  {"region": "amer", "service": "catalog", "latency_ms": 190.13, "uptime_pct": 99.284, "timestamp": 20250307},
  {"region": "amer", "service": "support", "latency_ms": 207.38, "uptime_pct": 98.294, "timestamp": 20250308},
  {"region": "amer", "service": "checkout", "latency_ms": 176.65, "uptime_pct": 99.458, "timestamp": 20250309},
  {"region": "amer", "service": "checkout", "latency_ms": 115.06, "uptime_pct": 98.076, "timestamp": 20250310},
  {"region": "amer", "service": "payments", "latency_ms": 122.07, "uptime_pct": 97.893, "timestamp": 20250311},
  {"region": "amer", "service": "checkout", "latency_ms": 141.32, "uptime_pct": 97.426, "timestamp": 20250312}
]

def calculate_percentile(values, percentile):
    """Calculate the percentile of a list of values."""
    if not values:
        return 0
    sorted_values = sorted(values)
    index = (percentile / 100) * (len(sorted_values) - 1)
    lower = int(index)
    upper = lower + 1
    weight = index - lower
    
    if upper >= len(sorted_values):
        return sorted_values[lower]
    
    return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight

def analyze_region(region_data, threshold_ms):
    """Analyze telemetry data for a specific region."""
    if not region_data:
        return {
            "avg_latency": 0,
            "p95_latency": 0,
            "avg_uptime": 0,
            "breaches": 0
        }
    
    latencies = [record["latency_ms"] for record in region_data]
    uptimes = [record["uptime_pct"] for record in region_data]
    
    return {
        "avg_latency": round(statistics.mean(latencies), 2),
        "p95_latency": round(calculate_percentile(latencies, 95), 2),
        "avg_uptime": round(statistics.mean(uptimes), 2),
        "breaches": sum(1 for lat in latencies if lat > threshold_ms)
    }

@app.route('/api', methods=['POST'])
@app.route('/api/', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        regions = data.get('regions', [])
        threshold_ms = data.get('threshold_ms', 180)
        
        response_data = {}
        for region in regions:
            region_records = [r for r in TELEMETRY_DATA if r['region'] == region]
            response_data[region] = analyze_region(region_records, threshold_ms)
        
        return jsonify(response_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
