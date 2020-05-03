#! /usr/bin/env python
'''
CSC450 SP 2020 Group 4
Missouri State University

Creates, stores, and returns a spectrogram for a given audio file

FUNCTIONAL REQUIREMENTS
FR.02
NFR.03
NFR.04
EIR.1
DC.02
LDR.1
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

warnings.filterwarnings("ignore", category=SourceChangeWarning)

class melSpectrogram:

    ''' init function '''
    def __init__(self, source_filename):
        self.source_filename = source_filename
        self.samplerate = 16000


    '''
    FR.02   EDGAR shall create a log-mel spectrograph (LMS)
    NFR.03  EDGAR shall create LMS in less than 1 second


    function: get_MelSpectrogram
    creates a spectrogram from a WAV file
    class variables:
        sr (int):           sample rate
        S (numpy array):    power spectrogram (amplitude squared)
        S_dB (numpy array): power spectrogram with decibel units
    local variables:
        y (float array):    loaded WAV file
    '''
    def get_MelSpectrogram(self):
        y, self.sr = librosa.load(self.source_filename, self.samplerate)                                # Loads wav file for analysis
        self.S = librosa.feature.melspectrogram(y, self.sr, n_mels=40, n_fft=512, fmin=300, fmax=8000)  # creates numpy array spectrogram
        self.S_dB = librosa.power_to_db(self.S, ref=max)    # convert power spectrogram to decibel units


    '''
    FR.02   EDGAR shall create a log-mel spectrograph (LMS)
    NFR.03  EDGAR shall create LMS in less than 1 second
    EIR.1   EDGAR shall be able to show the LMS to the user
    
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
    FR.02   EDGAR shall create a log-mel spectrograph (LMS)
    NFR.03  EDGAR shall create LMS in less than 1 second
    NFR.04  EDGAR must be able to store LMS on host machine
    
    function: saveSpectrogram
    saves spectrogram as a png image
    local variables:
        fig (Figure):               figure to be saved
        canvas (FigureCanvasAgg):   canvas to hold the figure
        ax (int):                   defines the axis to use
    '''
    def saveSpectrogram(self):
        fig = plt.Figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        librosa.display.specshow(librosa.amplitude_to_db(self.S_dB, ref=max), ax=ax, y_axis='log', x_axis='time')
        fig.savefig('spec.png')

        canvas.draw()
        self.data = frombuffer(fig.canvas.tostring_rgb(), dtype=uint8)
        self.data = self.data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        self.saveFile()

    '''
    FR.02   EDGAR shall create a log-mel spectrograph (LMS)
    NFR.03  EDGAR shall create LMS in less than 1 second
    NFR.04  EDGAR must be able to store LMS on host machine

    function: saveFile
    saves spectrogram as rgb npy array
    class variables:
        filename (string):  filename to save npy array in
    local variables:
        unique_num (int):   current time in seconds, used to create unique filenames
    '''
    def saveFile(self):
        unique_num = int(time.time())
        self.filename = 'numpy_output/output-' + str(unique_num)
        save(self.filename, self.data)
        print("file " + self.filename + ".npy saved")


    '''
    DC.02   EDGDAR must not retain audio files pot-processing
    LDR.1   EDGAR must not store audio data

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
    mSpec = melSpectrogram("live_audio\\1587785357.wav")    # will not work without this file

    # create melSpectrogram metric from file
    mSpec.get_MelSpectrogram()

    # save melspectrogram as a 3D numpy array for processing
    mSpec.saveSpectrogram()


if __name__ == '__main__':
    main()
