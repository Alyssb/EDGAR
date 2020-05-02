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
torch.manual_seed(0) #for consistency in model runs
np.random.seed(0)
torch.cuda.manual_seed(0)






transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])




# ********************************** class loadModel **********************************
def loadModel(metrics):
    
    '''
    I don't have the energy to modularize this class right now
    it's just going to be like this.
    parameters:
        metrics (npy array):            npy array that represents the mfcc of a WAV file
    returns:
        prediction (int):               representation of the emotion classified by the model
    local variables:
        model (RecursiveScriptModule):  instance of the model modelsavestate.py
        metrics (Tensor):               metrics parameter transformed into a tensor
        output (Tensor):                Tensor that represents output of model
        prediction (int):               integer representation of largest (most common) value in output
    '''

    # load and evaluate model (make function)

    #model = torch.load("modelsavestate1.pt") #load weights
##    model = torchvision.models.resnet18(pretrained=False) #put weights into model
##    #print(model)
##    num_ftrs = model.fc.in_features
##    # Adding layers on the end of the pretrained model.
##    # These layers will be the only layers trained while the model is running
##    model.fc = nn.Linear(num_ftrs, 5)
##    model.load_state_dict(torch.load("modelsavestate1.pt"))

    model = torch.load("modelsavewhole1.pt")
    model = model.to(device)

    model.eval()
    # transform passed numpy array into a tensor
    #metrics = torch.from_numpy(metrics)
    metrics = transform(metrics)
    # reform tensor into correct shape
    metrics = metrics.unsqueeze(0)
    #metrics = metrics.permute(0,3,1,2) # 0=1,1=480, 2=640, 3=3
    #print(metrics.shape)
    metrics = metrics.to(device)
    metrics = metrics.float()
    
    # run model on tensor
    output = model(metrics)
    m = nn.Softmax(dim=1)
    #m = nn.ReLU()
    output = m(output)
    
    s= nn.Sigmoid()
    output=s(output)
    #print(output)
    #print(output)

    #for the purpose of human readability, the inference will apply weight to the ouput so that a proper response can be generated
    #0.757352941, 0.990686275, 0.870588235, 0.624019608, 0.757352941 #the original weights
    #0.7, 0.9, 0.8, 0.6, 0.7 #the 'fine-tuned' weights
    #weight = torch.tensor([0.757352941, 0.990686275, 0.870588235, 0.624019608, 0.757352941])
    weight = torch.tensor([0.75, 0.835, 0.80, 0.6, 0.75])
    weight = weight.to(device)
    output = (output*weight)
    #print(output)
    # get predicted emotion
    prediction = int(torch.argmax(output))    
    
    return prediction


# ********************************** main **********************************
if __name__ == '__main__':
    print("main function of run_torch_model.py")

    tester = np.load("test.npy")
    print(loadModel(tester)) #tis a sad one
        
##    tester = np.load("testhap.npy")
##    print(loadModel(tester))
##    
##    tester = np.load("testfear.npy")
##    print(loadModel(tester))
##    
##    tester = np.load("testsad.npy")
##    print(loadModel(tester))
##    
##    tester = np.load("testanger.npy")
##    print(loadModel(tester))
##    
##    tester = np.load("testneu.npy")
##    print(loadModel(tester))
