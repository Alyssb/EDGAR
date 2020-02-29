import sys
sys.path.append('./CSC450/')
from get_mfcc import get_MFCC
from get_spectrogram import get_spectrogram
from get_melspectrogram import get_MelSpectrogram

sys.path.append('./recording_audio/')
from get_audio import get_audio

from os import remove
from os.path import exists

input_name = get_audio()
print("Audio file: " + input_name + " created")
#get_MFCC(input_name, 0, 512, 128, "delta")
#get_spectrogram(input_name, 0)
melSpectrogram_nparray = get_MelSpectrogram(input_name)
print("size of array: ", melSpectrogram_nparray.shape)

if(exists(input_name)):
    remove(input_name)
    print("file deleted")
else:
    print("file error")

