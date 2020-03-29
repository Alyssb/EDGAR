'''
CSC450 SP2020 Group 4
03/28/2020

MUST be run from EDGAR directory.
'''
'''
test cases:
    happy
    fearful
    angry
    sad
    neutral
    invalid  input
'''
import sys
sys.path.insert(1, "C:\\Users\\alyss\\Documents\\EDGAR\\functions\\")

import get_response

def test_happy():
    classification = 1
    responseObject = get_response.get_response(classification)
    responseObject.get_image()
    

def test_fear():
    classification = 2
    responseObject = get_response.get_response(classification)
    responseObject.get_image()

def test_angry():
    classification = 3
    responseObject = get_response.get_response(classification)
    responseObject.get_image()

def test_sad():
    classification = 4
    responseObject = get_response.get_response(classification)
    responseObject.get_image()

def test_neutral():
    classification = 5
    responseObject = get_response.get_response(classification)
    responseObject.get_image()

def test_invalid():
    classification = 0
    responseObject = get_response.get_response(classification)
    responseObject.get_image()

def main():
    test_happy()
    test_fear()
    test_angry()
    test_sad()
    test_neutral()
    test_invalid()

if __name__ == "__main__":
    main()