#! /usr/bin/env python
'''
CSC450 SP2020 Group 4
Missouri State University

Passively listens to external audio
If 60dB is exceeded,
    Check if input is speech data
    Record for 3 seconds if speech data is detected
    Save recording as a WAV file
'''

import sys
sys.path.append('./CSC450/recording_audio/')

# ********************************** imports **********************************
# general imports
from check_and_record import check_and_record
from keyboard import is_pressed
import time

# audio imports
import wave
import pyaudio
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr

# ********************************** global variables **********************************
# for recording
CHUNK = 1024                    # record in chunks of 1024 samples
FORMAT = pyaudio.paInt16        # 16 bits per sample
CHANNELS = 1                    # only using one channel
FS = 44100                      # record at 44100 samples per second

# for RMS calculation
SHORT_NORMALIZE = (1.0/32768.0) # factor for normalizing samples in a chunk
SWIDTH = 2                      # factor for shorts per frame
THRESHOLD = 100                 # sets threshold in RMS: 317rms is equal to 60dB

# for demo
FILES = []
# ********************************** class do_record **********************************
class EDGAR():
    ''' init function '''
    def __init__(self):
        print("EDGAR has started.")
    

    '''
    function: setup_record
    sets up a fresh recording stream
    MUST be executed before check_dB
    class variables:
        frames (array):             array for storing frames during recording
        p (PyAudio):                instance of PyAudio
        stream (PyAudio stream):    PyAudio stream created with global variables
    '''
    def setup_record(self):
        self.frames = []
        self.p = pyaudio.PyAudio()

        # sets up a recording stream
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=FS,
                                  frames_per_buffer=CHUNK,
                                  input=True,
                                  output=True)
        print("EDGAR is ready.")
    
    '''
    function: run_EDGAR
    checks every chunk until 'Q' is pressed
    calls check_and_record.rms
    if key 'Q' is pressed, exit
    local variables:
        input (frame):      the current audio chunk
    '''
    def run_EDGAR(self):
        self.setup_record()
        print("Listening... press \'Q\' to quit.")
        while True:
            if is_pressed('q'):
                print("\nEDGAR has exited successfully.")
                break
            else:
                # time.sleep(0.1)
                input = self.stream.read(CHUNK, exception_on_overflow = False) # input is a frame (chunk)
                self.rms(input)
    
    '''
    function: rms
    calculates RMS (root-mean-square) of current frame
    calls check_rms()
    parameters:
        frame (frame): the current chunk
    local variables:
        count (float):          length of frame divided by short width (SWIDTH)
        format (string):        format string for frame (short int)
        shorts (tuple):         tuple that contains short ints representing frame
        sample (tuple element): an iteration through shorts
        n (float):              sample times short int normalization factor (SHORT_NORMALIZE)
        sum_squares (float):    sum of n * n for for shorts
        rms (float):            represents calculated RMS for frame
    '''
    def rms(self, frame):
        count = len(frame) / SWIDTH
        format = "%dh" % (count)
        shorts = unpack(format, frame)
        sum_squares = 0.0

        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = pow(sum_squares / count, 0.5)
        self.check_rms(rms)

    '''
    function: check_rms
    checks if rms is greater than THRESHOLD
    if THRESHOLD is exceeded, calls get_audio_for_check()
    parameters:
        rms (float):    calculated RMS for current
    '''
    def check_rms(self, rms):
        if (rms * 1000) > THRESHOLD:
            print("Threshold exceeded.")
            record_fn = check_and_record()
            record_fn.get_audio_for_check()



# ********************************** main **********************************
def main():
    print("main function of decibel_detection.py")
    # executes EDGAR
    EDGAR_instance = EDGAR()
    EDGAR_instance.run_EDGAR()

if __name__ == "__main__":
    main()