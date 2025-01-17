from pathlib import Path
import librosa
import matplotlib.pyplot as plt
import numpy as np

class Audio:
    def __init__(self, audio_path: Path, sr=22050):
        """
            Initialize the audio class
            Args:
                audio_path: Path to the audio file
                sr: Sample rate
        """
        self.load_new_audio(audio_path, sr)
    

    def load_new_audio(self, audio_path: Path, my_sr=22050):
        """
            Load new audio file
            Args:
                audio_path: Path to the new audio file
                sr: Sample rate
        """
        self.audio_path = audio_path
        self._audio, self._sr = librosa.load(audio_path, sr = my_sr)
        self._spectrogram = self._generate_spectrogram()

    def get_spectrogram(self):
        """
            Get spectrogram
            Returns:
                Spectrogram
        """
        return self._spectrogram

    def get_audio(self):
        """
            Get audio time series
            Returns:
                Audio time series
        """
        return self._audio

    def get_sr(self):
        """
            Get sample rate
            Returns:
                Sample rate
        """
        return self._sr
    
    def save_spectrogram(self, save_path: Path, verbose=False):
        """
            Save spectrogram
            Args:
                save_path: Path to save the spectrogram
        """
        if verbose:
            print(f"Saving spectrogram to {save_path}")
        try:
            librosa.display.specshow(librosa.power_to_db(self._spectrogram, ref=np.max), sr=self._sr)
            if verbose:
                plt.colorbar(format='%+2.0f dB')
            else:
                plt.axis('off')
            plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
            if verbose:
                print("Spectrogram saved successfully")
                print(f"Spectrogram saved to {save_path}")
                print(f"Spectrogram: {plt.show()}")
            plt.close()
        except Exception as e:
            print(f"Error while saving spectrogram: {e}")

    def _generate_spectrogram(self, n_fft=2048, hop_length=512):
        """
            Generate spectrogram
            Returns:
                Spectrogram
        """
        return librosa.feature.melspectrogram(y=self._audio, sr=self._sr, n_fft=n_fft, hop_length=hop_length)
