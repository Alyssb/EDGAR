'''
CSC450 SP2020 Group 4
Missouri State Univeristy

MUST be run from EDGAR directory.
'''
'''
test cases:
    Valid output
    Runtime
    
from test suite
    FR.03-TC.01     system should classify the emotion of a speaker's speech
    NFR.05-TC.01    edgar shall classify emotion of the speaker in less than 3 seconds
    NFR.06-TC.01    edgar should correctly identify emotion at least 75% of the time
    NFR.06-TC.02    build and train CCNN using audio files from database
        untestable?
'''
import time
from numpy import load
import sys
sys.path.append('./functions/')

from run_torch_model import run_model

def run_run_model(filename):
    test_melspec = load(filename, allow_pickle=True)

    model_object = run_model(test_melspec)
    model_object.load_model()
    model_object.transform_metrics()
    model_object.run_model()
    model_object.fine_tune()
    model_object.print_output()
    return(model_object.get_prediction())

def test_output():
    print("\nRunning test_output")
    result = run_run_model("./testing/test_melspec.npy")
    if isinstance(result, int) == True and result >= 0 and result <= 4:
        print("\ttest_output passed")
    else:
        print("\ttest_output failed")


def test_runtime():
    current_time = time.time()
    result = run_run_model("./testing/test_melspec.npy")
    print("TIME ELAPSED: ", round(time.time() - current_time, 3), " seconds")


def main():
    test_output()
    test_runtime()

if __name__ == '__main__':
    main()