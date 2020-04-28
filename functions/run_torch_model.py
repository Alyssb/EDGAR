'''
CSC450 SP2020 Group 4 (Cory Jackson)
Missouri State University
Loads a saved model
Runs a spectrogram through loaded model
'''
# ********************************** imports **********************************
# general imports
import numpy as np
import os
import time

# pytorch imports3
import torch
import torch.nn as nn
import torchvision
from torchvision import transforms

# ********************************** end imports **********************************

# sets the device to either the available GPU or system CPU
device = torch.device("cpu" if not (torch.cuda.is_available()) else "cuda:0")

# ********************************** class loadModel **********************************
def loadModel(metrics):
    
    '''
    I don't have the energy to modularize this class right now
    it's just going to be like this.
    parameters:
        metrics (npy array):            npy array that represents the mfcc of a WAV file
    returns:
        preduction (int):               representation of the emotion classified by the model
    local variables:
        model (RecursiveScriptModule):  instance of the model testmodelsavewhole4.py
        metrics (Tensor):               metrics parameter transformed into a tensor
        output (Tensor):                Tensor that represents output of model
        prediction (int):               integer representation of largest (most common) value in output
    '''

    # load and evaluate model (make function)
    model = torch.load("testmodelsavewhole4.pt", map_location=device)
    model.eval()

    # transform passed numpy array into a tensor
    metrics = np.copy(metrics)
    metrics = torch.from_numpy(metrics)
    
    # reform tensor into correct shape
    metrics = metrics.unsqueeze(0)
    metrics = metrics.permute(0,3,1,2) #0,3,1,2 or 0,3,2,1 0=1,1=40, 2=224, 3=3
    
    # send to device for analysis
    metrics = metrics.to(device)
    model = model.to(device)
    metrics = metrics.float()

    # run model on tensor
    output = model(metrics)

    # get predicted emotion
    prediction = int(torch.argmax(output))    
    
    return prediction


# ********************************** main **********************************
if __name__ == '__main__':
    print("main function of run_torch_model.py")
