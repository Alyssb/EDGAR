#! /usr/bin/env python

import sys
import librosa
import librosa.display
from numpy import max


def get_MelSpectrogram(source_filename, samplerate=48000):
    y, sr = librosa.load(source_filename, samplerate)
    S = librosa.feature.melspectrogram(y, sr)
    # Passing through arguments to the Mel filters

    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 4))
    S_dB = librosa.power_to_db(S, ref=max)
    librosa.display.specshow(S_dB, x_axis='time',
                             y_axis='mel', sr=samplerate,
                             fmax=8000)
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel-frequency spectrogram')
    plt.tight_layout()
    plt.show()
