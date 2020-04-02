'''
Author: Cory &

Load saved model, run stuff through saved model
'''


#from __future__ import print_function, division

import torch
import numpy as np
import os

def loadModel():
    model = torch.load("testmodelsavewhole.pt")
    model.eval() #internet docs say you gotta do this, so do this. No I don't know why stop asking so many questions



if __name__ == '__main__':
    loadModel()
