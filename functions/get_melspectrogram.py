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

# imports for deleting audio file
from os import remove
from os.path import exists

# ***************************** class melSpectrogram *****************************
class melSpectrogram:

    def __init__(self, source_filename):
        self.source_filename = source_filename
        self.samplerate = 16000

    def get_MelSpectrogram(self):
        # Loads wav file for analysis, using default samplerate of 16000 if one is not specified
        y, self.sr = librosa.load(self.source_filename, self.samplerate)

        # Creates numpy array of Mel Spectrogram for wav file with the following parameters:
        # sr: samplerate
        # n_mels: the number of mel-filterbanks used
        # n_fft: length of the FFT window
        # fmin: lower frequency
        # fmax: upper frequency
        S = librosa.feature.melspectrogram(y, self.sr, n_mels=40, n_fft=512, fmin=300, fmax=8000)

        # Creates numpy array of the delta of the Mel Spectrogram, will be same dimensions as S above
        ms_delta = librosa.feature.delta(S)

        # Creates numpy array of the delta delta of the Mel Spectrogram, will be same dimensions as S above
        ms_delta2 = librosa.feature.delta(S, order=2)

        # Convert a power spectrogram (amplitude squared) to decibel (dB) units
        self.S_dB = librosa.power_to_db(S, ref=max)

        # Convert a power spectrogram (amplitude squared) to decibel (dB) units
        self.ms_delta_dB = librosa.power_to_db(ms_delta, ref=max)

        # Convert a power spectrogram (amplitude squared) to decibel (dB) units
        self.ms_delta2_dB = librosa.power_to_db(ms_delta2, ref=max)

        self.padToLongest()

        #stacks the arrays depth wise to make a 3D numpy array
        self.output = dstack((self.S_dB_out, self.ms_delta_dB_out, self.ms_delta2_dB_out))
        #self.output = dstack((self.S_dB, self.ms_delta_dB, self.ms_delta2_dB))
        
        # CAN ONLY PLOT ONE FIGURE IN A PYTHON SCRIPT. 
        # uncomment only if there will be only one audio file and you want it displayed
        #self.displaySpectrogram()

        return(self.output)

    def padToLongest(self):
        # pads numpy arrays with zeroes to fit longest wav file used for training (1067) rows
        pad_trim = 224
        self.S_dB_out = librosa.util.fix_length(self.S_dB, pad_trim, axis=1)
        self.ms_delta_dB_out = librosa.util.fix_length(self.ms_delta_dB, pad_trim, axis=1)
        self.ms_delta2_dB_out = librosa.util.fix_length(self.ms_delta2_dB, pad_trim, axis=1)

    def displaySpectrogram(self):
        # Plotting the Mel Spectrogram
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(self.S_dB, x_axis='time',
                                 y_axis='mel', sr=self.samplerate,
                                 fmax=8000)
        plt.colorbar(format='%+2.0f dB')
        plt.title('Mel-frequency spectrogram')
        plt.tight_layout()
        plt.show(block=False)

    def saveFile(self):
        # use current time to calculate a unique number
        unique_num = int(time.time())
        self.filename = 'numpy_output\\Output' + str(unique_num)
        save(self.filename, self.output)

        # print confirmation that the file was saved
        print("file " + self.filename + ".npy saved")

    def deleteFile(self):
        if(exists(self.source_filename)):
            remove(self.source_filename)
            print("file " + str(self.source_filename) + " deleted")
        else:
            print("FILE ERROR: cannot remove file")

# ***************************** main *****************************
def main():
    print("main function of get_melspectrogram.py")

if __name__ == '__main__':
    main()