#!/usr/bin/python
import sys
from pathlib import Path
from ia.audio.input import Audio
from ia.model import ModelLoader

MODEL_PATH = Path("ia/models/spectrogram_model_test.keras")

if __name__ == "__main__":
    model = ModelLoader(MODEL_PATH)
    audio = None
    msg = ""
    save_path = Path("spectrogram.png") 

    sys.stdout.write("ready")

    while msg != "exit":
        match msg:
            case "audio":
                audio_path = input()
                audio_path = audio_path.replace('\x00', '')
                audio = Audio(Path(audio_path))
                audio.save_spectrogram(save_path)
                print("done")

            case "classify":
                prediction = model.predict(save_path)[0]
                print(prediction)

            case _:
                pass
        msg = input()
