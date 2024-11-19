# utilities.py
# Utility functions for the Plant Monitoring System.

import os
import json
import uuid
from datetime import datetime


# Time-related utilities
def format_timestamp(timestamp=None):
    """
    Formats a timestamp into a human-readable string.
    """
    if not timestamp:
        timestamp = datetime.now()
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def parse_datetime(date_string):
    """
    Parses a datetime string into a datetime object.
    """
    try:
        return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError("Invalid date format. Expected: YYYY-MM-DD HH:MM:SS")


# Data validation utilities
def validate_schedule_time(schedule_time):
    """
    Validates a schedule time string.
    """
    try:
        parsed_time = parse_datetime(schedule_time)
        if parsed_time < datetime.now():
            raise ValueError("Schedule time cannot be in the past.")
        return True
    except ValueError as e:
        raise ValueError(f"Invalid schedule time: {e}")


def validate_sensor_data(data):
    """
    Validates sensor data format.
    """
    required_keys = ["soil_moisture", "light_level", "temperature", "humidity"]
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing sensor data field: {key}")
    return True


# File operations
def save_to_file(data, file_path):
    """
    Saves data to a JSON file.
    """
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {file_path}.")
    except Exception as e:
        print(f"Error saving data to file: {e}")


def load_from_file(file_path):
    """
    Loads data from a JSON file.
    """
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error loading data from file: {e}")
        return {}


# Logging utilities
def log_action(log_file, action):
    """
    Logs an action to a log file with a timestamp.
    """
    timestamp = format_timestamp()
    log_entry = f"{timestamp} - {action}"
    try:
        with open(log_file, "a") as file:
            file.write(log_entry + "\n")
        print(f"Logged action: {action}")
    except Exception as e:
        print(f"Error logging action: {e}")


def read_logs(log_file, limit=10):
    """
    Reads the most recent log entries from a log file.
    """
    if not os.path.exists(log_file):
        return []
    try:
        with open(log_file, "r") as file:
            lines = file.readlines()
        return lines[-limit:]
    except Exception as e:
        print(f"Error reading logs: {e}")
        return []


# ID generation utilities
def generate_unique_id():
    """
    Generates a unique identifier.
    """
    return str(uuid.uuid4())


# Formatting utilities
def format_sensor_data(sensor_data):
    """
    Formats sensor data into a readable string.
    """
    return (
        f"Soil Moisture: {sensor_data['soil_moisture']}%\n"
        f"Light Level: {sensor_data['light_level']} lumens\n"
        f"Temperature: {sensor_data['temperature']}°C\n"
        f"Humidity: {sensor_data['humidity']}%"
    )


# Example usage
if __name__ == "__main__":
    # Example: Validating schedule time
    try:
        validate_schedule_time("2024-11-20 14:00:00")
        print("Schedule time is valid.")
    except ValueError as e:
        print(e)

    # Example: Saving and loading data
    data = {"key": "value"}
    save_to_file(data, "example.json")
    loaded_data = load_from_file("example.json")
    print("Loaded Data:", loaded_data)

    # Example: Logging actions
    log_action("system.log", "Started the system")
    print("Recent Logs:")
    for log in read_logs("system.log"):
        print(log.strip())

    # Example: Formatting sensor data
    sensor_data = {
        "soil_moisture": 50,
        "light_level": 300,
        "temperature": 22.5,
        "humidity": 45,
    }
    print(format_sensor_data(sensor_data))