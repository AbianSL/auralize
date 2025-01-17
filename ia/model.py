import tensorflow as tf
import json
from pathlib import Path

from .train import SpectrogramTrainer
from .audio.input import Audio

class ModelLoader(SpectrogramTrainer):
    def __init__(self, model_path: Path):
        """
        Initializes the class with the path to the model file.

        :param model_path: Path to the saved model file (.h5, .keras, etc.)
        """
        self.model_path = None 
        self.model = None
        self.labels = None
        self.load_model(model_path)
        self._load_labels()

    def load_model(self, model_path: Path):
        """
        Loads the model from the specified file.

        :raises FileNotFoundError: If the file does not exist.
        """
        self.model_path = model_path
        try:
            self.model = tf.keras.models.load_model(self.model_path)
            # print(f"Model successfully loaded from: {self.model_path}")
        except Exception as e:
            raise FileNotFoundError(f"Error loading the model: {e}")

    def get_summary(self):
        """
        Returns a summary of the loaded model.

        :raises ValueError: If the model has not been loaded yet.
        """
        if self.model is None:
            raise ValueError("The model is not loaded. Use the load_model method first.")

        self.model.summary()
    
    def _load_labels(self):
        """
        Loads the labels from the label file.

        :raises FileNotFoundError: If the file does not exist.
        """
        try:
            with open("./ia/labels.json", "r") as file:
                self.labels = json.load(file)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Error loading labels: {e}")

# Example usage
if __name__ == "__main__":
    # Replace 'path_to_model.h5' with the actual path to your model
    model_loader = ModelLoader(Path("models/spectrogram_model_test.keras"))
    
    try:
        model_loader.get_summary()

        predictions = model_loader.predict(Path("esc50_data/spectrograms/1-137-A-32.png"))
        print("Predictions:", predictions)

    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)

