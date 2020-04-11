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

def main():
    record_instance = do_record()
    record_instance.setup_record()
    record_instance.record_3sec()
    record_instance.write_to_file()

if __name__ == "__main__":
    main()