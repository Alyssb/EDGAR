'''
CSC450 SP2020 Group 4
03/08/2020
Currently configured for demo 2 on 03/12/2020
MUST be run from EDGAR directory.
'''

# import path to file directory and change it to where our inputs are located
import sys
sys.path.append('./CSC450/recording_audio/')
sys.path.insert(1, './unused/')

# ***************************** imports *****************************
# import modules we have created
#from get_mfcc import get_MFCC
#from get_spectrogram import get_spectrogram
from get_melspectrogram import melSpectrogram
#from get_audio import get_audio
#from run_model import runModel
from output import response
from get_response import get_response
from run_torch_model import loadModel
from decibel_detection import do_record, main
import time

# ***************************** demo *****************************
def runDemo():

    #recording = get_audio()                 # creates an instance of get_audio.py
    #input_names = recording.prompt_user()   # creates .wav files and returns an array of names

    # recording = do_record()
    # recording.setup_record()
    # input_names = recording.check_dB()
    since = time.time()
    
    #get_MFCC(input_names, 0, 512, 128, "delta")
    #get_spectrogram(input_names, 0)
    
    # for i in range(len(input_names)):
    #     # print("Audio file: " + input_names[i] + " created")     # prints after the files are created
        
    #     # mSpec = melSpectrogram(input_names[i])
    #     mSpec = melSpectrogram("live_audio\\1587785357.wav")
    #     mSpec.get_MelSpectrogram()     # creates a mel spectrogram for a given file
    #     result = loadModel(mSpec.S_dB)
    #     response(result)
    #     image_out = get_response(result)
    #     image_out.get_image()

        
    #     mSpec.deleteFile()  # deletes original audio file to protect privacy
    #     mSpec.saveFile()    # Saves 3D numpy output array to a file
    mSpec = melSpectrogram("live_audio\\1587785357.wav")
    mSpec.get_MelSpectrogram()     # creates a mel spectrogram for a given file
    result = loadModel(mSpec.S_dB)
    response(result)
    image_out = get_response(result)
    image_out.get_image()
    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(
    time_elapsed // 60, time_elapsed % 60))

# ***************************** main *****************************
def main():
    
    runDemo()


if __name__ == "__main__":
    main()
