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
class check_and_record():

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
        self.setup_record()
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
                self.setup_record()
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
        self.filename = "live_audio/" + str(self.unique_num) + ".wav"

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
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(FS)
        wf.writeframes(b''.join(self.frames))

        wf.close()
        self.p.terminate()
        print(self.filename + " saved.\n")
        FILES.append(self.filename) # for demo only


# ********************************** main **********************************
def main():
    # executes the do_record class
    record_instance = do_record()
    record_instance.setup_record()
    record_instance.check_dB()

if __name__ == "__main__":
    main()