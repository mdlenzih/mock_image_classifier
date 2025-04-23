"""
This module provides a mock image classification model for testing and development purposes.
It simulates the behavior of a real image classifier by introducing artificial delays and
returning random predictions from a predefined set of classes (cat, dog, banana, toaster).
This is useful for testing API endpoints and frontend functionality without requiring
an actual trained model.
"""

import random
from time import sleep

class MockModel:
    def __init__(self):
        self.classes = ["cat", "dog", "banana", "toaster"]
        print("Loading fake model weights...")
        sleep(1)  # Simulate load time
        print("Model ready.")

    def preprocess(self, file):
        print("Preprocessing file...")
        sleep(0.5)  # Simulate processing time
        return "mock_image_tensor"

    def predict(self, processed_img):
        print(f" Predicting on: {processed_img}")
        sleep(0.5)
        return random.choice(self.classes)
