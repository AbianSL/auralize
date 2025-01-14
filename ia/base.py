from ..Audio.input import Audio 
from ..download import download_all_files

from pathlib import Path
import numpy as np
import os

import tensorflow as tf
import pandas as pd
from keras.preprocessing import image
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Flatten, Dense

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
        self.model = Sequential() 
        self._load_data()

    def _load_data(self):
        """
            Load data
        """
        self._load_spectrograms()
        self._load_labels()

    def train(self):
        """
            Train the model
        """
        # layer 1
        self.model.add(Conv2D(32, (3, 3), input_shape=(224, 224, 3), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        # layer 2
        self.model.add(Conv2D(32, (3, 3), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        # layer 3
        self.model.add(Conv2D(64, (3, 3), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        # layer 4
        self.model.add(Conv2D(64, (3, 3), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Flatten())
        self.model.add(Dense(units=128, activation='relu'))
        self.model.add(Dense(units=1, activation='sigmoid'))
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        self.model.summary()

        print("Training the model")
        # TODO: how to train the model
        # self.model.fit(self.spectrograms, self.labels, epochs=10, batch_size=32)

    def _load_spectrograms(self):
        """
            Load spectrograms
        """
        pass 

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
    
