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
from numpy import max, save, frombuffer, uint8
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import time
import matplotlib.pyplot as plt


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
        self.S = librosa.feature.melspectrogram(y, self.sr, n_mels=40, n_fft=512, fmin=300, fmax=8000)

        # Convert a power spectrogram (amplitude squared) to decibel (dB) units
        self.S_dB = librosa.power_to_db(self.S, ref=max)


    def saveSpectrogram(self):
        # Save spectrogram as rgb numpy array
        fig = plt.Figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        librosa.display.specshow(librosa.amplitude_to_db(self.S_dB, ref=max), ax=ax, y_axis='log', x_axis='time')
        canvas.draw()
        self.data = frombuffer(fig.canvas.tostring_rgb(), dtype=uint8)
        self.data = self.data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    def saveFile(self):
        # use current time to calculate a unique number
        unique_num = int(time.time())
        self.filename = '/Users/Momma/PycharmProjects/EDGAR/numpy_output/Output' + str(unique_num)
        save(self.filename, self)

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

    # create instance of melSpectrogram
    mSpec = melSpectrogram("Ses01F_impro03_F005.wav")

    # create melSpectrogram metric from file
    mSpec.get_MelSpectrogram()  # creates a mel spectrogram for a given file

    # save melspectrogram as a 3D numpy array for processing
    mSpec.saveSpectrogram()


if __name__ == '__main__':
    main()
