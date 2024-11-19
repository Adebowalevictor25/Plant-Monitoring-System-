# web_interface.py
# Web interface for the Plant Monitoring System.

from flask import Flask, render_template, request, jsonify
import threading
import time
from sensors import get_sensor_data
from ai_model import analyze_plant_image
import os
import matplotlib.pyplot as plt
from datetime import datetime

# Flask app initialization
app = Flask(__name__)

# Global variables for system status
system_status = {
    "light": "off",
    "watering": "off",
    "sensor_data": {},
    "last_analysis": {},
    "logs": [],
}

LOG_FILE = "web_logs.txt"

# Helper functions
def log_action(action):
    """
    Logs actions performed through the web interface.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {action}"
    system_status["logs"].append(log_entry)
    with open(LOG_FILE, "a") as f:
        f.write(log_entry + "\n")


@app.route("/")
def home():
    """
    Displays the main dashboard with current sensor data.
    """
    return render_template("dashboard.html", status=system_status)


@app.route("/status")
def get_status():
    """
    Returns the current system status as JSON.
    """
    try:
        sensor_data = get_sensor_data()
        system_status["sensor_data"] = sensor_data
        log_action("Fetched sensor data.")
        return jsonify({"status": "success", "data": sensor_data})
    except Exception as e:
        log_action(f"Error fetching sensor data: {e}")
        return jsonify({"status": "error", "message": str(e)})


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Performs plant health analysis and returns the result.
    """
    try:
        plant_name = request.json.get("plant", "Plant1")
        image_path = f"{plant_name}_image.jpg"
        analysis = analyze_plant_image(image_path)
        system_status["last_analysis"] = analysis
        log_action(f"Performed analysis on {plant_name}.")
        return jsonify({"status": "success", "data": analysis})
    except Exception as e:
        log_action(f"Error during analysis: {e}")
        return jsonify({"status": "error", "message": str(e)})


@app.route("/control", methods=["POST"])
def control():
    """
    Controls the system's devices (light or watering).
    """
    try:
        device = request.json.get("device")
        action = request.json.get("action")
        if device not in ["light", "watering"]:
            raise ValueError("Invalid device specified.")
        if action not in ["on", "off"]:
            raise ValueError("Invalid action specified.")
        
        system_status[device] = action
        log_action(f"Set {device} to {action}.")
        return jsonify({"status": "success", "message": f"{device} turned {action}."})
    except Exception as e:
        log_action(f"Error controlling device: {e}")
        return jsonify({"status": "error", "message": str(e)})


@app.route("/logs")
def view_logs():
    """
    Displays the system logs.
    """
    try:
        with open(LOG_FILE, "r") as f:
            logs = f.readlines()
        return jsonify({"status": "success", "logs": logs})
    except FileNotFoundError:
        return jsonify({"status": "error", "message": "No logs available."})


@app.route("/visualize")
def visualize():
    """
    Generates and displays a graph of sensor data.
    """
    try:
        data = system_status["sensor_data"]
        if not data:
            raise ValueError("No sensor data available.")

        timestamps = list(range(len(data.keys())))
        values = list(data.values())

        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, values, marker="o")
        plt.title("Sensor Data Visualization")
        plt.xlabel("Timestamp")
        plt.ylabel("Sensor Value")
        plt.grid(True)
        image_path = "static/sensor_graph.png"
        plt.savefig(image_path)
        log_action("Generated sensor data visualization.")
        return jsonify({"status": "success", "image_path": image_path})
    except Exception as e:
        log_action(f"Error generating visualization: {e}")
        return jsonify({"status": "error", "message": str(e)})


@app.route("/reset", methods=["POST"])
def reset():
    """
    Resets the system's status and logs.
    """
    try:
        system_status.update({
            "light": "off",
            "watering": "off",
            "sensor_data": {},
            "last_analysis": {},
            "logs": [],
        })
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
        log_action("System reset.")
        return jsonify({"status": "success", "message": "System reset successfully."})
    except Exception as e:
        log_action(f"Error during system reset: {e}")
        return jsonify({"status": "error", "message": str(e)})


# Background thread for periodic updates
def update_sensor_data():
    """
    Periodically updates sensor data in the background.
    """
    while True:
        try:
            sensor_data = get_sensor_data()
            system_status["sensor_data"] = sensor_data
            log_action("Updated sensor data.")
            time.sleep(60)
        except Exception as e:
            log_action(f"Error updating sensor data: {e}")


if __name__ == "__main__":
    # Start background thread
    threading.Thread(target=update_sensor_data, daemon=True).start()
    
    # Run the Flask app
    log_action("Starting web server.")
    app.run(host="0.0.0.0", port=5000)