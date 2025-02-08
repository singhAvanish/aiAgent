from flask import Flask, request, jsonify
import os
import time
import re
from flask_cors import CORS
import groclake
from groclake.modellake import ModelLake
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()
# Initialize Flask app
app = Flask(__name__)


CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

# Environment variable setup
GROCLAKE_API_KEY = os.getenv("GROCLAKE_API_KEY")
GROCLAKE_ACCOUNT_ID = os.getenv("GROCLAKE_ACCOUNT_ID")

os.environ['GROCLAKE_API_KEY'] = GROCLAKE_API_KEY
os.environ['GROCLAKE_ACCOUNT_ID'] = GROCLAKE_ACCOUNT_ID

# Initialize ModelLake
model_lake = ModelLake()
print(f"API Key: {GROCLAKE_API_KEY}")  # Test if it's loading correctly

class CyberSecurityAgent:
    def __init__(self):
        self.name = "CyberSecurityAI"
        self.role = "Monitor system logs and detect security threats."
        self.log_file = "/var/log/auth.log"  # Change based on OS
        self.agent = model_lake

    def detect_suspicious_activity(self, log_line):
        if "Failed password" in log_line:
            return "⚠️ Multiple failed login attempts detected! Possible brute-force attack."
        if "sudo:" in log_line and "incorrect password" in log_line:
            return "⚠️ Unauthorized sudo access attempt detected!"
        return None
    
    def monitor_logs(self):
        print("Starting system log monitoring...")
        if not os.path.exists(self.log_file):
            print("Log file not found! Check the path.")
            return
        
        try:
            with open(self.log_file, "r") as file:
                file.seek(0, 2)  # Move to end of file for real-time monitoring
                while True:
                    line = file.readline()
                    if not line:
                        time.sleep(1)
                        continue
                    alert = self.detect_suspicious_activity(line)
                    if alert:
                        self.agent.send_message(alert)
                        print(alert)
        except PermissionError:
            print("Permission denied: Unable to read log file. Try running with elevated privileges.")
    
    def run(self):
        self.agent.run(self.monitor_logs)

cyber_agent = CyberSecurityAgent()

@app.route('/scan_logs', methods=['POST'])
def scan_logs():
    try:
        data = request.get_json()
        if not data or "log_data" not in data:
            return jsonify({"error": "Missing 'log_data' in request body"}), 400
        
        log_entry = data["log_data"]
        alert = cyber_agent.detect_suspicious_activity(log_entry)
        
        if alert:
            return jsonify({"alert": alert})
        else:
            return jsonify({"message": "No threats detected."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
