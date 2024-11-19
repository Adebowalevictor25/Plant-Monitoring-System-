# config.py
# Configuration settings for the Plant Monitoring System.

import os

# General settings
DEBUG = True
LOG_FILE = "system.log"
DATABASE_FILE = "plant_monitoring.db"
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000

# Sensor thresholds
SENSOR_THRESHOLDS = {
    "soil_moisture": {"min": 30, "max": 70},  # Percent
    "light_level": {"min": 200, "max": 800},  # Lumens
    "temperature": {"min": 15, "max": 35},    # Celsius
    "humidity": {"min": 40, "max": 70},       # Percent
}

# Telegram bot settings
TELEGRAM_BOT_TOKEN = "your-telegram-bot-token"
TELEGRAM_LOG_FILE = "telegram_bot.log"

# Scheduling
DEFAULT_SCHEDULE_INTERVAL = {
    "watering": 60,  # Minutes
    "light": 30,     # Minutes
}

# API endpoints (if external integrations are needed)
API_SETTINGS = {
    "open_weather": {
        "base_url": "https://api.openweathermap.org/data/2.5/weather",
        "api_key": "your-openweather-api-key",
    }
}

# Logging configuration
LOGGING = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S",
}

# Flask templates and static file paths
TEMPLATE_FOLDER = os.path.join(os.getcwd(), "templates")
STATIC_FOLDER = os.path.join(os.getcwd(), "static")

# File paths
SENSOR_DATA_FILE = "sensor_data.json"
ANALYSIS_RESULTS_FILE = "analysis_results.json"

# Retry settings for APIs or devices
RETRY_SETTINGS = {
    "max_retries": 3,
    "retry_interval": 5,  # Seconds
}

# Security
SECRET_KEY = "your-secret-key"

# Example helper function to check thresholds
def is_within_threshold(sensor, value):
    """
    Checks if a sensor value is within the defined threshold.
    """
    thresholds = SENSOR_THRESHOLDS.get(sensor)
    if not thresholds:
        raise ValueError(f"No thresholds defined for sensor: {sensor}")
    return thresholds["min"] <= value <= thresholds["max"]

# Example usage of configuration values
if __name__ == "__main__":
    # Check if a value is within the soil moisture threshold
    example_value = 50
    if is_within_threshold("soil_moisture", example_value):
        print(f"Value {example_value} is within the soil moisture threshold.")
    else:
        print(f"Value {example_value} is outside the soil moisture threshold.")

    # Print Flask server settings
    print(f"Flask will run on {FLASK_HOST}:{FLASK_PORT}")