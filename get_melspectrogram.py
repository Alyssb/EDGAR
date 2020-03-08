#! /usr/bin/env python
'''
CSC450 SP 2020 Group 4
03/08/2020
creates, stores, and returns a spectrogram for a given audio file

currently called by EDGAR_demo.py
'''

################################### imports ######################################
# You will need to pip install all of these things
import librosa
import librosa.display
from numpy import max, dstack, save
import matplotlib.pyplot as plt
import time


################################### class melSpectrogram ######################################
class melSpectrogram:

    def __init__(self, source_filename):
        self.source_filename = source_filename
        self.samplerate = 16000

    def get_MelSpectrogram(self):
        y, sr = librosa.load(self.source_filename, self.samplerate)
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
        # plt.figure(figsize=(10, 4))
        # librosa.display.specshow(S_dB, x_axis='time',
        #                          y_axis='mel', sr=samplerate,
        #                          fmax=8000)
        # plt.colorbar(format='%+2.0f dB')
        # plt.title('Mel-frequency spectrogram')
        # plt.tight_layout()
        # plt.show()
        self.saveFile(output)
        return output

    def saveFile(self, contents):
        unique_num = int(time.time())
        filename = 'numpy_output\\Output' + str(unique_num)
        save(filename, contents)
        print(filename + ".npy saved")

def main():
    print("main function of get_melspectrogram.py")

if __name__ == '__main__':
    main()