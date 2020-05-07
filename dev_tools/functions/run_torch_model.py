#! /usr/bin/env python
'''
CSC450 SP2020 Group 4 (Cory Jackson)
Missouri State University

Loads a saved model
Runs a spectrogram through loaded model

FUNCTIONAL REQUIREMENTS
FR.01
FR.04
NFR.05
NFR.06
DC.03
'''
# ********************************** imports **********************************
# general imports
import numpy as np
import os
import time
import warnings
warnings.filterwarnings("ignore")

# pytorch imports3
import torch
import torch.nn as nn
import torchvision
from torchvision import transforms
import torch.optim as optim

# ********************************** class run_model **********************************

class run_model:
    '''
    init function
    parameters:
        metrics (npy array):            npy array that represents the mfcc of a WAV file
    optional parameters: (the weights do not need to be positive, sum to 1, or be below 1)
        anger_weight (float):           float containing weight value for anger output, change per user customization, default of 0.75
        fear_weight (float):            float containing weight value for fear output, change per user customization, default of 0.835
        happy_weight (float):           float containing weight value for happy output, change per user customization, default of 0.8
        neutral_weight (float):         float containing weight value for neutral output, change per user customization, default of 0.6
        sad_weight (float):             float containing weight value for sad output, change per user customization, default of 0.75
    '''
    def __init__(self, metrics, anger_weight=0.75, fear_weight=0.835, happy_weight=0.8, neutral_weight=0.6, sad_weight=0.75):
        self.metrics = metrics.copy()
        self.anger_weight = anger_weight
        self.fear_weight = fear_weight
        self.happy_weight = happy_weight
        self.neutral_weight = neutral_weight
        self.sad_weight = sad_weight

        # sets the device to either the available GPU or system CPU
        self.device = torch.device("cpu" if not (torch.cuda.is_available()) else "cuda:0")

        # transform sets the incoming number array into a tensor 
        # normalizes the image based off RGB values 
        # as per stated by ResNet's preferred input specifications
        self.transform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])


    '''
    FR.01   EDGAR must classify the emotion of a speaker
    NFR.05  EDGAR must classify the emotion of the speaker in less than 3 seconds

    function load_model
    loads and evaluates model
    class variables:
        model (RecursiveScriptModule):  instance of the model modelsavewhole1.py
    '''
    def load_model(self):
        self.model = torch.load("modelsavewhole1.pt", map_location=self.device)
        self.model = self.model.to(self.device)

        self.model.eval()   # transform passed numpy array into a tensor


    '''
    FR.01   EDGAR must classify the emotion of a speaker
    NFR.05  EDGAR must classify the emotion of the speaker in less than 3 seconds
    
    function transform_metrics
    transforms metrics into a tensor of the correct shape and format
    class variables:
        metrics (Tensor):   metrics parameter transformed into a tensor
    '''
    def transform_metrics(self):
        self.metrics = self.transform(self.metrics)
    
        # reform tensor into correct shape, send to device, and data format
        self.metrics = self.metrics.unsqueeze(0)
        self.metrics = self.metrics.to(self.device)
        self.metrics = self.metrics.float()


    '''
    FR.01   EDGAR must classify the emotion of a speaker
    NFR.05  EDGAR must classify the emotion of the speaker in less than 3 seconds
    DC.03   EDGAR shall not use semantic context to identify emotion
    
    function run_model
    runs model on tensor
    class variables:
        output (Tensor):    Tensor that represents output of model
    local variables:
        m (Softmax):        modifies outputs to sum to 1
        s (Sigmoid):        sigmoid that can be applied to output
    '''
    def run_model(self):
        self.output = self.model(self.metrics)

        # modify output based off Softmax to modify outputs to sum to 1
        m = nn.Softmax(dim=1)
        self.output = m(self.output)
    
        # apply sigmoid
        s = nn.Sigmoid()
        self.output = s(self.output)

    '''
    FR.01   EDGAR must classify the emotion of a speaker
    NFR.05  EDGAR must classify the emotion of the speaker in less than 3 seconds
    NFR.06  EDGAR must correctly identify emotion at least 75% of the time

    function fine_tune
    applies weights to output to generate a more accurate prediction
    class variables:
        weight (Tensor):                tensor list of weights of each emotion to balance output
    '''
    def fine_tune(self):
        # original weights:     0.757352941, 0.990686275, 0.870588235, 0.624019608, 0.757352941
        # 'fine-tuned' weights: 0.75, 0.835, 0.80, 0.6, 0.75
        self.weight = torch.tensor([self.anger_weight, self.fear_weight, self.happy_weight, self.neutral_weight, self.sad_weight])
        self.weight = self.weight.to(self.device)
        self.output = (self.output*self.weight)


    '''
    FR.04   EDGAR must show classification to the user

    function print_output
    prints the weights of each emotion in an understandable way
    '''
    def print_output(self):
        print("\n" + "".join("WEIGHTS:".center(50)))

        print("".join("ANGER".ljust(10)), 
              "".join("FEAR".ljust(10)), 
              "".join("HAPPY".ljust(10)), 
              "".join("NEUTRAL".ljust(10)), 
              "".join("SAD".ljust(10)))

        print("".join(str(round(self.output[0][0].item(), 3)).ljust(10)), 
              "".join(str(round(self.output[0][1].item(), 3)).ljust(10)), 
              "".join(str(round(self.output[0][2].item(), 3)).ljust(10)), 
              "".join(str(round(self.output[0][3].item(), 3)).ljust(10)), 
              "".join(str(round(self.output[0][4].item(), 3)).ljust(10)))


    '''
    FR.01   EDGAR must classify the emotion of a speaker
    NFR.05  EDGAR must classify the emotion of the speaker in less than 3 seconds
    DC.03   EDGAR shall not use semantic context to identify emotion
    
    function get_prediction
    gets the prediction from the output
    returns:
        prediction (int):   integer representation of largest (most common) value in output
    '''
    def get_prediction(self):
        # get predicted emotion
        self.prediction = int(torch.argmax(self.output))    
    
        return self.prediction


# ********************************** main **********************************
if __name__ == '__main__':
    print("main function of run_torch_model.py")
