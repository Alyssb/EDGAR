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
import keyboard

import pyaudio
from pydub import AudioSegment
from pydub.playback import play

# global variables
SHORT_NORMALIZE = (1.0/32768.0)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
FS = 44100
SWIDTH = 2

# sets threshold in RMS: 317rms is equal to 60dB
THRESHOLD = 317

class do_record():
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
                    
    def check_dB(self):
        print('listening... press \'Q\' to quit')
        while True:
            if keyboard.is_pressed('q'):
                print('EDGAR has exited successfully')
                break
            else:
                input = self.stream.read(CHUNK) # input is a frame (chunk)
                rms_val = self.rms(input)
                if rms_val > THRESHOLD:
                    self.unique_num = int(time.time())
                    self.final_time = self.unique_num + 3
                    self.record_3sec()
                    self.setup_record()

    # calculates RMS of current frame
    def rms(self, frame):
        count = len(frame) / SWIDTH
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)
        sum_squares = 0.0

        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000

    def record_3sec(self):
        while(time.time() < self.final_time):
            data = self.stream.read(CHUNK)
            self.rec.append(data)
        self.write_to_file()

    def write_to_file(self):
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(FS)
        # I really don't know what the b on this line does
        wf.writeframes(b''.join(self.rec))

        wf.close()
        self.p.terminate()
        print(self.filename + " saved\n")

def main():
    print("EDGAR has started.")
    record_instance = do_record()
    record_instance.setup_record()
    record_instance.check_dB()

if __name__ == "__main__":
    main()