#! /usr/bin/env python
'''
CSC450 SP2020 Group 4
Missouri State University
Detects and creates a recording if the decibel level of 60dB is exceeded
Exits if 'Q' is pressed while listening
MUST be run from EDGAR directory
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

# ********************************** global variables **********************************
# for recording
CHUNK = 1024                    # record in chunks of 1024 samples
FORMAT = pyaudio.paInt16        # 16 bits per sample
CHANNELS = 1                    # only using one channel
FS = 44100                      # record at 44100 samples per second

# for RMS calculation
SHORT_NORMALIZE = (1.0/32768.0) # factor for normalizing samples in a chunk
SWIDTH = 2                      # factor for shorts per frame (?)
THRESHOLD = 150                 # sets threshold in RMS: 317rms is equal to 60dB

# for demo
FILES = []
# ********************************** class do_record **********************************
class do_record():
    def __init__(self):
        print("EDGAR has started.")

    '''
    function: setup_record
    sets up a fresh recording stream
    prints system is ready
    must be executed before check_dB
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
        print('EDGAR is ready')  

    '''
    function: check_dB
    if current decibel level above THRESHOLD, make a recording
    if key 'Q' is pressed, exit
    class variables:
        unique_num (int):   current time in seconds
        filename (string):  name of file to store recording in
    
    local variables:
        input (frame):      the current audio chunk
        rms_val (float):    the rms value of input
    '''       
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
                    self.record_3sec()
                    
                    print("preparing to resume listening. press \'Q\' to quit")
                    self.setup_record()     # sets up a new recording and clears self.frames
        return FILES    # for demo only
    
    '''
    function: rms
    calculates RMS (root-mean-square) of current frame
    parameters:
        frame (frame): the current chunk
    
    returns:
        rms (float):    calculated RMS value for frame
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

        return rms * 1000

    '''
    function: record_3sec
    appends all frames to frames for 3 seconds
    calls write_to_file()
    local variables:
        data (frame):   the value of the current chunk
    '''
    def record_3sec(self):
        while(time.time() < (self.unique_num + 4)):
            data = self.stream.read(CHUNK)
            self.frames.append(data)
        self.write_to_file()

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
        # I really don't know what the b on this line does
        wf.writeframes(b''.join(self.frames))

        wf.close()
        self.p.terminate()
        print(self.filename + " saved\n")
        FILES.append(self.filename) # for demo only


# ********************************** main **********************************
def main():
    # executes the do_record class
    record_instance = do_record()
    record_instance.setup_record()
    record_instance.check_dB()

if __name__ == "__main__":
    main()