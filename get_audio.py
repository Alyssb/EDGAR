import pyaudio
import wave
from pydub import AudioSegment
from pydub.playback import play
import random


def get_audio():

    custom_seconds = input("how long do you want to record? ")
    num_recordings = input("How many recordings of that length would you like? ")
    #start = raw_input("Press 'r' to beging recording. ") #is this python 2?
    start = input("type and enter 'r' to begin recording. ")


    if start == 'r' or 'R':
        for b in range(int(num_recordings)):
            chunk = 1024  # Record in chunks of 1024 samples
            sample_format = pyaudio.paInt16  # 16 bits per sample
            channels = 2
            fs = 44100  # Record at 44100 samples per second
            seconds = int(custom_seconds)

            unique_num = random.randint(1,10000)

            filename = 'recording_audio/Output/Output' + str(unique_num) + '.wav'

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
            print('Finished recording ' + str(b))

            # Save the recorded data as a WAV file
            wf = wave.open(filename, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(sample_format))
            wf.setframerate(fs)
            wf.writeframes(b''.join(frames))
            wf.close()

            # sound = AudioSegment.from_wav(filename)
            # play(sound)
            return filename

    else:
        print("Incorrect key. Run program again.")
