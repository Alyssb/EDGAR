'''
CSC450 SP2020 Group 4
03/08/2020

MUST be run from EDGAR directory.
'''
'''
Tests decibel_detection.py

test cases:

from test suite:
    FR.01-TC.01     User should be able to record audio in system
    FR.01-TC.02     audio length should not be more than 3 seconds
    FR.01-TC.03     audio collection should initiate recording of user's speech
    NFR.01-TC.01    edgar should pad audio data shorter than 3 seconds
    NFR.01-TC.02    audio collection component should segment recording in 3 seconds length
    NFR.01-TC.03    edgar should not process data shorter than 1 seconds
    NFR.02-TC.01    edgar should convert audio data to WAV format
    NFR.05-TC.02    lms should be passed to neural network
    DC.01-TC.01     system must not require a wake word to stop recording
    DC.03-TC.01     classification should not depend on semantic context of speech
    EIR.02-TC.01    system should allow users to input speech via microphone
'''
import sys
import time
from os.path import exists
import numpy as np
sys.path.append('./functions/')

import decibel_detection

import wave


def setup_dd():
    dd = decibel_detection.do_record()
    return(dd)

def run_dd():
    dd = decibel_detection.do_record()
    dd.setup_record()
    dd.check_dB()


def skip_while():
    dd = decibel_detection.do_record()
    dd.setup_record()
    dd.input = dd.stream.read(1024, exception_on_overflow = False)
    return(dd.input)


def skip_checks():
    dd = decibel_detection.do_record()
    dd.setup_record()
    dd.cont = False
    dd.record_3sec()
    return dd


def test_mic_chunk():
    print("\nRunning test_mic_chunk\n")
    mic_input = skip_while()
    if mic_input is not None:
        print("\n\ttest_mic passed")
    else:
        print("\n\ttest_mic failed")


def test_mic_sr():
    print("\nRunning test_mic_sr\n")
    # recommended no speech is happening during this time.
    dd = setup_dd()
    dd.get_audio_for_check()
    if dd.audio is not None:
        print("\n\ttest_mic_sr passed")
    else:
        print("\n\ttest_mic_sr failed")


def test_valid_wav():
    print("\nRunning test_valid_wav\n")
    dd = skip_checks()
    filename = dd.filename
    if(wave.open(filename)):
        print("\ttest_valid_wav passed")
    else:
        print("\ttest_valid_wav failed")


def test_recording_length():
    # duration = number frames / framerate
    # doesn't have to be exactly 3 seconds anymore, just preferred to be around it
    print("\nRunning test_recording_length\n")
    dd = skip_checks()
    filename = dd.filename
    f = wave.open(filename, 'r')
    frames = f.getnframes()
    rate = f.getframerate()
    f.close()
    if (frames / rate) >= (0.95 * 3) and (frames / rate) <= (1.05 * 3):
        print("\n\ttest_recording_length passed")
    elif (frames / rate) <= (0.95 * 3):
        print("\n\tRecording too short. test_recording_length failed")
    elif (frames / rate) <= (1.05 * 3):
        print("\n\tRecording too long. test_recording_length failed")


def test_write_to_file():
    print("\nRunning test_write_to_file\n")
    dd = skip_checks()
    filename = dd.filename
    if (exists(filename)):
        print("\t" + filename + " created")
        print("\ttest_write_to_file passed")
    else:
        print("\ttest_write_to_file failed")


def test_runtime():
    print("\nRunning test_runtime\n")
    print("\nRunning test_runtime")
    current_time = time.time()
    dd = skip_checks()
    print("TIME ELAPSED: ", round(time.time() - current_time, 3), " seconds")


def test_melspec():
    # WILL DELETE YOUR WAV FILE
    print("\nRunning test_melspec\n")
    cont_dd = decibel_detection.next_steps("./testing/testaudio.wav")
    cont_dd.run_get_melSpectrogram()    
    print("\tIf no errors, test_melspec passed")


def test_model():
    print("\nRunning test_model\n")
    cont_dd = decibel_detection.next_steps("./testing/testaudio.wav")
    cont_dd.run_run_model(np.load("./testing/test_melspec.npy"))
    print("\tIf no errors, test_model passed")


def test_response():
    print("\nRunning test_response\n")
    cont_dd = decibel_detection.next_steps("./testing/testaudio.wav")
    response = 0
    cont_dd.run_get_response(response)
    if(cont_dd.out.response == "ANGER"):
        print("\ttest_resposnse passed")


def total_runtime():
    print("\nRunning total_runtime\n")
    current_time = time.time()
    dd = skip_checks()
    dd.continue_EDGAR()
    print("TOTAL TIME ELAPSED: ", round(time.time() - current_time, 3), " seconds")


def main():
    test_mic_chunk()
    test_mic_sr()
    test_valid_wav()
    test_recording_length()
    test_write_to_file()
    test_runtime()
    # test_melspec()    # commented because it deletes the WAV file. It passes.
    test_model()
    test_response()
    total_runtime()

if __name__ == '__main__':
    main()