from audio.input import Audio 

from pathlib import Path
import numpy as np
import os

import tensorflow as tf
import pandas as pd
from tensorflow.keras.utils import to_categorical
from keras.preprocessing import image
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Flatten, Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

class SpectrogramTrainer:
    def __init__(self, spectrogram_dir: Path,
                 label_csv: Path, model_dir: Path) -> None:
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
        self.x_test = None
        self.y_test = None
        self.model = Sequential() 
        self._load_data()

    def _load_data(self) -> None:
        """
            Load data
        """
        matches = self._find_spectrogram_labels()
        self._assing_labels(matches)

    def train(self, epochs_arg : int, batch_size_arg : int) -> None:
        """
            Train the model
        """

        x_train, x_test, y_train, y_test = train_test_split(self.spectrograms, self.labels, stratify=self.labels, test_size=0.2, random_state=0)
        
        x_train_norm = np.array(x_train) / 255
        x_test_norm = np.array(x_test) / 255
        
        encoder = LabelEncoder()

        y_train_encoded = encoder.fit_transform(y_train)
        y_train_encoded = to_categorical(y_train_encoded)
        
        y_test_encoded = encoder.fit_transform(y_test)
        y_test_encoded = to_categorical(y_test_encoded)

        self.x_test = x_test_norm
        self.y_test = y_test_encoded

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

    def _clasify_spectrogram(self, csv_file: Path):
        """
            Classify a spectrogram
            Args:
                csv_file: Path to the csv file
        """

if __name__ == "__main__":

    # Supongamos que estas son las etiquetas de tu conjunto de datos:
    labels = [0, 2, 1, 0]
    
    # Convertimos a one-hot encoding:
    one_hot_labels = to_categorical(labels)
    
    print(one_hot_labels)
    
    pass
    spectrogram_dir = Path("data/spectrograms")
    label_csv = Path("data/labels.csv")
    model_dir = Path("models")
    trainer = SpectrogramTrainer(spectrogram_dir, label_csv, model_dir)
    print(trainer.spectrograms)
    trainer.train()
    
