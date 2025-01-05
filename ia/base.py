from ..Audio.input import Audio 
from ..download import download_all_files

from pathlib import Path
import numpy as np
import os

import tensorflow as tf
import pandas as pd
from keras.preprocessing import image

class SpectrogramTrainer:
    def __init__(self, spectrogram_dir: Path,
                 label_csv: Path, model_dir: Path):
        """
            Initialize the spectrogram trainer
            Args:
                spectrogram_dir: Path to the spectrogram directory
                label_csv: Path to the label csv file
                model_dir: Path to the model directory
        """
        self.spectrogram_dir = spectrogram_dir
        self.label_csv = label_csv
        self.model_dir = model_dir
        self.spectrograms = []
        self.labels = []
        self._load_data()

    def _load_data(self):
        """
            Load data
        """
        self._load_spectrograms()
        self._load_labels()

    def _load_spectrograms(self):
        """
            Load spectrograms
        """
        images = []
        labels = []
        for file in os.listdir(self.spectrogram_dir):
            images.append(image.img_to_array(image.load_img(os.path.join(self.spectrogram_dir, file), target_size=(224, 224, 3))))
            labels.append((label))
        return images, labels

    def _load_labels(self):
        """
            Load labels
        """
        pass 

if __name__ == "__main__":
    spectrogram_dir = Path("data/spectrograms")
    label_csv = Path("data/labels.csv")
    model_dir = Path("models")
    trainer = SpectrogramTrainer(spectrogram_dir, label_csv, model_dir)
    print(trainer.spectrograms)
    
