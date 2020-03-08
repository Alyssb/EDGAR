#! /usr/bin/env python
'''
CSC450 SP 2020 Group 4
03/08/2020
a whole mess

currently called by get_melspectrogram.py
jk no it's not idk what uses this, it might be unused
'''

# ***************************** imports ****************************
import sys
from aubio import source, pvoc, mfcc
from numpy import vstack, zeros, diff
from numpy import save, load, set_printoptions
import time                                     # file naming scheme

# ***************************** class get_MFCC *****************************
class get_MFCC:
    def __init__(self, source_filename, samplerate, win_s, hop_s, mode):
        self.source_filename = source_filename
        self.samplerate = samplerate
        self.win_s = win_s
        self.hop_s = hop_s
        self.mode = mode

    def get_MFCC(self):
        n_filters = 40              # must be 40 for mfcc
        n_coeffs = 13

        source_filename = self.source_filename #"..\\recording_audio\\" + 

        s = source(source_filename, self.samplerate, self.hop_s)
        samplerate = s.samplerate
        p = pvoc(self.win_s, self.hop_s)
        m = mfcc(self.win_s, n_filters, n_coeffs, samplerate)

        mfccs = zeros([n_coeffs,])
        frames_read = 0
        while True:
            samples, read = s()
            spec = p(samples)
            mfcc_out = m(spec)
            mfccs = vstack((mfccs, mfcc_out))
            frames_read += read
            if read < self.hop_s: break

        # do plotting
        from numpy import arange
        from get_waveform_plot import get_waveform_plot
        from get_waveform_plot import set_xlabels_sample2time
        import matplotlib.pyplot as plt

        fig = plt.figure()
        plt.rc('lines',linewidth='.8')
        wave = plt.axes([0.1, 0.75, 0.8, 0.19])

        get_waveform_plot( source_filename, samplerate, block_size = self.hop_s, ax = wave)
        wave.xaxis.set_visible(False)
        wave.yaxis.set_visible(False)

        # compute first and second derivatives
        if self.mode in ["delta", "ddelta"]:
            mfccs = diff(mfccs, axis = 0)
        if self.mode == "ddelta":
            mfccs = diff(mfccs, axis = 0)

        all_times = arange(mfccs.shape[0]) * self.hop_s
        #plt.savefig("test-pic-output.png") #no labels but only main 'wave'
        n_coeffs = mfccs.shape[1]
        for i in range(n_coeffs):
            ax = plt.axes ( [0.1, 0.75 - ((i+1) * 0.65 / n_coeffs),  0.8, 0.65 / n_coeffs], sharex = wave )
            ax.xaxis.set_visible(False)
            ax.set_yticks([])
            ax.set_ylabel('%d' % i)
            ax.plot(all_times, mfccs.T[i])
        plt.savefig("test-pic-output.png")
        #plt.savefig("test-pic-output.png") #no file name, still has left axis label
        #begin npy saving process
        timer = time.time()
        output_filename = 'output-' + str(timer) + '.npy'
        #save(output_filename, all_times) #save numpy vstack data

        #testing- load npy file and display in console
        set_printoptions(precision=None, threshold=sys.maxsize)#edit numpy print options
        #npy_file_test = load(output_filename)
        #print(npy_file_test)
        print("npy loaded and printed")

        # add time to the last axis
        set_xlabels_sample2time( ax, frames_read, samplerate)

        #plt.ylabel('spectral descriptor value')
        ax.xaxis.set_visible(True)
        title = 'MFCC for %s' % source_filename
        if self.mode == "delta": title = self.mode + " " + title
        elif self.mode == "ddelta": title = "double-delta" + " " + title
        wave.set_title(title)

        plt.show()

def main():
    import matplotlib.pyplot as plt
    if len(sys.argv) < 2:
        print("Usage: %s <source_filename> [samplerate] [win_s] [hop_s] [mode]" % sys.argv[0])
        print("  where [mode] can be 'delta' or 'ddelta' for first and second derivatives")
        sys.exit(1)

    source_filename = sys.argv[1]

    if len(sys.argv) > 2: samplerate = int(sys.argv[2])
    else: samplerate = 0
    if len(sys.argv) > 3: win_s = int(sys.argv[3])
    else: win_s = 512
    if len(sys.argv) > 4: hop_s = int(sys.argv[4])
    else: hop_s = win_s // 4
    if len(sys.argv) > 5: mode = sys.argv[5]
    else: mode = "default"

    samplerate = 0

    get_MFCC(source_filename, samplerate, win_s, hop_s, mode)

if __name__ == '__main__':
    main()


