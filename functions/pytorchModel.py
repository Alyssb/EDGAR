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

FILEPATH = "C:\\Users\\zackj\\450\\mine\\model_building\\organized_metrics\\"

x_dim = 40
y_dim = 1067
z_dim = 3
channel_dim = 1
batch_size = 32
img_shape = (x_dim, y_dim, z_dim)


# ************** Organizing files into proper folders **************************
# ********* WARNING, this takes a while but only needs to run once *************
# Separating 750 random images for validation
# This method of generation allows with/without replacement
# rng = default_rng(11)
# test_index = rng.choice(7531, size=750, replace=False)
# for i in range(0, 7531):
#     print(i)
#     spectrogram = np.load(FILEPATH + "\\mine\\model_training\\metrics_stretched_no_xxx\\{}.npy".format(i),
#                           allow_pickle=False)
#     this_label = labels[i]
#     if i in test_index:
#         test_val = "val"
#     else:
#         test_val = "train"
#     np.save(FILEPATH + "\\mine\\model_training\\organized_metrics\\{}\\{}\\{}.npy".format(
#         test_val, this_label, i), spectrogram)
# exit()


# **************** Maybe unneeded? ***********************
# turning labels into integers
# label_dict = {'ang': 0, 'dis': 1, 'exc': 2, 'fea': 3, 'fru': 4,
#               'hap': 5, 'neu': 6, 'oth': 7, 'sad': 8, 'sur': 9, 'xxx': 10}
# new_train_labels = []
# new_test_labels = []
# for label in train_labels:
#     new_train_labels.append(label_dict[label])
# for label in test_labels:
#     new_test_labels.append(label_dict[label])
# new_train_labels = np.array(new_train_labels)
# new_test_labels = np.array(new_test_labels)


# ******************** Pytorch example begins **********************
# https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html
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

# @TODO this will have to be changed based on where your data is
data_dir = os.getcwd() + "\\mine\\model_training\\organized_metrics"
print(data_dir)
image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x),
                                          data_transforms[x])
                  for x in ['train', 'val']}
dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=4,
                                              shuffle=True, num_workers=4)
               for x in ['train', 'val']}
dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
class_names = image_datasets['train'].classes
print(dataset_sizes)
print(image_datasets["train"][1])


# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


# def train_model(model, criterion, optimizer, scheduler, num_epochs=25):
#     since = time.time()

#     best_model_wts = copy.deepcopy(model.state_dict())
#     best_acc = 0.0

#     for epoch in range(num_epochs):
#         print('Epoch {}/{}'.format(epoch, num_epochs - 1))
#         print('-' * 10)

#         # Each epoch has a training and validation phase
#         for phase in ['train', 'val']:
#             if phase == 'train':
#                 model.train()  # Set model to training mode
#             else:
#                 model.eval()   # Set model to evaluate mode

#             running_loss = 0.0
#             running_corrects = 0

#             # Iterate over data.
#             for inputs, labels in dataloaders[phase]:
#                 inputs = inputs.to(device)
#                 labels = labels.to(device)

#                 # zero the parameter gradients
#                 optimizer.zero_grad()

#                 # forward
#                 # track history if only in train
#                 with torch.set_grad_enabled(phase == 'train'):
#                     outputs = model(inputs)
#                     _, preds = torch.max(outputs, 1)
#                     loss = criterion(outputs, labels)

#                     # backward + optimize only if in training phase
#                     if phase == 'train':
#                         loss.backward()
#                         optimizer.step()

#                 # statistics
#                 running_loss += loss.item() * inputs.size(0)
#                 running_corrects += torch.sum(preds == labels.data)
#             if phase == 'train':
#                 scheduler.step()

#             epoch_loss = running_loss / dataset_sizes[phase]
#             epoch_acc = running_corrects.double() / dataset_sizes[phase]

#             print('{} Loss: {:.4f} Acc: {:.4f}'.format(
#                 phase, epoch_loss, epoch_acc))

#             # deep copy the model
#             if phase == 'val' and epoch_acc > best_acc:
#                 best_acc = epoch_acc
#                 best_model_wts = copy.deepcopy(model.state_dict())

#         print()

#     time_elapsed = time.time() - since
#     print('Training complete in {:.0f}m {:.0f}s'.format(
#         time_elapsed // 60, time_elapsed % 60))
#     print('Best val Acc: {:4f}'.format(best_acc))

#     # load best model weights
#     model.load_state_dict(best_model_wts)
#     return model


# model_conv = torchvision.models.resnet18(pretrained=True)
# for param in model_conv.parameters():
#     param.requires_grad = False

# # Parameters of newly constructed modules have requires_grad=True by default
# num_ftrs = model_conv.fc.in_features
# model_conv.fc = nn.Linear(num_ftrs, 2)

# model_conv = model_conv.to(device)

# criterion = nn.CrossEntropyLoss()

# # Observe that only parameters of final layer are being optimized as
# # opposed to before.
# optimizer_conv = optim.SGD(model_conv.fc.parameters(), lr=0.001, momentum=0.9)

# # Decay LR by a factor of 0.1 every 7 epochs
# exp_lr_scheduler = lr_scheduler.StepLR(optimizer_conv, step_size=7, gamma=0.1)

# model_conv = train_model(model_conv, criterion, optimizer_conv,
#                          exp_lr_scheduler, num_epochs=25)
