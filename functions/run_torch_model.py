'''
Author: Cory &

Load saved model, run stuff through saved model
'''

#from __future__ import print_function, division

import torch
import torch.nn as nn
import torchvision
from torchvision import transforms
import numpy as np
import os
import time

device = torch.device("cpu" if not (torch.cuda.is_available()) else "cuda:0")
#torch.nn.Module.dump_patches = True

def loadModel(metrics):
    
    model = torch.load("testmodelsavewhole4.pt", map_location=device) #whole model, 4/10- use this not state, state is unstable it seems
#start of state code
##    model = torchvision.models.resnet18(pretrained=True)
##    # "Freeze" the weights on the pretrained model.
##    for param in model.parameters():
##        param.requires_grad = False
##
##    # Parameters of newly constructed modules have requires_grad=True by default
##    num_ftrs = model.fc.in_features
##    # Adding layers on the end of the pretrained model.
##    # These layers will be the only layers trained while the model is running
##    model.fc = nn.Linear(num_ftrs, 10)
##
##    # Sending the model to the device it will be trained on
##    model = model.to(device)
#end of state code

    
    model.eval() #internet docs say you gotta do this, so do this. No I don't know why stop asking so many questions

    metrics = np.copy(metrics)
    metrics = torch.from_numpy(metrics)
    
    metrics = metrics.unsqueeze(0)
    # metrics = metrics.unsqueeze(0)

    # print(metrics.shape) # [1,1,40,98]
    metrics = metrics.permute(0,3,1,2) #0,3,1,2 or 0,3,2,1 0=1,1=40, 2=224, 3=3
    
    metrics = metrics.to(device)
    model = model.to(device)
    metrics = metrics.float()

    output = model(metrics)

    prediction = int(torch.argmax(output))
    #print("this be the prediction ",prediction)
    
    
    return prediction


if __name__ == '__main__':
    print("welcome to run_torch_model.py")
##    since = time.time()
##    #test code below
##    tester = np.load("testanger.npy")
##    print("ang(0?): ")
##    loadModel(tester)
##    time_elapsed = time.time() - since
##    print('Training complete in {:.0f}m {:.0f}s'.format(
##        time_elapsed // 60, time_elapsed % 60))
##    
##    tester = np.load("testfear.npy")
##    print("fear(1?): ")
##    loadModel(tester)
##    
##    tester = np.load("testhap.npy")
##    print("hap(2?): ")  
##    loadModel(tester)
##    
##    tester = np.load("testneu.npy")
##    print("neu: (3?)")
##    loadModel(tester)
##    
##
##
##    tester = np.load("testsad.npy")
##    print("sad(4?): ")
##    loadModel(tester)
##
##    time_elapsed = time.time() - since
##    print('Training complete in {:.0f}m {:.0f}s'.format(
##        time_elapsed // 60, time_elapsed % 60))
