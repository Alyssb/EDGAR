'''
CSC450 SP2020 Group 4
03/08/2020
'''
'''
test cases:
    That it works
    Shape of Array
    Size of Array
    Array is saved 
    umm idk what else
'''
import sys

# adds string to path for the running of this file
sys.path.insert(1, "C:\\Users\\alyss\\Documents\\EDGAR\\")

import get_melspectrogram

filename = "testing\\withSpeech3sec.wav"

def default_test():
    melspec = get_melspectrogram.melSpectrogram(filename)
    melspec.get_MelSpectrogram()
    print("bruh moment.")

def main():
    
    default_test()

if __name__ == '__main__':
    main()