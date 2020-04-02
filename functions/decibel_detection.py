'''
CSC450 Team 4
Detects the decibel level and activates EDGAR if 60dB is exceeded

right now im just using this for getting audio continuously
'''

import pyaudio
import time

temp = True
chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100

while temp:
    unique_num = int(time.time())
    final_time = unique_num + 3
    print(unique_num)

    filename = 'live_audio/Output' + str(temp) + '.wav'

    p = pyaudio.PyAudio()

    stream = p.open(format=sample_format, 
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []

    data = stream.read(chunk)
    frames.append(data)

    if time.time() < final_time:
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setfreamerate(fs)
        wf.writeframes(join(frames))
        wf.close()
        temp = False

# def main():
#     print("hello world")

# if __name__ == "__main__":
#     main()