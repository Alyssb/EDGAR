#! /usr/bin/env python
# This is just cory's code stolen
# I will not be using system arguments, and instead going through it manually
# must be run from the directory EDGAR in the project.

import sys
from aubio import source, pvoc, mfcc
from numpy import vstack, zeros, diff
from numpy import save, load, set_printoptions #Cory's mess
import time #file naming scheme - Cory

n_filters = 40              # must be 40 for mfcc
n_coeffs = 13
root = ".\\CSC450\\data\\Audio_Speech_Actors_01-24\\"

if len(sys.argv) < 2:
    print("Usage: %s <source_filename> [samplerate] [win_s] [hop_s] [mode]" % sys.argv[0])
    print("  where [mode] can be 'delta' or 'ddelta' for first and second derivatives")
    #sys.exit(1)

source_filename = root + "Actor_01\\03-01-01-01-01-01-01.wav"

samplerate = 0
win_s = 512
hop_s = win_s // 4
mode = "default"

s = source(source_filename, samplerate, hop_s)
samplerate = s.samplerate
p = pvoc(win_s, hop_s)
m = mfcc(win_s, n_filters, n_coeffs, samplerate)

mfccs = zeros([n_coeffs,])
frames_read = 0
while True:
    samples, read = s()
    spec = p(samples)
    mfcc_out = m(spec)
    mfccs = vstack((mfccs, mfcc_out))
    frames_read += read
    if read < hop_s: break

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