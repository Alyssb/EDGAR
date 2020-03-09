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
'''
import sys
from os.path import exists

# adds string to path for the running of this file
sys.path.insert(1, "C:\\Users\\alyss\\Documents\\EDGAR\\")

import get_melspectrogram

filename = "testing\\withSpeech3sec.wav"

def default_test():
    melspec = get_melspectrogram.melSpectrogram(filename)
    melspec.get_MelSpectrogram()
    print("it works")

def test_displaySpectrogram():
    print("not yet implemented")

def test_deleteFile():
    print("not yet implemented")

def test_saveFile():
    print("not yet implemented")

def test_arrayShape():
    # will not pass if padToLongest does not work
    print("not yet implemented")

def test_arraySize():
    # will not pass if padToLongest does not work
    print("not yet implemented")

def main():
    default_test()

if __name__ == '__main__':
    main()