'''
CSC450 Team 4
Detects the decibel level and activates EDGAR if 60dB is exceeded

right now im just using this for getting audio continuously
'''

import pyaudio
import wave
from pydub import AudioSegment
from pydub.playback import play
import time

temp = True
chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100
frames = []

while temp:
    unique_num = int(time.time())
    final_time = unique_num + 3
    tempnum = unique_num + 9
    print(unique_num)
    print(final_time)

    filename = 'live_audio/Output' + str(unique_num) + '.wav'

    p = pyaudio.PyAudio()

    stream = p.open(format=sample_format, 
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)



    data = stream.read(chunk)
    frames.append(data)

    print(time.time())
    if final_time < time.time():
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        b = 1
        wf.writeframes(b''.join(frames))
        #print(b''.join(frames))
        wf.close()
        p.terminate()
        print(filename + " saved")
        temp = False

# def main():
#     print("hello world")

# if __name__ == "__main__":
#     main()