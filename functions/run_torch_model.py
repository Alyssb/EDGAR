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
import torch.optim as optim
# ********************************** end imports **********************************

# sets the device to either the available GPU or system CPU
device = torch.device("cpu" if not (torch.cuda.is_available()) else "cuda:0")

#transform sets the incoming number array into a tensor and normalizes the image based off RGB values as per stated by ResNet's preferred input specifications
transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

'''
function loadModel
loads a torch model 
runs it on the inputted numpy array
parameters:
    metrics (npy array):            npy array that represents the mfcc of a WAV file
optional parameters: (the weights do not need to be positive, sum to 1, or be below 1)
    anger_weight (float):           float containing weight value for anger output, change per user customization, default of 0.75
    fear_weight (float):            float containing weight value for fear output, change per user customization, default of 0.835
    happy_weight (float):           float containing weight value for happy output, change per user customization, default of 0.8
    neutral_weight (float):         float containing weight value for neutral output, change per user customization, default of 0.6
    sad_weight (float):             float containing weight value for sad output, change per user customization, default of 0.75
returns:
    prediction (int):               representation of the emotion classified by the model
local variables:
    model (RecursiveScriptModule):  instance of the model modelsavewhole1.py
    metrics (Tensor):               metrics parameter transformed into a tensor
    weight (Tensor):                tensor list of weights of each emotion to balance output
    output (Tensor):                Tensor that represents output of model
    prediction (int):               integer representation of largest (most common) value in output
'''
class run_model:

    def __init__(self, metrics):
        self.metrics = metrics.copy()
        self.anger_weight = 0.75
        self.fear_weight = 0.835
        self.happy_weight = 0.8
        self.neutral_weighht = 0.6
        self.sad_weight = 0.75 

    def load_model(self):
        # load and evaluate model (make function)
        self.model = torch.load("modelsavewhole1.pt", map_location=device)
        self.model = model.to(device)

        self.model.eval()
        # transform passed numpy array into a tensor

    def transform_metrics(self):
        self.metrics = transform(self.metrics)
    
        # reform tensor into correct shape, send to device, and data format
        metrics = metrics.unsqueeze(0)
        metrics = metrics.to(device)
        metrics = metrics.float()

    def run_model(self):
        # run model on tensor
        self.output = model(metrics)
        #modify output based off Softmax to modify outputs to sum to 1
        m = nn.Softmax(dim=1)
        self.output = m(output)
    
        # apply sigmoid
        s = nn.Sigmoid()
        self.output = s(output)

    '''
    for the purpose of human readability, 
    the inference will apply weight to the output 
    so that a more accurate response can be generated
    '''
    def fine_tune(self):
        # original weights:     0.757352941, 0.990686275, 0.870588235, 0.624019608, 0.757352941
        # 'fine-tuned' weights: 0.75, 0.835, 0.80, 0.6, 0.75
        self.weight = torch.tensor([anger_weight, fear_weight, happy_weight, neutral_weight, sad_weight])
        self.weight = weight.to(device)
        self.output = (output*weight)
        
        print("WEIGHTS:")
        print("anger\tfear\thappy\tneutral\tsad")
        print(self.output[0], "\t", self.output[1], "\t", self.output[2], "\t", self.output[3], "\t", self.output[4])

    def get_prediction(self):
        # get predicted emotion
        self.prediction = int(torch.argmax(self.output))    
    
        return self.prediction


# ********************************** main **********************************
if __name__ == '__main__':
    print("main function of run_torch_model.py")

    tester = np.load("test.npy")
    print(loadModel(tester)) #tis a sad one
        
    tester = np.load("testhap.npy") #left here for possible copy/paste format to quickly input a single numpy image for input testing
    print(loadModel(tester))
    
    tester = np.load("testfear.npy")
    print(loadModel(tester))
    
    tester = np.load("testsad.npy")
    print(loadModel(tester))
