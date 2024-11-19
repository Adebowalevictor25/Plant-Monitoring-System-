# database.py
# Handles database operations for the Plant Monitoring System.

import sqlite3
from datetime import datetime

# Constants
DATABASE_FILE = "plant_monitoring.db"


def initialize_database():
    """
    Initializes the database and creates necessary tables.
    """
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        # Create sensors data table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            soil_moisture INTEGER,
            light_level INTEGER,
            temperature REAL,
            humidity REAL
        )
        """)

        # Create logs table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            action TEXT
        )
        """)

        # Create schedule table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device TEXT,
            schedule_time DATETIME,
            duration INTEGER
        )
        """)

        connection.commit()
        connection.close()
        print("Database initialized successfully.")
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")


def add_sensor_data(soil_moisture, light_level, temperature, humidity):
    """
    Adds new sensor data to the database.
    """
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO sensor_data (soil_moisture, light_level, temperature, humidity)
        VALUES (?, ?, ?, ?)
        """, (soil_moisture, light_level, temperature, humidity))

        connection.commit()
        connection.close()
        print("Sensor data added successfully.")
    except sqlite3.Error as e:
        print(f"Error adding sensor data: {e}")


def get_sensor_data_history(limit=10):
    """
    Retrieves the most recent sensor data from the database.
    """
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        cursor.execute("""
        SELECT * FROM sensor_data
        ORDER BY timestamp DESC
        LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()
        connection.close()
        return rows
    except sqlite3.Error as e:
        print(f"Error retrieving sensor data: {e}")
        return []


def add_log(action):
    """
    Adds a new log entry to the database.
    """
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO logs (action)
        VALUES (?)
        """, (action,))

        connection.commit()
        connection.close()
        print("Log added successfully.")
    except sqlite3.Error as e:
        print(f"Error adding log: {e}")


def get_logs(limit=10):
    """
    Retrieves the most recent logs from the database.
    """
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        cursor.execute("""
        SELECT * FROM logs
        ORDER BY timestamp DESC
        LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()
        connection.close()
        return rows
    except sqlite3.Error as e:
        print(f"Error retrieving logs: {e}")
        return []


def add_schedule(device, schedule_time, duration):
    """
    Adds a new schedule to the database.
    """
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO schedules (device, schedule_time, duration)
        VALUES (?, ?, ?)
        """, (device, schedule_time, duration))

        connection.commit()
        connection.close()
        print("Schedule added successfully.")
    except sqlite3.Error as e:
        print(f"Error adding schedule: {e}")


def get_schedules():
    """
    Retrieves all schedules from the database.
    """
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        cursor.execute("""
        SELECT * FROM schedules
        ORDER BY schedule_time ASC
        """)

        rows = cursor.fetchall()
        connection.close()
        return rows
    except sqlite3.Error as e:
        print(f"Error retrieving schedules: {e}")
        return []


def delete_schedule(schedule_id):
    """
    Deletes a schedule from the database by ID.
    """
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        cursor.execute("""
        DELETE FROM schedules
        WHERE id = ?
        """, (schedule_id,))

        connection.commit()
        connection.close()
        print("Schedule deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting schedule: {e}")


# Example usage
if __name__ == "__main__":
    initialize_database()
    add_sensor_data(45, 300, 25.5, 60)
    print("Recent Sensor Data:")
    for row in get_sensor_data_history():
        print(row)
    add_log("Test log entry")
    print("Recent Logs:")
    for row in get_logs():
        print(row)
    add_schedule("watering", "2024-11-19 08:00:00", 15)
    print("Schedules:")
    for row in get_schedules():
        print(row)