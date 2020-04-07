'''
Author: Zack Roy

Attempt at moving CNN recognition model from tensorflow to pytorch
'''

from __future__ import print_function, division

import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
from numpy.random import default_rng
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import os
import copy

plt.ion()
#C:\\Users\\PremiumHamsters\\Documents\EDGAR\mine\model_training\metrics_stretched_no_xxx
#FILEPATH = "C:\\Users\\PremiumHamsters\\EDGAR\\mine\\model_building\\organized_metrics\\"
FILEPATH = "C:\\Users\\PremiumHamsters\\Documents\\EDGAR\\mine\\model_training\\organized_metrics\\"
x_dim = 40
y_dim = 224
z_dim = 3
channel_dim = 1
batch_size = 32
img_shape = (x_dim, y_dim, z_dim)


# ************** Organizing files into proper folders **************************
# ********* WARNING, this takes a while but only needs to run once *************
# Separating 750 random images for validation
# This method of generation allows with/without replacement
##print("yes doing this first")
##rng = default_rng(11)
##test_index = rng.choice(7531, size=750, replace=False)
##labels = np.load(FILEPATH + "\\label_list_stretched_no_xxx.npy")
##for i in range(0, 7531):
##     print(i)
##     spectrogram = np.load(FILEPATH + "\\mine\\model_training\\metrics_stretched_no_xxx\\{}.npy".format(i),
##                           allow_pickle=False)
##     this_label = labels[i]
##     if i in test_index:
##         test_val = "val"
##     else:
##         test_val = "train"
##     np.save(FILEPATH + "\\mine\\model_training\\organized_metrics\\{}\\{}\\{}.npy".format(
##         test_val, this_label, i), spectrogram)
##exit()


# ******************** Pytorch example begins **********************
# https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html

def loadNumpyFile(pathname):
    return np.load(pathname, allow_pickle=False)


data_transforms = {
    'train': transforms.Compose([
        # transforms.RandomResizedCrop(224),
        # transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        # transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'val': transforms.Compose([
        # transforms.Resize(256),
        # transforms.CenterCrop(224),
        transforms.ToTensor(),
        # transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}

#data_dir = os.getcwd() + "\\mine\\model_training\\organized_metrics"
data_dir = FILEPATH

image_datasets = {x: datasets.DatasetFolder(os.path.join(data_dir, x), loadNumpyFile,
                                            transform=data_transforms[x], extensions=("npy"))
                  for x in ['train', 'val']}
dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=4,
                                              shuffle=True, num_workers=4)
               for x in ['train', 'val']}
dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
class_names = image_datasets['train'].classes

#print(torch.cuda.is_available())
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def train_model(model, criterion, optimizer, scheduler, num_epochs=25):
    since = time.time()

    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    for epoch in range(num_epochs):
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('-' * 10)

        # Each epoch has a training and validation phase
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()  # Set model to training mode
            else:
                model.eval()   # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0

            # Iterate over data.
            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward
                # track history if only in train
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    #print(outputs, labels)
                    loss = criterion(outputs, labels)

                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                # statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)
            if phase == 'train':
                scheduler.step()

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            print('{} Loss: {:.4f} Acc: {:.4f}'.format(
                phase, epoch_loss, epoch_acc))

            # deep copy the model
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())

        print()

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(
        time_elapsed // 60, time_elapsed % 60))
    print('Best val Acc: {:4f}'.format(best_acc))

    # load best model weights
    model.load_state_dict(best_model_wts)
    return model


if __name__ == '__main__':
    # Initailize model with pretrained resnet18 model.
    model_conv = torchvision.models.resnet18(pretrained=True)
    # "Freeze" the weights on the pretrained model.
    for param in model_conv.parameters():
        param.requires_grad = False

    # Parameters of newly constructed modules have requires_grad=True by default
    num_ftrs = model_conv.fc.in_features
    # Adding layers on the end of the pretrained model.
    # These layers will be the only layers trained while the model is running
    model_conv.fc = nn.Linear(num_ftrs, 10)

    # Sending the model to the device it will be trained on
    model_conv = model_conv.to(device)

    # Initalizing the loss criteria from which weights will be adjusted
    criterion = nn.CrossEntropyLoss()

    # Initalizing optimizer
    optimizer_conv = optim.SGD(
        model_conv.fc.parameters(), lr=0.001, momentum=0.9)

    # Decay LR by a factor of 0.1 every 7 epochs
    exp_lr_scheduler = lr_scheduler.StepLR(
        optimizer_conv, step_size=7, gamma=0.1)

    # Train the model.
    model_conv = train_model(model_conv, criterion, optimizer_conv,
                             exp_lr_scheduler, num_epochs=30)

    torch.save(model_conv.state_dict(), "testmodelsavestate.pt")

    torch.save(model_conv, "testmodelsavewhole.pt")

    #print(model_conv)

##
##    loadmodel = torchvision.models.resnet18(pretrained=True)
##    # "Freeze" the weights on the pretrained model.
##    for param in loadmodel.parameters():
##        param.requires_grad = False
##
##    # Parameters of newly constructed modules have requires_grad=True by default
##    num_ftrs = loadmodel.fc.in_features
##    # Adding layers on the end of the pretrained model.
##    # These layers will be the only layers trained while the model is running
##    loadmodel.fc = nn.Linear(num_ftrs, 10)
##
##    # Sending the model to the device it will be trained on
##    loadmodel = loadmodel.to(device)
    #loadmodel = torchvision.models.resnet18(pretrained=True)
    
    #loadmodel.load_state_dict(torch.load("testmodelsavestate.pt"))
    #loadmodel.eval()
    #print(loadmodel.eval())
    #model_conv.load_

    model = torch.load("testmodelsavewhole.pt")
    model.eval()

    exit()
