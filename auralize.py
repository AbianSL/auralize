#!/usr/bin/python

from logging import error
import time
import numpy as np
# import tensorflow as tf

from pathlib import Path
from audio.input import Audio

def load_model():
    time.sleep(1)
    return "anything"
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
                audio_path = audio_path.replace('\x00', '')
                audio = Audio(Path(audio_path))
                audio.save_spectrogram(Path("spectrogram.png"));
                print("done")

            case _:
                pass

        msg = input()
