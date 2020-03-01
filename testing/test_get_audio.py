'''
Alyssa Slayton 2020
'''
'''
test cases:
    idk yo
    creates file
    returns file
'''
import get_audio
from os import system

def create_audio():
    audio_object = get_audio.get_audio()
    return audio_object

# will input 3 to command line, for use as the default for recording length
def default_seconds():
    system("3")

def default_num_recordings():
    system("1")

def test_seconds():
    audio_object = create_audio()


def main():
    print("hello world.")

if __name__ == '__main__':
    main()