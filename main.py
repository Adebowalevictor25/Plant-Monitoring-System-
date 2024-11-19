# main.py
# Author: Hrachov Oleksii
# Main entry point for the AI-powered plant monitoring system.

from sensors import get_sensor_data, initialize_sensors
from camera import capture_image, setup_camera
from ai_model import analyze_plant_image, load_ai_model
from telegram_bot import start_bot
from web_interface import start_web_server

def initialize_system():
    """
    Initialize all components of the plant monitoring system.
    This includes sensors, camera, AI model, and communication interfaces.
    """
    print("Initializing system components...")
    # Initialize sensors
    initialize_sensors()
    # Set up the camera
    setup_camera()
    # Load the AI model
    load_ai_model()
    print("All components initialized successfully!")

def main():
    """
    Main function that orchestrates the workflow of the system.
    """
    print("Starting Plant Monitoring System...")

    # Step 1: Initialize system components
    initialize_system()

    # Step 2: Fetch sensor data
    try:
        sensor_data = get_sensor_data()
        print(f"Sensor data: {sensor_data}")
    except Exception as e:
        print(f"Error fetching sensor data: {e}")
        sensor_data = None

    # Step 3: Capture an image of the plant
    try:
        image_path = capture_image()
        print(f"Image captured at: {image_path}")
    except Exception as e:
        print(f"Error capturing image: {e}")
        image_path = None

    # Step 4: Analyze the image with AI
    if image_path:
        try:
            analysis = analyze_plant_image(image_path)
            print(f"AI analysis result: {analysis}")
        except Exception as e:
            print(f"Error analyzing image: {e}")
    else:
        print("Skipping AI analysis due to missing image.")

    # Step 5: Start Telegram bot for notifications
    try:
        start_bot()
    except Exception as e:
        print(f"Error starting Telegram bot: {e}")

    # Step 6: Start web interface for live monitoring
    try:
        start_web_server()
    except Exception as e:
        print(f"Error starting web interface: {e}")

    print("Plant Monitoring System is now running!")

if __name__ == "__main__":
    main()