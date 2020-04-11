'''
CSC450 Team 4
Detects the decibel level and activates EDGAR if 60dB is exceeded
'''

import wave
import time
from struct import unpack
from math import pow
from keyboard import is_pressed
# import os     # os.getcwd() to get current directory

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
THRESHOLD = 150 # turned it down b/c roommate is asleep

class do_record():
    def setup_record(self):
        self.rec = []

        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(format=FORMAT, 
                    channels=CHANNELS,
                    rate=FS,
                    frames_per_buffer=CHUNK,
                    input=True,
                    output=True)  
        print('EDGAR is ready')  
                    
    def check_dB(self):
        print('listening... press \'Q\' to quit')
        while True:
            if is_pressed('q'):
                print('EDGAR has exited successfully')
                break
            else:
                input = self.stream.read(CHUNK) # input is a frame (chunk)
                rms_val = self.rms(input)

                if rms_val > THRESHOLD:
                    print("sound detected. initiating record at time", time.time(), "\n")
                    self.unique_num = int(time.time())
                    self.filename = 'live_audio/Output' + str(self.unique_num) + '.wav'
                    self.final_time = self.unique_num + 3
                    self.record_3sec()
                    print("preparing to resume listening. press \'Q\' to quit")
                    self.setup_record()

    # calculates RMS of current frame
    def rms(self, frame):
        count = len(frame) / SWIDTH
        format = "%dh" % (count)
        shorts = unpack(format, frame)
        sum_squares = 0.0

        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = pow(sum_squares / count, 0.5)

        return rms * 1000

    def record_3sec(self):
        while(time.time() < self.final_time):
            data = self.stream.read(CHUNK)
            self.rec.append(data)
        # self.write_to_file()

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