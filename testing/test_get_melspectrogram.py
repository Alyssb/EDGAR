'''
CSC450 SP2020 Group 4
03/08/2020

MUST be run from EDGAR directory.
'''
'''
test cases:
    displaySpectrogram works
    saveFile works
    deleteFile works
    Shape of Array
    Size of Array

from test suite
    FR.02-TC.01     system should create lms from wav files
    FR.02-TC0.2     system should store LMS created from WAV files
    NFR.03-TC.01    EDGAR should create lms in less than 1 second
    NFR.04-TC.01    EDGAR shall store lms on host machine
    DC.02-TC.01     system must delete audio files after LMS is generated
    LDR.01-TC.01    system should store LMS from WAV files
'''
import sys
from os.path import exists
import numpy.testing as npy_test

# for copying files
import shutil

# for reading output
import subprocess

# adds string to path for the running of this file
# HARDCODED change for your directory
sys.path.insert(1, "C:\\Users\\alyss\\Documents\\EDGAR\\functions\\")

import get_melspectrogram

filename = "testing/withSpeech3Sec.wav"


def make_melspec(audio=filename):
    melspec = get_melspectrogram.melSpectrogram(audio)
    return (melspec)


def test_deleteFile_exists():
    print("\nRunning test_deleteFile_exists")
    # create a file that is a copy of filename
    # and then delete it with get_melspectrogram.py
    tempname = "testing\\temp.wav"
    shutil.copyfile(filename, tempname)
    melspec = make_melspec(tempname)
    melspec.deleteFile()
    if (exists(tempname)):
        print("\tdeleteFile_exits failed")
    else:
        print("\tdeleteFile_exists passed")


def test_deleteFile_notExists():
    print("\nRunning test_deleteFile_notExists\n")
    tempname = "testing\\temp.wav"
    melspec = make_melspec(tempname)
    melspec.deleteFile()
    print("\nif output was:\n\tFILE ERROR: cannot remove file\n\tdeleteFile_notExists passed")

def test_saveFile():
    print("\nRunning test_saveFile\n")
    melspec = make_melspec(filename)
    melspec.get_MelSpectrogram()
    melspec.saveFile()
    tempname = melspec.filename
    if (exists(tempname + ".npy")):
        print("\tsaveFile passed")
    else:
        print("\tsaveFile failed")

def test_arrayShape():
    # will not pass if padToLongest does not work
    print("\nRunning test_arrayShape")
    melspec = make_melspec()
    npArray = melspec.get_MelSpectrogram()
    temp = (40, 1067, 3)
    if npArray.shape == temp:
        print("\tarrayShape passed")


def test_arraySize():
    # will not pass if padToLongest does not work
    print("\nRunning test_arraySize")
    melspec = make_melspec()
    npArray = melspec.get_MelSpectrogram()
    temp = (40, 1067, 3)
    if npArray.ndim == len(temp):
        print("\tarraySize passed")


def test_displaySpectrogram():
    # at the end because spectrogram has to be manually exited
    print("\nRunning test_displaySpectrogram")
    melspec = make_melspec()
    melspec.get_MelSpectrogram()
    melspec.displaySpectrogram()
    print("\tdisplaySpectrogram passed")


def main():
    test_deleteFile_exists()
    test_deleteFile_notExists()
    test_saveFile()
    test_arrayShape()
    test_arraySize()
    # test_displaySpectrogram()


if __name__ == '__main__':
    main()
