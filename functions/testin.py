import numpy as np
import os
import sys
import get_melspectrogram
from numpy.random import default_rng

path = "F:/project/IEMOCAP_full_release/"
FILEPATH = "F:\\project"

##audio = "test2.wav"
##
##
##mel = get_melspectrogram.melSpectrogram(audio)
##
##arrayy = mel.get_MelSpectrogram()
##
##print(arrayy.shape)
##print(arrayy.size)

print("yes doing this first")
rng = default_rng(11)
test_index = rng.choice(4530, size=450, replace=False)
labels = np.load(FILEPATH + "\\label_list_200_five.npy")
for i in range(0, 4530):
     print(i)
     spectrogram = np.load(FILEPATH + "\\mine\\model_training\metrics_200_five\\{}.npy".format(i),
                           allow_pickle=False)
     this_label = labels[i]
     if i in test_index:
         test_val = "val"
     else:
         test_val = "train"
     np.save(FILEPATH + "\\mine\\model_training\\organized_metrics\\{}\\{}\\{}.npy".format(
         test_val, this_label, i), spectrogram)
exit()
