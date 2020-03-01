'''
Alyssa Slayton 2020
'''
'''
test cases:
    idk yo
    creates file
    returns file
'''
import sys
import subprocess
from time import sleep
from os import system

sys.path.insert(1, 'C:\\Users\\alyss\\Documents\\EDGAR\\')

import get_audio

def create_audio():
    p = subprocess.Popen(['python', 'C:\\Users\\alyss\\Documents\\EDGAR\\get_audio.py'], stdin=subprocess.PIPE)
    return p
# will input 3 to command line, for use as the default for recording length
def default_seconds(p):
    sleep(1)
    num_seconds = 2
    p.stdin.write('{}\n'.format(num_seconds).encode('utf-8'))

def default_num_recordings(p):
    sleep(1)
    num_recordings = 3
    p.stdin.write('{}\n'.format(num_recordings).encode('utf-8'))

def default_test():
    p = create_audio()
    default_seconds(p)
    default_num_recordings(p)
    record_input = 'r'
    p.stdin.write('{}\n'.format(record_input).encode('utf-8'))
    p.stdin.close()
    p.wait()
    p.kill()

def main():
    default_test()

if __name__ == '__main__':
    main()