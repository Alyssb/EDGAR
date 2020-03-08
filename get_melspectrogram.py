#! /usr/bin/env python
'''
CSC450 SP 2020 Group 4
03/08/2020
creates, stores, and returns a spectrogram for a given audio file

currently called by EDGAR_demo.py
'''

# ***************************** imports *****************************
# You will need to pip install all of these things
import librosa
import librosa.display
from numpy import max, dstack, save
import matplotlib.pyplot as plt
import time

# ***************************** class melSpectrogram *****************************
class melSpectrogram:

    def __init__(self, source_filename):
        self.source_filename = source_filename
        self.samplerate = 16000

    def get_MelSpectrogram(self):
        # I don't really know what these do, someone else should document this
        y, self.sr = librosa.load(self.source_filename, self.samplerate)
        S = librosa.feature.melspectrogram(y, self.sr, n_mels=40, n_fft=512, fmin=300, fmax=8000)
        ms_delta = librosa.feature.delta(S)
        ms_delta2 = librosa.feature.delta(S, order=2)

        # Passing through arguments to the Mel filters
        self.S_dB = librosa.power_to_db(S, ref=max)
        S_dB_out = librosa.util.fix_length(self.S_dB, 1067, axis=1)
        ms_delta_dB = librosa.power_to_db(ms_delta, ref=max)
        ms_delta_dB_out = librosa.util.fix_length(ms_delta_dB, 1067, axis=1)
        ms_delta2_dB = librosa.power_to_db(ms_delta2, ref=max)
        ms_delta2_dB_out = librosa.util.fix_length(ms_delta2_dB, 1067, axis=1)
        self.output = dstack((S_dB_out, ms_delta_dB_out, ms_delta2_dB_out))
        
        # CAN ONLY PLOT ONE FIGURE IN A PYTHON SCRIPT. uncomment only if there will be only one audio file
        # self.displaySpectrogram()

        self.saveFile(self.output)
        return(self.output)

    def displaySpectrogram(self):
        # Plotting the Mel Spectrogram
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(self.S_dB, x_axis='time',
                                 y_axis='mel', sr=self.samplerate,
                                 fmax=8000)
        plt.colorbar(format='%+2.0f dB')
        plt.title('Mel-frequency spectrogram')
        plt.tight_layout()
        plt.show()

    def saveFile(self, contents):
        unique_num = int(time.time())
        filename = 'numpy_output\\Output' + str(unique_num)
        save(filename, contents)
        print("file " + filename + ".npy saved")

# ***************************** main *****************************
def main():
    print("main function of get_melspectrogram.py")

if __name__ == '__main__':
    main()