'''
CSC450 SP2020 Group 4
Missouri State University

MUST be run from EDGAR directory.
'''
'''
test cases:
    displaySpectrogram works
    saveFile works
    deleteFile works
    runtime

from test suite
    FR.02-TC.01     system should create lms from wav files
    FR.02-TC0.2     system should store LMS created from WAV files
    NFR.03-TC.01    EDGAR should create lms in less than 1 second
    NFR.04-TC.01    EDGAR shall store lms on host machine
    DC.02-TC.01     system must delete audio files after LMS is generated
    LDR.01-TC.01    system should store LMS from WAV files
'''
import time
import sys
from os.path import exists
from os import remove
import numpy.testing as npy_test

# for copying files
import shutil

# for reading output
import subprocess

# adds string to path for the running of this file
# HARDCODED change for your directory
sys.path.append('./functions/')

import get_melspectrogram

filename = "./testing/testaudio.wav"


def make_melspec(audio=filename):
    melspec = get_melspectrogram.melSpectrogram(audio)
    melspec.get_MelSpectrogram()
    melspec.saveSpectrogram()
    return (melspec)


def test_deleteFile_exists():
    print("\nRunning test_deleteFile_exists")
    # create a file that is a copy of filename
    # and then delete it with get_melspectrogram.py
    tempname = "./testing/temp.wav"
    shutil.copyfile(filename, tempname)
    melspec = make_melspec(tempname)
    melspec.deleteFile()
    if (exists(tempname)):
        print("\tdeleteFile_exits failed")
    else:
        print("\tdeleteFile_exists passed")


def test_deleteFile_notExists():
    print("\nRunning test_deleteFile_notExists\n")
    tempname = "./testing/temp.wav"
    shutil.copyfile(filename, tempname)
    melspec = make_melspec(tempname)
    remove(tempname)
    melspec.deleteFile()
    print("\nif output was:\n\tFILE ERROR: cannot remove file\n\tdeleteFile_notExists passed")


def test_saveFile():
    print("\nRunning test_saveFile\n")
    melspec = make_melspec(filename)
    melspec.saveFile()
    tempname = melspec.filename
    if (exists(tempname + ".npy")):
        print("\tsaveFile passed")
    else:
        print("\tsaveFile failed")


def test_runtime():
    # executes every function normally executed by EDGAR
    print("\nRunning test_runtime\n")
    current_time = time.time()
    melspec = make_melspec()
    melspec.saveFile()
    melspec.source_filename = "./testing/temp.wav"
    melspec.deleteFile()
    print("TIME ELAPSED: ", round(time.time() - current_time, 3), " seconds")


def test_displaySpectrogram():
    # at the end because spectrogram has to be manually exited
    print("\nRunning test_displaySpectrogram")
    melspec = make_melspec()
    melspec.displaySpectrogram()
    print("\tdisplaySpectrogram passed")


def main():
    test_deleteFile_exists()
    test_deleteFile_notExists()
    test_saveFile()
    test_runtime()
    # test_displaySpectrogram()


if __name__ == '__main__':
    main()
