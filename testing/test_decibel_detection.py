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
sys.path.append('./functions/')

import decibel_detection


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


def main():
    test_mic_chunk()
    test_mic_sr()

if __name__ == '__main__':
    main()