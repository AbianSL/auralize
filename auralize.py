import numpy as np
# import tensorflow as tf

from pathlib import Path
from sys import argv
from audio.input import Audio

def load_model():
    pass
    # return tf.keras.models.load_model("auralize_model.keras", None, True)


if __name__ == "__main__":
    model = load_model()
    audio = None
    msg = "";

    print("ready")

    while msg != "exit":
        match msg:
            case "audio":
                audio_path = input()
                audio = Audio(Path(audio_path))
                audio.save_spectrogram(Path("spectrogram.png"));
                pass

            case _:
                pass

        msg = input()
