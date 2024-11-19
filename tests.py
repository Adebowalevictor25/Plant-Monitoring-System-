# tests.py
# Unit tests for the Plant Monitoring System.

import unittest
from sensors import get_sensor_data, read_soil_moisture
from ai_model import preprocess_image, analyze_plant_image
from database import (
    initialize_database,
    add_sensor_data,
    get_sensor_data_history,
    add_log,
    get_logs,
)
from utilities import validate_schedule_time, format_sensor_data
from notifier import send_telegram_notification

class TestSensors(unittest.TestCase):
    def test_get_sensor_data(self):
        """
        Tests if the sensor data retrieval returns a valid format.
        """
        data = get_sensor_data()
        self.assertIn("soil_moisture", data)
        self.assertIn("light_level", data)
        self.assertIn("temperature", data)
        self.assertIn("humidity", data)

    def test_read_soil_moisture(self):
        """
        Tests the soil moisture sensor value.
        """
        value = read_soil_moisture()
        self.assertGreaterEqual(value, 0)
        self.assertLessEqual(value, 100)

class TestAIModel(unittest.TestCase):
    def test_preprocess_image(self):
        """
        Tests if the image preprocessing returns a valid array.
        """
        image_path = "test_image.jpg"
        array = preprocess_image(image_path)
        self.assertEqual(array.shape, (224, 224, 3))

    def test_analyze_plant_image(self):
        """
        Tests the AI analysis function.
        """
        image_path = "test_image.jpg"
        result = analyze_plant_image(image_path)
        self.assertIn("Healthy", result)
        self.assertIn("Diseased", result)

class TestDatabase(unittest.TestCase):
    def setUp(self):
        """
        Initializes the database for testing.
        """
        initialize_database()

    def test_add_sensor_data(self):
        """
        Tests adding sensor data to the database.
        """
        add_sensor_data(45, 300, 25.5, 60)
        data = get_sensor_data_history()
        self.assertGreater(len(data), 0)

    def test_add_log(self):
        """
        Tests adding a log entry.
        """
        add_log("Test log entry")
        logs = get_logs()
        self.assertGreater(len(logs), 0)

class TestUtilities(unittest.TestCase):
    def test_validate_schedule_time(self):
        """
        Tests if a valid schedule time is accepted.
        """
        valid_time = "2024-11-20 14:00:00"
        self.assertTrue(validate_schedule_time(valid_time))

    def test_format_sensor_data(self):
        """
        Tests formatting of sensor data.
        """
        sensor_data = {
            "soil_moisture": 50,
            "light_level": 300,
            "temperature": 22.5,
            "humidity": 45,
        }
        formatted = format_sensor_data(sensor_data)
        self.assertIn("Soil Moisture", formatted)
        self.assertIn("Light Level", formatted)

class TestNotifier(unittest.TestCase):
    def test_send_telegram_notification(self):
        """
        Tests sending a Telegram notification.
        """
        try:
            send_telegram_notification("123456789", "Test notification")
            success = True
        except Exception:
            success = False
        self.assertTrue(success)

if __name__ == "__main__":
    unittest.main()