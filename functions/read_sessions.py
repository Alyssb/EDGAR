##This code is meant to be ran inside the folder of the iemocap database, and is kept inside the training_audio folder for the time being as this version will simply read the file names and thier labels but will not run the metrics at this time
##Also this will not be a part of the 'live' edgar and only used likely once to create the final model

import numpy as np
import os
import sys
import get_melspectrogram

emotions = []
file_names = []

path = "F:/project/IEMOCAP_full_release/"
session_list = ["Session1", "Session2", "Session3", "Session4", "Session5"]
audio_path = "/sentences/wav/"
label_path = "/dialog/EmoEvaluation/" #Categorical/
session = 1
counter = 0

anger = 0
sad = 0
fear = 0
happy = 0
frustrated = 0
none = 0
other = 0
excited = 0
surprised = 0
disgusted = 0
neutral = 0


for session in session_list: #run through all 5 sessions
    wav_p = path + session + audio_path #path to audio .wav file
    label_p = path + session + label_path #path to cat labels

    wav_folder = os.listdir(wav_p)

    d_list = []
    d_list = [folders for folders in sorted(os.listdir(wav_p))]

    for i in d_list:
        individual_audio_path = wav_p + i + "/"
        audio_folder = os.listdir(individual_audio_path)
        wav_list = []
        wav_list = [files for files in sorted((audio_folder))]   
        
        for j in wav_list:
            individual_class = j.replace(".wav", "")


            classify_list = label_p + i + ".txt"
            with open(classify_list) as f:
                for number, line in enumerate(f, 1):
                    if individual_class in line:
                        temp = line.split("\t")
                        temp2 = temp.index(individual_class)
                        majority = temp[temp2+1]
                        if(majority != "xxx" and majority !="fru" and majority !="oth" and majority !="exc" and majority !="sur" and majority !="dis"):
                            emotions.append(majority)
                            if j.endswith(".wav"):
                                dummy = individual_audio_path + j
                                file_names.append(dummy)
                                metric = get_melspectrogram.melSpectrogram(dummy)
                                metric = metric.get_MelSpectrogram()
                                #metric = get_MelSpectrogram(dummy)
                                np.save("F:/project/metrics_200_five/"+str(counter), metric)
                                counter = counter + 1
                            if(majority == 'neu'): neutral=neutral+1
                            elif(majority == 'sad'): sad=sad+1
                            elif(majority == 'ang'): anger=anger+1
                            elif(majority == 'fea'): fear=fear+1
                            elif(majority == 'hap'): happy=happy+1
                            elif(majority == 'fru'): frustrated=frustrated+1
                            elif(majority == 'xxx'): none=none+1
                            elif(majority == 'oth'): other=other+1
                            elif(majority == 'exc'): excited=excited+1
                            elif(majority == 'sur'): surprised=surprised+1
                            elif(majority == 'dis'): disgusted=disgusted+1
                            else:print("uncaught...")
                
                    
print(set(emotions))

print("anger: ",anger,"sad: ",sad,"fear: ",fear,"happy: ",happy,"frustrated: ",frustrated,"none: ",none,"other: ",other,"excited: ",excited,"surprised: ",surprised,"disgusted: ",disgusted,"neutral: ",neutral)
print("there are this many .wavs: ",counter)

file_np = np.array(file_names)
file2_np = np.array(emotions)
np.save("file_list_200_five", file_np)
np.save("label_list_200_five", file2_np)


print(file_names[0], emotions[0])
#print(np.load("F:/project/metrics/0.npy"))
