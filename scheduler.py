# scheduler.py
# Handles scheduling for the Plant Monitoring System.

import schedule
import time
from datetime import datetime
from database import add_log, add_schedule, get_schedules, delete_schedule

# Function to simulate watering
def water_plants(duration):
    """
    Simulates the watering process.
    """
    add_log(f"Started watering plants for {duration} minutes.")
    time.sleep(duration * 60)
    add_log("Completed watering plants.")

# Function to simulate lighting
def control_lights(action):
    """
    Simulates turning lights on or off.
    """
    if action not in ["on", "off"]:
        raise ValueError("Invalid action for lights. Use 'on' or 'off'.")
    add_log(f"Lights turned {action}.")

# Schedule management
def schedule_watering(time, duration):
    """
    Schedules a watering task.
    """
    add_schedule("watering", time, duration)
    schedule.every().day.at(time).do(water_plants, duration)
    print(f"Watering scheduled at {time} for {duration} minutes.")

def schedule_lighting(time, action):
    """
    Schedules a lighting task.
    """
    add_schedule("lighting", time, 0)  # Duration not required for lights
    schedule.every().day.at(time).do(control_lights, action)
    print(f"Lights scheduled to turn {action} at {time}.")

def run_scheduled_tasks():
    """
    Runs scheduled tasks in a loop.
    """
    print("Scheduler started. Running tasks...")
    while True:
        schedule.run_pending()
        time.sleep(1)

def cancel_all_schedules():
    """
    Cancels all scheduled tasks and clears the database.
    """
    for job in schedule.jobs:
        schedule.cancel_job(job)
    for row in get_schedules():
        delete_schedule(row[0])
    add_log("All schedules canceled.")

# Example usage
if __name__ == "__main__":
    # Schedule watering and lighting
    schedule_watering("08:00", 15)
    schedule_lighting("19:00", "on")
    schedule_lighting("23:00", "off")

    # Start running scheduled tasks
    try:
        run_scheduled_tasks()
    except KeyboardInterrupt:
        print("Scheduler stopped.")
        cancel_all_schedules()