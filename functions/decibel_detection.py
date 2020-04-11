'''
CSC450 Team 4
Detects the decibel level and activates EDGAR if 60dB is exceeded

right now im just using this for getting audio continuously
Combining it with get_speech.py, by stephen
'''

import math
import struct
import wave
import os
import time

import pyaudio
from pydub import AudioSegment
from pydub.playback import play

temp = True
chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100

unique_num = int(time.time())
tempnum = unique_num + 9
final_time = unique_num + 3
frames = []

class doRecord:

    def __init__(self):
        self.temp = True

def update_loop(final_time):
    frames = []
    unique_num = int(time.time())
    final_time += 3


while time.time() < tempnum:
    print("current time ", time.time())
    print(final_time)
    filename = 'live_audio/Output' + str(unique_num) + '.wav'

    p = pyaudio.PyAudio()

    stream = p.open(format=sample_format, 
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    while time.time() < final_time:
        data = stream.read(chunk)
        frames.append(data)

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    b = ''
    wf.writeframes(b''.join(frames))
    #print(b''.join(frames))
    wf.close()
    p.terminate()
    print(filename + " saved\n")

    frames = []
    unique_num = int(time.time())
    final_time += 3

    temp = False

# def main():
#     print("hello world")

# if __name__ == "__main__":
#     main()