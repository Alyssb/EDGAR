#! /usr/bin/env python
# This is just cory's code stolen
# I will not be using system arguments, and instead going through it manually
# must be run from the directory EDGAR in the project.

import sys
from aubio import source, pvoc, mfcc
from numpy import vstack, zeros, diff
from numpy import save, load, set_printoptions #Cory's mess
import time #file naming scheme - Cory

def getFilename(root):
    return(root + "Actor_01\\03-01-01-01-01-01-01.wav")

# we're doing our best
class doPlotting:
    def __init__(self,filename):
        self.n_filters = 40              # must be 40 for mfcc
        self.n_coeffs = 13

        self.source_filename = filename

        self.samplerate = 0
        self.win_s = 512
        self.hop_s = self.win_s // 4
        self.mode = "default"

        self.s = source(self.source_filename, self.samplerate, self.hop_s)
        self.samplerate = self.s.samplerate
        self.p = pvoc(self.win_s, self.hop_s)
        self.m = mfcc(self.win_s, self.n_filters, self.n_coeffs, self.samplerate)

    def getMFCC(self):
        mfccs = zeros([n_coeffs,])
        frames_read = 0
        
        while True:
            self.samples, read = self.s()
            spec = self.p(self.samples)
            mfcc_out = self.m(spec)
            mfccs = vstack((mfccs, mfcc_out))
            frames_read += read
            if read < self.hop_s: break





# do plotting
from numpy import arange
from demo_waveform_plot import get_waveform_plot
from demo_waveform_plot import set_xlabels_sample2time
import matplotlib.pyplot as plt

fig = plt.figure()
plt.rc('lines',linewidth='.8')
wave = plt.axes([0.1, 0.75, 0.8, 0.19])

get_waveform_plot( source_filename, samplerate, block_size = hop_s, ax = wave)
wave.xaxis.set_visible(False)
wave.yaxis.set_visible(False)

# compute first and second derivatives
if mode in ["delta", "ddelta"]:
    mfccs = diff(mfccs, axis = 0)
if mode == "ddelta":
    mfccs = diff(mfccs, axis = 0)

all_times = arange(mfccs.shape[0]) * hop_s
n_coeffs = mfccs.shape[1]
for i in range(n_coeffs):
    ax = plt.axes ( [0.1, 0.75 - ((i+1) * 0.65 / n_coeffs),  0.8, 0.65 / n_coeffs], sharex = wave )
    ax.xaxis.set_visible(False)
    ax.set_yticks([])
    ax.set_ylabel('%d' % i)
    ax.plot(all_times, mfccs.T[i])


#begin npy saving process
timer = time.time()
output_filename = 'mfcc-outputs\\output-' + str(timer) + '.npy'
save(output_filename, all_times) #save numpy vstack data

#testing- load npy file and display in console
set_printoptions(precision=None, threshold=sys.maxsize)#edit numpy print options
npy_file_test = load(output_filename)
print(npy_file_test)
# print("npy loaded and printed")

# add time to the last axis
set_xlabels_sample2time( ax, frames_read, samplerate)

#plt.ylabel('spectral descriptor value')
ax.xaxis.set_visible(True)
title = 'MFCC for %s' % source_filename
if mode == "delta": title = mode + " " + title
elif mode == "ddelta": title = "double-delta" + " " + title
wave.set_title(title)
plt.show()

def main():
    root = "C:\\Users\\alyss\\Documents\\EDGAR\\CSC450\\data\\Audio_Speech_Actors_01-24\\"
    filename = getFilename(root)
    print("hello world.")

if __name__ == "__main__":
    main()