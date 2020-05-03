'''
CSC450 SP2020 Group 4
03/08/2020

MUST be run from EDGAR directory.
'''
'''
Tests decibel_detection.py

Test Cases (from test suite):
    FR.01-TC.01 User should be able to record audio in system
    FR.01-TC.02 audio length should not be more than 3 seconds
    FR.01-TC.03 audio collection should initiate recording of user's speech
    NFR.01-TC.01    edgar should pad audio data shorter than 3 seconds
    NFR.01-TC.02    audio collection component should segment recording in 3 seconds length
    NFR.01-TC.03    edgar should not process data shorter than 1 seconds
    NFR.02-TC.01    edgar should convert audio data to WAV format
    NFR.05-TC.02    lms should be passed to neural network
    DC.01-TC.01     system must not require a wake word to stop recording
    DC.03-TC.01     classification should not depend on semantic context of speech
    EIR.02-TC.01    system should allow users to input speech via microphone
    

'''
def main():
    print("hello world")

if __name__ == '__main__':
    main()