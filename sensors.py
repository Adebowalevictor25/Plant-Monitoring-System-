# sensors.py
# Functions for interacting with sensors in the plant monitoring system.

import random
import time

# Constants for sensor thresholds
SOIL_MOISTURE_THRESHOLD = 30  # Minimum soil moisture level for healthy plants
LIGHT_LEVEL_THRESHOLD = 200  # Minimum light level in lumens
TEMPERATURE_RANGE = (15, 35)  # Optimal temperature range in Celsius
HUMIDITY_RANGE = (40, 70)  # Optimal humidity range in percentage

def initialize_sensors():
    """
    Simulates the initialization of sensors.
    """
    print("Initializing sensors...")
    time.sleep(1)  # Simulate delay
    print("Sensors initialized successfully!")

def read_soil_moisture():
    """
    Simulates reading soil moisture from a sensor.
    """
    moisture = random.randint(10, 90)  # Simulate random moisture level
    print(f"Soil moisture level: {moisture}%")
    return moisture

def read_light_level():
    """
    Simulates reading light level from a sensor.
    """
    light_level = random.randint(50, 500)  # Simulate random light level
    print(f"Light level: {light_level} lumens")
    return light_level

def read_temperature():
    """
    Simulates reading temperature from a sensor.
    """
    temperature = random.uniform(10.0, 40.0)  # Simulate random temperature
    print(f"Temperature: {temperature:.2f}°C")
    return temperature

def read_humidity():
    """
    Simulates reading humidity from a sensor.
    """
    humidity = random.uniform(20.0, 90.0)  # Simulate random humidity level
    print(f"Humidity: {humidity:.2f}%")
    return humidity

def get_sensor_data():
    """
    Collects data from all sensors and returns it as a dictionary.
    """
    print("Collecting data from sensors...")
    data = {
        "soil_moisture": read_soil_moisture(),
        "light_level": read_light_level(),
        "temperature": read_temperature(),
        "humidity": read_humidity()
    }
    return data

def is_soil_moisture_sufficient(moisture):
    """
    Checks if soil moisture is above the threshold.
    """
    return moisture >= SOIL_MOISTURE_THRESHOLD

def is_light_level_sufficient(light_level):
    """
    Checks if light level is above the threshold.
    """
    return light_level >= LIGHT_LEVEL_THRESHOLD

def is_temperature_optimal(temperature):
    """
    Checks if the temperature is within the optimal range.
    """
    return TEMPERATURE_RANGE[0] <= temperature <= TEMPERATURE_RANGE[1]

def is_humidity_optimal(humidity):
    """
    Checks if the humidity is within the optimal range.
    """
    return HUMIDITY_RANGE[0] <= humidity <= HUMIDITY_RANGE[1]

def print_sensor_status(data):
    """
    Prints the status of each sensor with recommendations.
    """
    print("\nSensor Status Report:")
    if is_soil_moisture_sufficient(data["soil_moisture"]):
        print("- Soil moisture is sufficient.")
    else:
        print("- Soil moisture is too low! Consider watering the plant.")

    if is_light_level_sufficient(data["light_level"]):
        print("- Light level is sufficient.")
    else:
        print("- Light level is too low! Provide additional lighting.")

    if is_temperature_optimal(data["temperature"]):
        print("- Temperature is within the optimal range.")
    else:
        print("- Temperature is not optimal! Adjust the environment.")

    if is_humidity_optimal(data["humidity"]):
        print("- Humidity is within the optimal range.")
    else:
        print("- Humidity is not optimal! Adjust the environment.")

def simulate_sensor_readings():
    """
    Simulates continuous readings from sensors.
    """
    print("\nSimulating sensor readings...")
    for _ in range(5):  # Simulate 5 readings
        data = get_sensor_data()
        print_sensor_status(data)
        time.sleep(2)  # Wait for 2 seconds between readings

# Example usage
if __name__ == "__main__":
    initialize_sensors()
    simulate_sensor_readings()