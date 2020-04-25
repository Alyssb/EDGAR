#! /usr/bin/env python
'''
CSC450 SP 2020 Group 4
Missouri State University

Creates, stores, and returns a spectrogram for a given audio file
'''

# ***************************** imports *****************************
# general imports
from numpy import max, dstack, save, frombuffer, set_printoptions, array, uint8, float64
import matplotlib
matplotlib.use('Agg')

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas, FigureCanvasAgg
import matplotlib.pyplot as plt
from scipy import io
import time

# audio imports
import librosa
import librosa.display

# imports for deleting audio file
from os import remove
from os.path import exists

# ***************************** class melSpectrogram *****************************


class melSpectrogram:
    ''' init function '''
    def __init__(self, source_filename):
        self.source_filename = source_filename
        self.samplerate = 16000


    '''
    function: get_MelSpectrogram
    creates a spectrogram from a WAV file
    class variables:
        sr (int):           sample rate
        S (numpy array):    power spectrogram (amplitude squared)
        S_dB (numpy array): power spectrogram with decibel units
    local variables:
        y (float array):    loaded WAV file
        n_mels (int):       number of mel-filterbanks used
        n_fft (int):        length of the FFT window
        fmin (int):         lower frequency
        fmax (int):         upper frequency
    '''
    def get_MelSpectrogram(self):
        y, self.sr = librosa.load(self.source_filename, self.samplerate)                                # Loads wav file for analysis
        self.S = librosa.feature.melspectrogram(y, self.sr, n_mels=40, n_fft=512, fmin=300, fmax=8000)  # creates numpy array spectrogram
        self.S_dB = librosa.power_to_db(self.S, ref=max)    # convert power spectrogram to decibel units

        print("Mel Spectrogram")
        print(self.S_dB)




    ''' unused, I think '''
    # def padToLongest(self):
    #     # pads numpy arrays with zeroes to fit longest wav file used for training (1067) rows
    #     self.S_dB_out = librosa.util.fix_length(self.S_dB, 1067, axis=1)
    #     self.ms_delta_dB_out = librosa.util.fix_length(self.ms_delta_dB, 1067, axis=1)
    #     self.ms_delta2_dB_out = librosa.util.fix_length(self.ms_delta2_dB, 1067, axis=1)


    ''' unused, I think '''
    # def displaySpectrogram(self):
    #     # Plotting the Mel Spectrogram
    #     plt.figure(figsize=(10, 4))
    #     librosa.display.specshow(self.S_dB, x_axis='time',
    #                              y_axis='mel', sr=self.samplerate,
    #                              fmax=8000)
    #     plt.colorbar(format='%+2.0f dB')
    #     plt.title('Mel-frequency spectrogram')
    #     plt.tight_layout()
    #     plt.show()


    '''
    function: saveSpectrogram
    saves a spectrogram as a rgb numpy array
    local variables:
        fig (640x480 Figure):               figure to store spectrogram data
        canvas (MatPlotLib Canvas Object):  Canvas instance which contains fig
        ax 
    '''
    def saveSpectrogram(self):
        fig = plt.Figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)   # I have no idea what this does, pls fill out in comment above fxn ty
        print(ax)
        librosa.display.specshow(librosa.amplitude_to_db(self.S_dB, ref=max), ax=ax, y_axis='log', x_axis='time')
        fig.savefig('spec.png')

        ''' what does all this stuff do? Is it necessary? '''
        # canvas.draw()
        # data = frombuffer(fig.canvas.tostring_rgb(), dtype=uint8)
        # print("data1")
        # print(data)
        # data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        # print("data2")
        # print(data)


    ''' unused, I think '''
    # def saveFile(self, image):
    #     # use current time to calculate a unique numbe
    #     unique_num = int(time.time())
    #     self.filename = 'C:\\Users\\alyss\\Documents\\EDGAR\\mfcc-outputs' + str(unique_num)
    #     save(self.filename, self)

    #     # print confirmation that the file was saved
    #     # print("file " + self.filename + ".npy saved")


    def deleteFile(self):
        if(exists(self.source_filename)):
            remove(self.source_filename)
            print("file " + str(self.source_filename) + " deleted")
        else:
            print("FILE ERROR: cannot remove file")

# ***************************** main *****************************
def main():
    print("main function of get_melspectrogram.py")
    mSpec = melSpectrogram("C:\\Users\\alyss\\Documents\\EDGAR\\live_audio\\1587785357.wav")
    mSpec.get_MelSpectrogram()  # creates a mel spectrogram for a given file

    print("ms from main")
    print(mSpec.S_dB)
    # mSpec.saveFile()  # Saves 3D numpy output array to a file
    mSpec.saveSpectrogram()


if __name__ == '__main__':
    main()