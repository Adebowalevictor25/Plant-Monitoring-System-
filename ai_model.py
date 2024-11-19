# ai_model.py
# Extended version: Includes simulation, visualization, and logging.

import os
import random
import time
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Constants
MODEL_PATH = "plant_ai_model.h5"
LOG_FILE = "analysis_log.txt"
CLASS_NAMES = ["Healthy", "Diseased", "Needs Water", "Low Light"]
IMAGE_SIZE = (224, 224)

# Simulated AI Model
class SimulatedAIModel:
    def __init__(self):
        print("Simulated AI Model initialized.")

    def predict(self, image_array):
        print("Simulating AI prediction...")
        time.sleep(1)
        probabilities = np.random.dirichlet(np.ones(len(CLASS_NAMES)), size=1)[0]
        return probabilities


# Global model instance
ai_model = None


def log_results(image_path, analysis):
    """
    Logs analysis results to a file.
    """
    with open(LOG_FILE, "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{timestamp} - {image_path}: {analysis}\n")
    print(f"Results logged to {LOG_FILE}")


def visualize_results(analysis):
    """
    Generates a bar chart for the AI analysis results.
    """
    labels = list(analysis.keys())
    values = list(analysis.values())

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='skyblue')
    plt.title("AI Analysis Results")
    plt.xlabel("Classes")
    plt.ylabel("Probability")
    plt.ylim(0, 1)
    plt.show()


def load_ai_model():
    global ai_model
    print(f"Loading AI model from {MODEL_PATH}...")
    time.sleep(2)
    if os.path.exists(MODEL_PATH):
        print("AI model loaded successfully.")
    else:
        print("Model not found. Using simulated model.")
        ai_model = SimulatedAIModel()


def preprocess_image(image_path):
    print(f"Preprocessing image at {image_path}...")
    time.sleep(1)
    image_array = np.random.rand(*IMAGE_SIZE, 3)
    print(f"Image preprocessed: {image_array.shape}")
    return image_array


def analyze_plant_image(image_path):
    if ai_model is None:
        raise RuntimeError("AI model has not been loaded.")

    image_array = preprocess_image(image_path)
    predictions = ai_model.predict(image_array)
    analysis = {CLASS_NAMES[i]: float(predictions[i]) for i in range(len(CLASS_NAMES))}

    print(f"AI Analysis Result: {analysis}")
    log_results(image_path, analysis)
    visualize_results(analysis)
    return analysis


def simulate_large_batch_analysis(num_images=100):
    print(f"Simulating batch analysis for {num_images} images...")
    batch_results = {}
    for i in range(num_images):
        image_path = f"image_{i + 1}.jpg"
        try:
            result = analyze_plant_image(image_path)
            batch_results[image_path] = result
        except Exception as e:
            batch_results[image_path] = f"Error: {e}"
    print(f"Batch analysis complete for {num_images} images.")
    return batch_results


def train_model(training_data_dir, epochs=5):
    print(f"Training model on data from {training_data_dir}...")
    for epoch in range(epochs):
        print(f"Epoch {epoch + 1}/{epochs}")
        for batch in range(10):
            loss = random.uniform(0.2, 1.0)
            print(f"Batch {batch + 1}: Loss={loss:.4f}")
            time.sleep(0.5)
    print("Training complete. Model saved.")


def evaluate_model(test_data_dir):
    print(f"Evaluating model on data from {test_data_dir}...")
    time.sleep(2)
    accuracy = random.uniform(0.7, 0.95)
    print(f"Evaluation Accuracy: {accuracy:.4f}")


# Example usage
if __name__ == "__main__":
    load_ai_model()
    train_model("training_data", epochs=3)
    evaluate_model("test_data")
    results = simulate_large_batch_analysis(100)
    print(f"Logged results for 100 images: {LOG_FILE}")