import numpy as np
# import tensorflow as tf

from pathlib import Path
from sys import argv
from audio.input import Audio

if __name__ == "__main__":
    if len(argv) != 2:
        exit(1)
    file_path = Path(argv[1])
    audio = Audio(file_path)
    audio.save_spectrogram(Path("spectrogram.png"));
    exit(0)

    model = tf.keras.models.load_model("auralize_model.keras", None, True)
    spectrogram = np.load("spectrogram.png");
    prediction = model.predict(spectrogram);
