#! /usr/bin/env python
# This is just cory's code stolen
# I will not be using system arguments, and instead going through it manually
# must be run from the directory EDGAR in the project.

import sys
from os import walk, remove
from aubio import source, pvoc, mfcc    # this line always has an error. Don't know why
from numpy import vstack, zeros, diff
from numpy import save, load, set_printoptions #Cory's mess
import time #file naming scheme - Cory

from numpy import arange
from demo_waveform_plot import get_waveform_plot
from demo_waveform_plot import set_xlabels_sample2time
import matplotlib.pyplot as plt

# hardcoded for current directory
# these files are not available on github
# They're from sharepoint.
class getFiles:
    def __init__(self, root):
        self.root = root

    def travelFolders(self):
        folders = []
        for i in range(1,25):
            folder = "Actor_" + str(i)
            folders.append(folder)
        return folders

    def travelFiles(self):
        files = []
        folders = self.travelFolders()
        for folder in folders:
            for contents in walk(self.root + folder, topdown=True):
                print("CONTENTS AT 0 ", contents[0])
                print("CONTENTS AT 1 ", contents[1])
                # walks through a directory and returns everything inside of it
                # an array of arrays, 3rd is what we want
                files.append(contents[2]) # an array of arrays: array of files per folder
                # print("FILES IN FOLDER ", folder, " ARE ", files)
        print("LEN FILES ",len(files))
        return files

    # def getFilename(self):
    #     self.travelFolders()
    #     return(self.root + "Actor_01\\03-01-01-01-01-01-01.wav")


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

    def calcMFCC(self):
        self.mfccs = zeros([self.n_coeffs,])
        frames_read = 0
        
        while True:
            self.samples, read = self.s()
            spec = self.p(self.samples)
            mfcc_out = self.m(spec)
            self.mfccs = vstack((self.mfccs, mfcc_out))
            frames_read += read
            if read < self.hop_s: break

        return frames_read

    # I would like to break this down further.
    # once I understand it better
    def createPlot(self):
        # do plotting
        fig = plt.figure()
        plt.rc('lines',linewidth='.8')
        self.wave = plt.axes([0.1, 0.75, 0.8, 0.19])

        get_waveform_plot( self.source_filename, self.samplerate, block_size = self.hop_s, ax = self.wave)
        self.wave.xaxis.set_visible(False)
        self.wave.yaxis.set_visible(False)

        # compute first and second derivatives
        if self.mode in ["delta", "ddelta"]:
            self.mfccs = diff(self.mfccs, axis = 0)
        if self.mode == "ddelta":
            self.mfccs = diff(self.mfccs, axis = 0)

        self.all_times = arange(self.mfccs.shape[0]) * self.hop_s
        self.n_coeffs = self.mfccs.shape[1]

    def defineAxes(self, frames_read):
        for i in range(self.n_coeffs):
            ax = plt.axes ( [0.1, 0.75 - ((i+1) * 0.65 / self.n_coeffs),  0.8, 0.65 / self.n_coeffs], sharex = self.wave )
            ax.xaxis.set_visible(False)
            ax.set_yticks([])
            ax.set_ylabel('%d' % i)
            ax.plot(self.all_times, self.mfccs.T[i])

        # add time to the last axis, originally came after pring(npy_file_test)
        # might need to go back there
        set_xlabels_sample2time( ax, frames_read, self.samplerate)
        return ax

    def saveNPY(self):
        #begin npy saving process
        timer = time.time()
        output_filename = 'mfcc-outputs\\output-' + str(timer) + '.npy'
        save(output_filename, self.all_times) #save numpy vstack data
        remove(output_filename)

        #testing- load npy file and display in console
        set_printoptions(precision=None, threshold=sys.maxsize)#edit numpy print options
        # npy_file_test = load(output_filename)
        # print(npy_file_test)
        # print("npy loaded and printed")

    # I just don't really want all of this to be in the same class
    def showPlot(self, ax):
        #plt.ylabel('spectral descriptor value')
        ax.xaxis.set_visible(True)
        title = 'MFCC for %s' % self.source_filename
        if self.mode == "delta": title = self.mode + " " + title
        elif self.mode == "ddelta": title = "double-delta" + " " + title
        self.wave.set_title(title)
        # plt.show()


def main():
    root = "C:\\Users\\alyss\\Documents\\EDGAR\\CSC450\\data\\Audio_Speech_Actors_01-24\\"
    filesFN = getFiles(root)
    filesByFolder = filesFN.travelFiles()
    print(len(filesByFolder))
    for i in range(24):
        files = filesByFolder[i]
        # print("FILES " , files)
        for filename in files:
            if(i < 10):
                stri = "0" + str(i+1)
                # plotFN = doPlotting(root + "Actor_" + stri + "\\" + filename)
            else:
                pass
                # plotFN = doPlotting(root + "Actor_" + str(i+1) + "\\" + filename)
            # print(i)
            # frames_read = plotFN.calcMFCC()
            # plotFN.createPlot()
            # ax = plotFN.defineAxes(frames_read)
            # plotFN.saveNPY()
            # plotFN.showPlot(ax)
    print("plotted.")

if __name__ == "__main__":
    main()