'''
Stephen Carr
CSC450 SP2020 GROUP 4
Missouri State University
'''

# ***************************** imports *****************************
import pyaudio
import wave
from pydub import AudioSegment
from pydub.playback import play
import random
import time

# ***************************** class get_audio *****************************
class get_audio():

    def prompt_user(self):
        '''
        will begin recording when 'R' or 'r' is entered into command line
        will close if any other string is entered
        calls setup_record, whch sets up a PyAudio recording.

        custom_seconds: number of seconds to record
        num_recordings: number of recordings to be taken
        '''

        self.custom_seconds = input("how many seconds do you want to record? ")
        self.num_recordings = input("How many recordings of that length would you like? ")
        try:
            int(self.custom_seconds)
            int(self.num_recordings)
            return(self.initiate_record())
        except:
            print("please input an integer number")
            

    def initiate_record(self):
        start = input("type and enter 'r' to begin recording. ")

        filenames = []
        # if r or R typed
        if start == 'r' or start == 'R':
            for b in range(int(self.num_recordings)):
                filenames.append(self.setup_record(b))
        else:
            print("Incorrect key. Run program again.")

        return filenames

    def setup_record(self, b):
        '''
        Uses PyAudio to setup a recording.
        Calls recordAudio, which actually records
        '''
        self.chunk = 1024                        # Record in chunks of 1024 samples
        self.sample_format = pyaudio.paInt16     # 16 bits per sample
        self.channels = 1                        # only using one channel
        self.fs = 44100                          # Record at 44100 samples per second

        # get the current time for use in unique filename
        self.unique_num = int(time.time())
        self.filename = 'live_audio/Output' + str(self.unique_num) + '.wav'

        self.p = pyaudio.PyAudio()               # Create an interface to PortAudio


        # open a recording stream
        self.stream = self.p.open(format=self.sample_format,
                            channels=self.channels,
                            rate=self.fs,
                            frames_per_buffer=self.chunk,
                            input=True)

        self.frames = []  # Initialize array to store frames
        
        print('Recording')
        return(self.record_audio(b))
    

    def record_audio(self, b):
        '''
        takes recordings as specified by the user
        calls save_file, which saves the audio data as a .wav file
        '''
        # Store data in chunks
        for i in range(0, int(self.fs / self.chunk * int(self.custom_seconds))):
            data = self.stream.read(self.chunk)
            self.frames.append(data)

        # Stop and close the stream
        self.stream.stop_stream()
        self.stream.close()

        # Terminate the PortAudio interface
        self.p.terminate()

        print('Finished recording ' + str(b))
        return(self.save_file(b))

    def save_file(self, b):
        '''
        saves the audio data as a .wav file
        '''
        # Save the recorded data as a WAV file
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        
        print('file ' + self.filename + ' saved.')
        return self.filename


# ***************************** main *****************************
if __name__ == '__main__':
    recording = get_audio()
    recording.prompt_user()
