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

# global variables (caps)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
FS = 44100

class do_record:

    def __init__(self):
        self.unique_num = int(time.time())
        self.final_time = self.unique_num + 3
        self.rec = []

    def setup_record(self):
        print("current time ", time.time())
        print(self.final_time)
        self.filename = 'live_audio/Output' + str(self.unique_num) + '.wav'

        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(format=FORMAT, 
                    channels=CHANNELS,
                    rate=FS,
                    frames_per_buffer=CHUNK,
                    input=True,
                    output=True)

    def record_3sec(self):
        while(time.time() < self.final_time):
            data = self.stream.read(CHUNK)
            self.rec.append(data)

    def write_to_file(self):
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(FS)
        # b = ''
        # I really don't know what the b on this line does
        wf.writeframes(b''.join(self.rec))

        wf.close()
        self.p.terminate()
        print(self.filename + " saved\n")

    # may not need this in class format
    def update_loop(self):
        self.frames = []
        self.unique_num = int(time.time())
        self.final_time += 3

# while time.time() < tempnum: # just to run it 3 times, dummy
#     print("current time ", time.time())
#     print(final_time)
#     filename = 'live_audio/Output' + str(unique_num) + '.wav'

#     p = pyaudio.PyAudio()

#     stream = p.open(format=sample_format, 
#                     channels=channels,
#                     rate=fs,
#                     frames_per_buffer=chunk,
#                     input=True)

#     while time.time() < final_time:
#         data = stream.read(chunk)
#         frames.append(data)

#     wf = wave.open(filename, 'wb')
#     wf.setnchannels(channels)
#     wf.setsampwidth(p.get_sample_size(sample_format))
#     wf.setframerate(fs)
#     b = ''
#     wf.writeframes(b''.join(frames))
#     #print(b''.join(frames))
#     wf.close()
#     p.terminate()
#     print(filename + " saved\n")

#     frames = []
#     unique_num = int(time.time())
#     final_time += 3


def main():
    record_instance = do_record()
    record_instance.setup_record()
    record_instance.record_3sec()
    record_instance.write_to_file()

if __name__ == "__main__":
    main()