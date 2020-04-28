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


    '''
    function: displaySpectrogram
    displays the melspectrogram created
    uses built-in PyPlot functions
    '''
    def displaySpectrogram(self):
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(self.S_dB, x_axis='time',
                                 y_axis='mel', sr=self.samplerate,
                                 fmax=8000)
        plt.colorbar(format='%+2.0f dB')
        plt.title('Mel-frequency spectrogram')
        plt.tight_layout()
        plt.show()


    '''
    function: saveSpectrogram
    saves spectrogram as a png image
    local variables:
        fig (Figure):               figure to be saved
        canvas (FigureCanvasAgg):   canvas to hold the figure
        ax
    '''
    def saveSpectrogram(self):
        fig = plt.Figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)   # I have no idea what this does
        librosa.display.specshow(librosa.amplitude_to_db(self.S_dB, ref=max), ax=ax, y_axis='log', x_axis='time')
        fig.savefig('spec.png')
        self.saveFile(fig)

        canvas.draw()
        self.data = frombuffer(fig.canvas.tostring_rgb(), dtype=uint8)
        self.data = self.data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        # self.deleteFile() # uncomment for final implementation


    '''
    function: saveFile
    saves spectrogram as rgb npy array
    class variables:
        filename (string):  filename to save npy array in
    local variables:
        unique_num (int):   current time in seconds, used to create unique filenames
    '''
    def saveFile(self, image):
        unique_num = int(time.time())
        self.filename = 'mfcc-outputs\\output-' + str(unique_num)
        # not sure what this line does
        save(self.filename, self)
        print("file " + self.filename + ".npy saved")


    '''
    function: deleteFile
    deletes original audio file
    '''
    def deleteFile(self):
        if(exists(self.source_filename)):
            remove(self.source_filename)
            print("file " + str(self.source_filename) + " deleted")
        else:
            print("FILE ERROR: cannot find file to remove")

# ***************************** main *****************************
def main():
    print("main function of get_melspectrogram.py")

    # create instance of melSpectrogram
    mSpec = melSpectrogram("live_audio\\1587785357.wav")

    # create melSpectrogram metric from file
    mSpec.get_MelSpectrogram()

    # save melspectrogram as a 3D numpy array for processing
    mSpec.saveSpectrogram()


if __name__ == '__main__':
    main()