'''
Stephen Carr
CSC450 SP2020 GROUP 4
Missouri State University
'''
'''
we should probably modularize this a bit
'''
import pyaudio
import wave
from pydub import AudioSegment
from pydub.playback import play
import random
import time


def get_audio():
    '''
    will begin recording when R is pressed

    custom_seconds: number of seconds to record
    num_recordings: number of recordings to be taken
    '''

    custom_seconds = input("how many seconds do you want to record? ")
    num_recordings = input("How many recordings of that length would you like? ")
    start = input("type and enter 'r' to begin recording. ")

    # if r or R typed
    if start == 'r' or 'R':

        for b in range(int(num_recordings)):
            chunk = 1024                        # Record in chunks of 1024 samples
            sample_format = pyaudio.paInt16     # 16 bits per sample
            channels = 1                        # only using one channel
            fs = 44100                          # Record at 44100 samples per second
            seconds = int(custom_seconds)

            # get the current time for use in unique filename
            unique_num = int(time.time())
            filename = 'live_audio/Output' + str(unique_num) + '.wav'

            p = pyaudio.PyAudio()  # Create an interface to PortAudio

            print('Recording')

            # open a recording stream
            stream = p.open(format=sample_format,
                            channels=channels,
                            rate=fs,
                            frames_per_buffer=chunk,
                            input=True)

            frames = []  # Initialize array to store frames


            # Store data in chunks
            for i in range(0, int(fs / chunk * seconds)):
                data = stream.read(chunk)
                frames.append(data)

            # Stop and close the stream
            stream.stop_stream()
            stream.close()

            # Terminate the PortAudio interface
            p.terminate()
            print('Finished recording ' + str(b))

            # Save the recorded data as a WAV file
            wf = wave.open(filename, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(sample_format))
            wf.setframerate(fs)
            wf.writeframes(b''.join(frames))
            wf.close()

            return filename

    else:
        print("Incorrect key. Run program again.")


if __name__ == '__main__':
    get_audio()
