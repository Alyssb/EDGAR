'''
Alyssa Slayton 2020
'''
'''
test cases:
    A standard run
    Make multiple recordings
    Use capital R
    Input invalid number of seconds
    Input invalid number of recordings
    Input invalid starting character
'''
import sys
import subprocess
from time import sleep
from os import system

# adds string to path for the running of this file
sys.path.insert(1, 'C:\\Users\\alyss\\Documents\\EDGAR\\functions\\')

# found because directory is now in path
import get_audio

def default_test():
    print("\nRunning default_test\n")
    p = create_audio()
    default_seconds(p)
    default_num_recordings(p)
    press_r(p)
    p.wait()
    p.kill()

def multiple_records():
    print("\nRunning multiple_records\n")
    p = create_audio()
    default_seconds(p)
    num_recordings = 3
    p.stdin.write('{}\n'.format(num_recordings).encode('utf-8'))
    press_r(p)
    p.wait()
    p.kill()

def capital_r():
    print("\nRunning capital_r\n")
    p = create_audio()
    default_seconds(p)
    default_num_recordings(p)
    r = 'R'
    p.stdin.write('{}\n'.format(r).encode('utf-8'))
    p.stdin.close()
    p.wait()
    p.kill()

def invalid_seconds():
    print("\nRunning invalid_seconds\n")
    p = create_audio()
    num_seconds = 'q'
    p.stdin.write('{}\n'.format(num_seconds).encode('utf-8'))
    default_num_recordings(p)
    press_r(p)
    p.wait()
    p.kill()

def invalid_num_recordings():
    print("\nRunning invalid_num_recordings\n")
    p = create_audio()
    default_seconds(p)
    num_recordings = 'q'
    p.stdin.write('{}\n'.format(num_recordings).encode('utf-8'))
    press_r(p)
    p.wait()
    p.kill()

def invalid_r():
    print("\nRunning invalid_r\n")
    p = create_audio()
    default_seconds(p)
    default_num_recordings(p)
    r = 'q'
    p.stdin.write('{}\n'.format(r).encode('utf-8'))
    p.stdin.close()
    p.wait()
    p.kill()

def create_audio():
    p = subprocess.Popen(['python', 'C:\\Users\\alyss\\Documents\\EDGAR\\get_audio.py'], stdin=subprocess.PIPE)
    return p

def default_seconds(p):
    sleep(1)
    num_seconds = 2
    p.stdin.write('{}\n'.format(num_seconds).encode('utf-8'))

def default_num_recordings(p):
    sleep(1)
    num_recordings = 1
    p.stdin.write('{}\n'.format(num_recordings).encode('utf-8'))

def press_r(p):
    sleep(1)
    r = 'r'
    p.stdin.write('{}\n'.format(r).encode('utf-8'))
    p.stdin.close()

def main():
    default_test()
    multiple_records()
    capital_r()
    invalid_seconds()
    invalid_num_recordings()
    invalid_r()

if __name__ == '__main__':
    main()