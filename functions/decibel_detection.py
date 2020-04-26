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

# import path to file directory and change it to where our inputs are located
import sys
sys.path.append('./CSC450/recording_audio/')
sys.path.insert(1, './unused/')


# ********************************** imports **********************************
# general imports
import time
from struct import unpack
from math import pow
from keyboard import is_pressed

# audio imports
import wave
import pyaudio
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr

# function imports
from get_melspectrogram import melSpectrogram
from run_torch_model import loadModel
from output import response
from get_response import get_response

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
FILENAME = ""
FILES = []
# ********************************** class do_record **********************************
class do_record():
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
    function: check_dB
    checks every chunk until 'Q' is pressed
    calls self.rms()
    if key 'Q' is pressed, exit
    local variables:
        input (frame):      the current audio chunk
    '''
    def check_dB(self):
        print("Listening... press \'Q\' to quit.")
        while True:
            if is_pressed('q'):
                print("\nEDGAR has exited successfully.")
                break
            else:
                input = self.stream.read(CHUNK, exception_on_overflow = False) # input is a frame (chunk)
                self.rms(input)
        return FILES    # for demo only


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
            self.get_audio_for_check()


    '''
    function: get_audio_for_check
    records 1 second of audio to check if it's speech
    calls check_if_speech()
    class variables:
        r (Recognizer Object):      creates an instance of a Recognizer object
        audio (AudioData Object):   0.99 second AudioData object
    local variables:
        data (frame):   the value of the current chunk
    '''   
    def get_audio_for_check(self):
        self.r = sr.Recognizer()
        with sr.Microphone() as source:                                 # use the default microphone as the audio source
            self.audio = self.r.listen(source, phrase_time_limit=0.99)  # records for 0.99 seconds to check if audio is speech
        self.check_if_speech()


    '''
    function: check_if_speech
    uses speech_recognition library to determine if audio is speech
    if speech is detected, calls record_3sec()
    if speech is not detected, calls setup_record()
    '''
    def check_if_speech(self):
        try:
            if len(self.r.recognize_google(self.audio)) > 0:
                print("Speech has been detected.")
                self.record_3sec()
        except sr.UnknownValueError:
            print("Could not understand. Speak again or press 'Q' to quit.")
            self.setup_record()


    '''
    function: record_3sec
    appends all frames to self.frames for 3 seconds
    calls write_to_file()
    class variables:
        unique_num (int):   current time in seconds
        filename (string):  name of file to store recording in
    local variables:
        data (frame):   the value of the current chunk
    '''
    def record_3sec(self):
        self.unique_num = int(time.time())
        FILENAME = "live_audio/" + str(self.unique_num) + ".wav"

        temp_time = time.time()
        while(time.time() < (temp_time + 3)):
            data = self.stream.read(CHUNK, exception_on_overflow = False)
            self.frames.append(data)
        self.write_to_file()
        self.setup_record()


    '''
    function: write_to_file
    saves recorded audio as a WAV file
    local variables:
        wf (wave object):   filename opened as an empty wave object
    '''
    def write_to_file(self):
        wf = wave.open(FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(FS)
        wf.writeframes(b''.join(self.frames))

        wf.close()
        self.p.terminate()
        print(FILENAME + " saved.\n")
        FILES.append(FILENAME) # for demo only

class next_steps():
    def __init__(self, mSpec):
        print("creating spectrogram")
        self.mSpec = mSpec

    def run_get_melSpectrogram(self):
        self.mSpec.get_MelSpectrogram()
        mSpec.saveSpectrogram()

# ********************************** main **********************************
def main():
    # executes the do_record class
    record_instance = do_record()
    record_instance.setup_record()
    record_instance.check_dB()

    mSpec = melSpectrogram(FILENAME)
    continue_EDGAR = next_steps(mSpec)

if __name__ == "__main__":
    main()