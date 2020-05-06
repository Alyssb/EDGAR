'''
CSC450 SP2020 Group 4
Missouri State University

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
    runtime

from test suite:
    FR.04-TC.01     system should show classification result in command line
    NFR.07-TC.01    EDGAR should respond with detected emotion in less than 1 second
    EIR.01-TC.01    system should show the classification result to the user

'''
import time
import sys
sys.path.append('./functions/')

import get_response

def test_anger():
    print("\nRunning test_anger")
    classification = 0
    responseObject = get_response.get_response(classification)
    responseObject.get_output()
    if responseObject.response == "ANGER":
        print("\ttest_anger passed")
    else:
        print("\ttest_anger failed")
    

def test_fear():
    print("\nRunning test_fear")
    classification = 1
    responseObject = get_response.get_response(classification)
    responseObject.get_output()
    if responseObject.response == "FEAR":
        print("\ttest_fear passed")
    else:
        print("\ttest_fear failed")


def test_happy():
    print("\nRunning test_happy")
    classification = 2
    responseObject = get_response.get_response(classification)
    responseObject.get_output()
    if responseObject.response == "HAPPY":
        print("\ttest_happy passed")
    else:
        print("\ttest_happy failed")


def test_neutral():
    print("\nRunning test_neutral")
    classification = 3
    responseObject = get_response.get_response(classification)
    responseObject.get_output()
    if responseObject.response == "NEUTRAL":
        print("\ttest_neutral passed")
    else:
        print("\ttest_neutral failed")



def test_sad():
    print("\nRunning test_sad")
    classification = 4
    responseObject = get_response.get_response(classification)
    responseObject.get_output()
    if responseObject.response == "SAD":
        print("\ttest_sad passed")
    else:
        print("\ttest_sad failed")


def test_invalid():
    classification = 5
    responseObject = get_response.get_response(classification)
    responseObject.get_output()
    print("\ttest_invalid passed if output was:\t5 is not a valid classification")


def test_runtime():
    classification = 0
    current_time = time.time()

    responseObject = get_response.get_response(classification)
    responseObject.get_output()

    print("TIME ELAPSED: ", round(time.time() - current_time, 3), " seconds")


def main():
    test_anger()
    test_fear()
    test_happy()
    test_neutral()
    test_sad()
    test_invalid()
    test_runtime()

if __name__ == "__main__":
    main()