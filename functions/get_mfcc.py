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
from numpy import max, dstack, save, frombuffer
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import time

# imports for deleting audio file
from os import remove
from os.path import exists

# ***************************** class mfcc *****************************
class mfcc:

    def __init__(self, source_filename):
        self.source_filename = source_filename
        self.samplerate = 16000

    def get_mfcc(self):
        # Loads wav file for analysis, using default samplerate of 16000 if one is not specified
        y, self.sr = librosa.load(self.source_filename, self.samplerate)

        # Creates numpy array of mfcc for wav file with the following parameters:
        #  y: np.ndarray[shape = (n,)] or None
        # sr: sample rate
        # S: Mel Spectrogram or None
        # n_mfcc: num of mfcc's to return
        # dct_type: Discrete Cosine Transform, default 2 {1, 2, 3}
        # norm: None or ‘ortho’: If dct_type is 2 or 3, setting norm =’ortho’ uses
        # an ortho - normal DCT basis.
        # lifter: number >= 0 (cepstral filtering)

        mfccs = librosa.feature.mfcc(y=y, sr=self.samplerate, n_mfcc=40)

        return(self.saveSpectrogram())

    def padToLongest(self):
        # pads numpy arrays with zeroes to fit longest wav file used for training (1067) rows
        self.S_dB_out = librosa.util.fix_length(self.S_dB, 1067, axis=1)
        self.ms_delta_dB_out = librosa.util.fix_length(self.ms_delta_dB, 1067, axis=1)
        self.ms_delta2_dB_out = librosa.util.fix_length(self.ms_delta2_dB, 1067, axis=1)

    def displaySpectrogram(self):
        # Plotting the MFCC
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(self.S_dB, x_axis='time',
                                 y_axis='mfcc', sr=self.samplerate,
                                 fmax=8000)
        plt.colorbar(format='%+2.0f dB')
        plt.title('MFCC')
        plt.tight_layout()
        plt.show()

    def saveSpectrogram(self):
        # Save spectrogram as rgb numpy array
        fig = Figure()
        fig.tight_layout(pad=0)
        canvas = FigureCanvas(fig)

        ax = fig.gca()
        ax.axis('off')
        ax.margins(0)

        canvas.draw()  # draw the canvas, cache the renderer

        #makes a 1d array of rgb values
        image = frombuffer(canvas.tostring_rgb(), dtype='uint8')

        #converts to a 3d array of rgb values
        formatted_image = image.reshape(fig.canvas.get_width_height()[::-1]+(3,))
        print("shape of formatted image: ", formatted_image.shape)

        return formatted_image

    def saveFile(self, image):
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
    print("main function of get_mfcc.py")
    mfcc_metrics = mfcc("Ses01F_impro03_F005.wav")
    mfcc_nparray = mfcc_metrics.get_mfcc()  # creates a mfcc for a given file

    #mSpec.saveFile()  # Saves 3D numpy output array to a file
    mfcc_metrics.saveFile(mfcc_metrics.get_mfcc())


if __name__ == '__main__':
    main()
