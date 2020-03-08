#! /usr/bin/env python
'''
Currently called by EDGAR_demo.py
'''

import librosa
import librosa.display
from numpy import max, dstack
import matplotlib.pyplot as plt


def get_MelSpectrogram(source_filename, samplerate=16000):
    y, sr = librosa.load(source_filename, samplerate)
    S = librosa.feature.melspectrogram(y, sr, n_mels=40, n_fft=512, fmin=300, fmax=8000)
    ms_delta = librosa.feature.delta(S)
    ms_delta2 = librosa.feature.delta(S, order=2)

    # Passing through arguments to the Mel filters
    S_dB = librosa.power_to_db(S, ref=max)
    S_dB_out = librosa.util.fix_length(S_dB, 1067, axis=1)
    ms_delta_dB = librosa.power_to_db(ms_delta, ref=max)
    ms_delta_dB_out = librosa.util.fix_length(ms_delta_dB, 1067, axis=1)
    ms_delta2_dB = librosa.power_to_db(ms_delta2, ref=max)
    ms_delta2_dB_out = librosa.util.fix_length(ms_delta2_dB, 1067, axis=1)
    output = dstack((S_dB_out, ms_delta_dB_out, ms_delta2_dB_out))


    #Plotting the Mel Spectrogram
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(S_dB, x_axis='time',
                             y_axis='mel', sr=samplerate,
                             fmax=8000)
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel-frequency spectrogram')
    plt.tight_layout()
    plt.show()
    return output

def main():
    return get_MelSpectrogram("C:\\Users\\alyss\\Documents\\EDGAR\\live_audio\\Output1582996270.wav")

if __name__ == '__main__':
    main()