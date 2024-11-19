# ml_training.py
# Script for training the AI model for plant health analysis.

import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# Directories for training and validation data
TRAINING_DIR = "data/train"
VALIDATION_DIR = "data/validation"
MODEL_SAVE_PATH = "plant_ai_model.h5"

# Training parameters
IMG_HEIGHT = 224
IMG_WIDTH = 224
BATCH_SIZE = 32
EPOCHS = 20
CLASS_NAMES = ["Healthy", "Diseased", "Needs Water", "Low Light"]

# Data augmentation and preprocessing
def create_data_generators():
    """
    Creates training and validation data generators with augmentation.
    """
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode="nearest",
    )
    validation_datagen = ImageDataGenerator(rescale=1.0 / 255)

    train_generator = train_datagen.flow_from_directory(
        TRAINING_DIR,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode="categorical",
    )
    validation_generator = validation_datagen.flow_from_directory(
        VALIDATION_DIR,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode="categorical",
    )

    return train_generator, validation_generator


# Model definition
def build_model():
    """
    Builds the CNN model for plant health analysis.
    """
    model = Sequential(
        [
            Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
            MaxPooling2D(2, 2),
            Conv2D(64, (3, 3), activation="relu"),
            MaxPooling2D(2, 2),
            Conv2D(128, (3, 3), activation="relu"),
            MaxPooling2D(2, 2),
            Flatten(),
            Dense(512, activation="relu"),
            Dropout(0.5),
            Dense(len(CLASS_NAMES), activation="softmax"),
        ]
    )
    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )
    return model


# Training the model
def train_model():
    """
    Trains the CNN model and saves the best version.
    """
    train_gen, val_gen = create_data_generators()
    model = build_model()

    # Callbacks for saving the best model and early stopping
    checkpoint = ModelCheckpoint(
        MODEL_SAVE_PATH, monitor="val_accuracy", save_best_only=True, verbose=1
    )
    early_stop = EarlyStopping(monitor="val_loss", patience=5, verbose=1)

    # Train the model
    history = model.fit(
        train_gen,
        epochs=EPOCHS,
        validation_data=val_gen,
        callbacks=[checkpoint, early_stop],
    )

    print("Training complete. Model saved at:", MODEL_SAVE_PATH)
    return history


# Visualizing training results
def plot_training_results(history):
    """
    Plots training and validation accuracy and loss.
    """
    import matplotlib.pyplot as plt

    acc = history.history["accuracy"]
    val_acc = history.history["val_accuracy"]
    loss = history.history["loss"]
    val_loss = history.history["val_loss"]

    epochs = range(len(acc))

    plt.figure(figsize=(12, 6))

    # Accuracy plot
    plt.subplot(1, 2, 1)
    plt.plot(epochs, acc, label="Training Accuracy")
    plt.plot(epochs, val_acc, label="Validation Accuracy")
    plt.title("Training and Validation Accuracy")
    plt.legend()

    # Loss plot
    plt.subplot(1, 2, 2)
    plt.plot(epochs, loss, label="Training Loss")
    plt.plot(epochs, val_loss, label="Validation Loss")
    plt.title("Training and Validation Loss")
    plt.legend()

    plt.show()


# Example usage
if __name__ == "__main__":
    if not os.path.exists(TRAINING_DIR) or not os.path.exists(VALIDATION_DIR):
        print("Training and validation data directories are missing.")
        exit(1)

    print("Starting training...")
    history = train_model()
    plot_training_results(history)