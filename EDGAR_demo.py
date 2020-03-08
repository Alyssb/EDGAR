'''
CSC450 SP2020 Group 4

'''
import sys
sys.path.append('./CSC450/')

from get_mfcc import get_MFCC
from get_spectrogram import get_spectrogram
from get_melspectrogram import get_MelSpectrogram

sys.path.append('./recording_audio/')
from get_audio import get_audio

from os import remove
from os.path import exists

recording = get_audio()
input_name = recording.prompt_user()
print("Audio file: " + input_name[0] + " created")
#get_MFCC(input_name, 0, 512, 128, "delta")
#get_spectrogram(input_name, 0)
melSpectrogram_nparray = get_MelSpectrogram(input_name[0])
print(melSpectrogram_nparray)
print("shape of array(should be 40, 1067, 3): ", melSpectrogram_nparray.shape)
print("size of array(should be 3): ", melSpectrogram_nparray.ndim)

if(exists(input_name[0])):
    remove(input_name[0])
    print("file " + str(input_name[0]) + " deleted")
else:
    print("file error")

