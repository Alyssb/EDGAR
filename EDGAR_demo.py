'''
CSC450 SP2020 Group 4
03/08/2020

Currently configured for demo 2 on 03/12/2020

MUST be run from EDGAR directory.
'''

# import path to file directory and change it to where out inputs are located
import sys
sys.path.append('./CSC450/recording_audio/')

# ***************************** imports *****************************
# import modules we have created
from get_mfcc import get_MFCC
from get_spectrogram import get_spectrogram
from get_melspectrogram import melSpectrogram
from get_audio import get_audio

# ***************************** demo *****************************
def runDemo():

    recording = get_audio()                 # creates an instance of get_audio.py
    input_names = recording.prompt_user()    # creates .wav files and returns an array of names
    
    #get_MFCC(input_names, 0, 512, 128, "delta")
    #get_spectrogram(input_names, 0)
    
    for i in range(len(input_names)):
        print("Audio file: " + input_names[i] + " created")         # prints after the files are created
        
        mSpec = melSpectrogram(input_names[i])
        melSpectrogram_nparray = mSpec.get_MelSpectrogram() # creates a mel spectrogram for a given file
        print(melSpectrogram_nparray)                               # prints the array
        print("shape of array (should be 40, 1067, 3): ", 
                melSpectrogram_nparray.shape)
        print("size of array (should be 3): ", melSpectrogram_nparray.ndim)
        mSpec.deleteFile()  # deletes original audio file to protect privacy


# ***************************** main *****************************
def main():
    runDemo()

if __name__ == "__main__":
    main()

