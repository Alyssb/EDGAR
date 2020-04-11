'''
CSC450 Team 4
Detects the decibel level and activates EDGAR if 60dB is exceeded
'''
# ***************************** imports *****************************
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

# ***************************** global variables *****************************
# for recording
CHUNK = 1024                    # record in chunks of 1024 samples
FORMAT = pyaudio.paInt16        # 16 bits per sample
CHANNELS = 1                    # only using one channel
FS = 44100                      # record at 44100 samples per second

# for RMS calculation
SHORT_NORMALIZE = (1.0/32768.0) # factor for normalizing samples in a chunk
SWIDTH = 2                      # factor for shorts per frame (?)
THRESHOLD = 150                 # sets threshold in RMS: 317rms is equal to 60dB

# ***************************** class do_record *****************************
class do_record():
    def __init__(self):
        print("EDGAR has started.")

    # sets up a fresh recording
    def setup_record(self):
        '''
        self.frames[]:      array for storing frames during recording

        '''
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
            self.frames.append(data)
        # self.write_to_file()

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


# ***************************** main *****************************
def main():
    record_instance = do_record()
    record_instance.setup_record()
    record_instance.check_dB()

if __name__ == "__main__":
    main()