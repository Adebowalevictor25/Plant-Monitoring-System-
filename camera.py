# camera.py
# Functions for capturing images of plants and managing the camera.

import time
import os
from datetime import datetime

# Constants for camera configuration
IMAGE_DIRECTORY = "images"
CAMERA_INITIALIZED = False


def setup_camera():
    """
    Simulates the setup and initialization of the camera.
    """
    global CAMERA_INITIALIZED
    print("Setting up the camera...")
    time.sleep(2)  # Simulate delay
    CAMERA_INITIALIZED = True
    print("Camera setup complete.")


def capture_image():
    """
    Captures an image using the camera.
    Returns the path to the saved image.
    """
    if not CAMERA_INITIALIZED:
        raise RuntimeError("Camera has not been initialized. Please call setup_camera() first.")
    
    # Ensure the image directory exists
    if not os.path.exists(IMAGE_DIRECTORY):
        os.makedirs(IMAGE_DIRECTORY)

    # Simulate image capture
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = os.path.join(IMAGE_DIRECTORY, f"plant_image_{timestamp}.jpg")
    print(f"Capturing image... (simulated save at {image_path})")
    time.sleep(1)  # Simulate delay
    with open(image_path, "w") as img_file:
        img_file.write("Simulated image data.")
    
    return image_path


def delete_old_images(days=7):
    """
    Deletes images older than the specified number of days.
    """
    if not os.path.exists(IMAGE_DIRECTORY):
        print(f"No images to clean up. Directory '{IMAGE_DIRECTORY}' does not exist.")
        return

    current_time = time.time()
    deleted_files = 0

    for filename in os.listdir(IMAGE_DIRECTORY):
        file_path = os.path.join(IMAGE_DIRECTORY, filename)
        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > days * 86400:  # Convert days to seconds
                os.remove(file_path)
                deleted_files += 1
                print(f"Deleted old image: {filename}")

    print(f"Cleanup complete. {deleted_files} files deleted.")


def list_images():
    """
    Lists all images in the image directory.
    """
    if not os.path.exists(IMAGE_DIRECTORY):
        print(f"No images found. Directory '{IMAGE_DIRECTORY}' does not exist.")
        return []

    images = [f for f in os.listdir(IMAGE_DIRECTORY) if f.endswith(".jpg")]
    print(f"Found {len(images)} images in '{IMAGE_DIRECTORY}':")
    for image in images:
        print(f"- {image}")
    return images


def simulate_camera_operation():
    """
    Simulates the camera capturing and managing images over time.
    """
    print("\nStarting camera simulation...")
    setup_camera()

    for i in range(5):
        try:
            print(f"\nIteration {i + 1}:")
            image_path = capture_image()
            print(f"Image captured at: {image_path}")

            if i == 3:  # Simulate cleanup on the 4th iteration
                print("\nCleaning up old images...")
                delete_old_images(days=0)

        except Exception as e:
            print(f"Error during camera operation: {e}")

        time.sleep(2)

    print("\nListing all remaining images:")
    list_images()


# Example usage
if __name__ == "__main__":
    simulate_camera_operation()