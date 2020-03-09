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

# for copying files
import shutil

# adds string to path for the running of this file
# HARDCODED change for your directory
sys.path.insert(1, "C:\\Users\\alyss\\Documents\\EDGAR\\")

import get_melspectrogram

filename = "testing\\withSpeech3sec.wav"

def make_melspec(audio = filename):
    melspec = get_melspectrogram.melSpectrogram(audio)
    return(melspec)

def test_deleteFile_exists():
    print("\nRunning test_deleteFile_exists\n")
    # create a file that is a copy of filename
    # and then delete it with get_melspectrogram.py
    tempname = "testing\\temp.wav"
    shutil.copyfile(filename, tempname)
    melspec = make_melspec(tempname)
    melspec.deleteFile()
    if(exists(tempname)):
        print("did not delete file")
    else:
        print("test_deleteFile_exists passed")

def test_deleteFile_notExists():
    print("not yet implemented")

def test_saveFile():
    print("not yet implemented")

def test_arrayShape():
    # will not pass if padToLongest does not work
    print("not yet implemented")

def test_arraySize():
    # will not pass if padToLongest does not work
    print("not yet implemented")

def test_displaySpectrogram():
    melspec = make_melspec()
    melspec.get_MelSpectrogram()
    melspec.displaySpectrogram()

def main():
    test_deleteFile_exists()

if __name__ == '__main__':
    main()