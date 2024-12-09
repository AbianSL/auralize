from pathlib import Path
import librosa

def load_audio(audio_path: Path, sr=22050):
    y, sr = librosa.load(audio_path, sr=sr)
    return y, sr
