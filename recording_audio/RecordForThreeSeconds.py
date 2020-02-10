# so it turns out this just straight up does not work
# Requires ffmpeg, but I had no luck getting pydub to work with it.
# moving on.

import pyaudio
import wave
from pydub import AudioSegment
from pydub.playback import play
import random

AudioSegment.ffmpeg = "C:\\Users\\alyss\\Documents\\miscDevTools\\ffmpeg-20200209-5ad1c1a-win64-static\\bin"

print("Press 'r' to beging recording.")
start = input()

if start == 'r' or 'R':
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = 3

    unique_num = random.randint(1,10000)

    filename = 'Output/Output' + str(unique_num) + '.wav'

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames


    # Store data in chunks for 3 seconds i.e. recording
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()
    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    sound = AudioSegment.from_wav(filename)
    play(sound)

else:
    print("Incorrect key. Run program again.")