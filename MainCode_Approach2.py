# -*- coding: utf-8 -*-
"""MJAhmadi_NNDL_HW2_Q2_Method2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DopIWJ5wYUrQD9P2U6yjp1cnNjC4910V
"""

!pip install --upgrade --no-cache-dir gdown
!gdown 1JwIyR97fXRfaciFjm4NLualTzq2XaDTg

import zipfile
zip_file_path = '/content/archive.zip'
folder_path = '/content/Dataset'
# Extract the zip file to the specified folder
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(folder_path)

import os
file_path = "/content/archive.zip"
if os.path.exists(file_path):
    os.remove(file_path)
    print(f"{file_path} has been deleted successfully.")
else:
    print(f"{file_path} does not exist.")

import os

# Define the path to the parent folder
parent_folder_path = "/content/Dataset"

# Recursively iterate through all subfolders and files in the parent folder
for dirpath, dirnames, filenames in os.walk(parent_folder_path):
    # Get the number of JPEG files in the current directory
    jpeg_count = sum(1 for filename in filenames if filename.lower().endswith('.jpeg'))
    
    # Print out the results for the current directory
    if jpeg_count > 0:
        # Get the relative path to the current directory
        relative_path = os.path.relpath(dirpath, parent_folder_path)
        
        # Print out the results
        print(f"{jpeg_count} (.jpeg) files are in {os.path.join(parent_folder_path, relative_path)}")

import os
import shutil
from torch.utils.data import Dataset, DataLoader
from torchvision.datasets.folder import default_loader

# Set the path to your input folder here
input_folder_path = "/content/Dataset/chest_xray/chest_xray"

# Define the classes in your dataset
classes = ["NORMAL", "PNEUMONIA"]

# Define the path to the output folder where you want to save the combined data
output_folder_path = os.path.join(input_folder_path, "AllData")

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# Loop through the train, test, and val folders
for split in ["train", "test", "val"]:
    split_folder_path = os.path.join(input_folder_path, split)

    # Loop through the NORMAL and PNEUMONIA folders in each split folder
    for class_name in classes:
        class_folder_path = os.path.join(split_folder_path, class_name)

        # Loop through the image files in each class folder and copy them to the output folder
        for file_name in os.listdir(class_folder_path):
            if file_name.endswith(".jpeg"):
                src_path = os.path.join(class_folder_path, file_name)
                dst_path = os.path.join(output_folder_path, class_name, file_name)

                # Create the class folder in the output folder if it doesn't exist
                if not os.path.exists(os.path.join(output_folder_path, class_name)):
                    os.makedirs(os.path.join(output_folder_path, class_name))

                # Copy the image file to the output folder
                shutil.copyfile(src_path, dst_path)

# Define a custom PyTorch dataset to load the combined data
class CustomDataset(Dataset):
    def __init__(self, root, classes, transform=None, loader=default_loader):
        self.root = root
        self.classes = classes
        self.transform = transform
        self.loader = loader
        self.samples = []

        # Loop through the NORMAL and PNEUMONIA classes and their respective image folders in the output folder
        for class_name in classes:
            class_folder_path = os.path.join(root, class_name)
            for file_name in os.listdir(class_folder_path):
                if file_name.endswith(".jpeg"):
                    self.samples.append((os.path.join(class_folder_path, file_name), classes.index(class_name)))

    def __getitem__(self, index):
        path, target = self.samples[index]
        sample = self.loader(path)
        if self.transform is not None:
            sample = self.transform(sample)
        return sample, target

    def __len__(self):
        return len(self.samples)

# Load the combined data using the custom PyTorch dataset
dataset = CustomDataset(output_folder_path, classes)

# Use the PyTorch DataLoader to create batches of data for training/testing
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

import os
import shutil
import random

# Set the path to the "FinalDataset" folder
data_dir = "/content/Dataset/chest_xray/chest_xray/AllData"

# Set the path to the output directory
output_dir = "/content/FinalDatasetTVT2"

# Set the train/validation/test split ratios
train_ratio = 0.6
val_ratio = 0.2
test_ratio = 0.2

# Create the output directories
os.makedirs(os.path.join(output_dir, "train", "NORMAL"), exist_ok=True)
os.makedirs(os.path.join(output_dir, "train", "PNEUMONIA"), exist_ok=True)
os.makedirs(os.path.join(output_dir, "val", "NORMAL"), exist_ok=True)
os.makedirs(os.path.join(output_dir, "val", "PNEUMONIA"), exist_ok=True)
os.makedirs(os.path.join(output_dir, "test", "NORMAL"), exist_ok=True)
os.makedirs(os.path.join(output_dir, "test", "PNEUMONIA"), exist_ok=True)

# Get the list of image files in each class folder
normal_files = os.listdir(os.path.join(data_dir, "NORMAL"))
pneumonia_files = os.listdir(os.path.join(data_dir, "PNEUMONIA"))

# Shuffle the lists to randomize the order
random.shuffle(normal_files)
random.shuffle(pneumonia_files)

# Calculate the number of images for each split
num_normal = len(normal_files)
num_pneumonia = len(pneumonia_files)
num_train_normal = int(num_normal * train_ratio)
num_train_pneumonia = int(num_pneumonia * train_ratio)
num_val_normal = int(num_normal * val_ratio)
num_val_pneumonia = int(num_pneumonia * val_ratio)
num_test_normal = int(num_normal * test_ratio)
num_test_pneumonia = int(num_pneumonia * test_ratio)

# Copy the image files to the output directories for each split
for i, file in enumerate(normal_files):
    if i < num_train_normal:
        shutil.copy(os.path.join(data_dir, "NORMAL", file), os.path.join(output_dir, "train", "NORMAL"))
    elif i < num_train_normal + num_val_normal:
        shutil.copy(os.path.join(data_dir, "NORMAL", file), os.path.join(output_dir, "val", "NORMAL"))
    else:
        shutil.copy(os.path.join(data_dir, "NORMAL", file), os.path.join(output_dir, "test", "NORMAL"))
for i, file in enumerate(pneumonia_files):
    if i < num_train_pneumonia:
        shutil.copy(os.path.join(data_dir, "PNEUMONIA", file), os.path.join(output_dir, "train", "PNEUMONIA"))
    elif i < num_train_pneumonia + num_val_pneumonia:
        shutil.copy(os.path.join(data_dir, "PNEUMONIA", file), os.path.join(output_dir, "val", "PNEUMONIA"))
    else:
        shutil.copy(os.path.join(data_dir, "PNEUMONIA", file), os.path.join(output_dir, "test", "PNEUMONIA"))

import os
import shutil
import random

# Set the path to the "FinalDataset" folder
data_dir = "/content/Dataset/chest_xray/chest_xray/AllData"

# Set the path to the output directory
output_dir = "/content/FinalDatasetTVT4"

# Set the train/validation/test split ratios
train_ratio = 0.6
val_ratio = 0.2
test_ratio = 0.2

# Create the output directories
os.makedirs(os.path.join(output_dir, "train", "0"), exist_ok=True)
os.makedirs(os.path.join(output_dir, "train", "1"), exist_ok=True)
os.makedirs(os.path.join(output_dir, "val", "0"), exist_ok=True)
os.makedirs(os.path.join(output_dir, "val", "1"), exist_ok=True)
os.makedirs(os.path.join(output_dir, "test", "0"), exist_ok=True)
os.makedirs(os.path.join(output_dir, "test", "1"), exist_ok=True)

# Get the list of image files in each class folder
normal_files = os.listdir(os.path.join(data_dir, "NORMAL"))
pneumonia_files = os.listdir(os.path.join(data_dir, "PNEUMONIA"))

# Shuffle the lists to randomize the order
random.shuffle(normal_files)
random.shuffle(pneumonia_files)

# Calculate the number of images for each split
num_normal = len(normal_files)
num_pneumonia = len(pneumonia_files)
num_train_normal = int(num_normal * train_ratio)
num_train_pneumonia = int(num_pneumonia * train_ratio)
num_val_normal = int(num_normal * val_ratio)
num_val_pneumonia = int(num_pneumonia * val_ratio)
num_test_normal = int(num_normal * test_ratio)
num_test_pneumonia = int(num_pneumonia * test_ratio)

# Copy the image files to the output directories for each split
for i, file in enumerate(normal_files):
    if i < num_train_normal:
        shutil.copy(os.path.join(data_dir, "NORMAL", file), os.path.join(output_dir, "train", "0"))
    elif i < num_train_normal + num_val_normal:
        shutil.copy(os.path.join(data_dir, "NORMAL", file), os.path.join(output_dir, "val", "0"))
    else:
        shutil.copy(os.path.join(data_dir, "NORMAL", file), os.path.join(output_dir, "test", "0"))
for i, file in enumerate(pneumonia_files):
    if i < num_train_pneumonia:
        shutil.copy(os.path.join(data_dir, "PNEUMONIA", file), os.path.join(output_dir, "train", "1"))
    elif i < num_train_pneumonia + num_val_pneumonia:
        shutil.copy(os.path.join(data_dir, "PNEUMONIA", file), os.path.join(output_dir, "val", "1"))
    else:
        shutil.copy(os.path.join(data_dir, "PNEUMONIA", file), os.path.join(output_dir, "test", "1"))

from PIL import Image
import os

# Set the path to the directory containing the images
directory = '/content/FinalDatasetTVT2/'

# Loop through all the subdirectories and files in the directory
for root, dirs, files in os.walk(directory):
    for filename in files:
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            # Open the image and convert it to RGB format
            img = Image.open(os.path.join(root, filename)).convert('RGB')
            
            # Save the image back to the same file
            img.save(os.path.join(root, filename))

import torch
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm.notebook import tqdm

import matplotlib.pyplot as plt 
import torch.nn.functional as F 
import torch 
import numpy as np 

def show_image(image,label,get_denormalize = True):
    
    image = image.permute(1,2,0)
    mean = torch.FloatTensor([0.485, 0.456, 0.406])
    std = torch.FloatTensor([0.229, 0.224, 0.225])
    
    if get_denormalize == True:
        image = image*std + mean
        image = np.clip(image,0,1)
        plt.imshow(image)
        plt.title(label)
        
    else: 
        plt.imshow(image)
        plt.title(label)

def show_grid(image,title = None):
    
    image = image.permute(1,2,0)
    mean = torch.FloatTensor([0.485, 0.456, 0.406])
    std = torch.FloatTensor([0.229, 0.224, 0.225])
    
    image = image*std + mean
    image = np.clip(image,0,1)
    
    plt.figure(figsize=[15, 15])
    plt.imshow(image)
    if title != None:
        plt.title(title)


def accuracy(y_pred,y_true):
    y_pred = F.softmax(y_pred,dim = 1)
    top_p,top_class = y_pred.topk(1,dim = 1)
    equals = top_class == y_true.view(*top_class.shape)
    return torch.mean(equals.type(torch.FloatTensor))


def view_classify(image,ps,label):
    
    class_name = ['NORMAL', 'PNEUMONIA']
    classes = np.array(class_name)

    ps = ps.cpu().data.numpy().squeeze()
    
    image = image.permute(1,2,0)
    mean = torch.FloatTensor([0.485, 0.456, 0.406])
    std = torch.FloatTensor([0.229, 0.224, 0.225])
    
    
    image = image*std + mean
    img = np.clip(image,0,1)
    
    fig, (ax1, ax2) = plt.subplots(figsize=(8,12), ncols=2)
    ax1.imshow(img)
    ax1.set_title('Ground Truth : {}'.format(class_name[label]))
    ax1.axis('off')
    ax2.barh(classes, ps)
    ax2.set_aspect(0.1)
    ax2.set_yticks(classes)
    ax2.set_yticklabels(classes)
    ax2.set_title('Predicted Class')
    ax2.set_xlim(0, 1.1)

    plt.tight_layout()

    return None

class CFG:

  epochs =30                              # No. of epochs for training the model
  lr = 0.001                              # Learning rate
  batch_size = 128                         # Batch Size for Dataset

  model_name = 'tf_efficientnet_b2_ns'    # Model name (we are going to import model from timm)
  img_size = 128                          # Resize all the images to be 224 by 224

  # going to be used for loading dataset
  #Data_DIR = "chest_xray"
  #TEST = "test"
  #TRAIN = "train"
  #VAL = "val" 
  train_path='/content/FinalDatasetTVT2/train'
  validate_path='/content/FinalDatasetTVT2/val'
  test_path='/content/FinalDatasetTVT2/test'

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("On which device we are on:{}".format(device))

from torchvision import transforms as T,datasets

CFG.img_size

train_transform = T.Compose([
                             
                             T.Resize(size=(CFG.img_size,CFG.img_size)), # Resizing the image to be 224 by 224
                             T.RandomRotation(degrees=(-30,+30)), #Randomly Rotate Images by +/- 20 degrees, Image argumentation for each epoch
                             T.RandomHorizontalFlip(p=0.5),
                             T.RandomAffine(degrees=30, translate=(0.2, 0.2), shear=0.2, scale=(0.8, 1.2)),
                             T.ToTensor(), #converting the dimension from (height,weight,channel) to (channel,height,weight) convention of PyTorch
                             T.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225]) # Normalize by 3 means 3 StD's of the image net, 3 channels

])

validate_transform = T.Compose([
                             
                             T.Resize(size=(CFG.img_size,CFG.img_size)), # Resizing the image to be 224 by 224
                             #T.RandomRotation(degrees=(-20,+20)), #NO need for validation
                             T.ToTensor(), #converting the dimension from (height,weight,channel) to (channel,height,weight) convention of PyTorch
                             T.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225]) # Normalize by 3 means 3 StD's of the image net, 3 channels

])

test_transform = T.Compose([
                             
                             T.Resize(size=(CFG.img_size,CFG.img_size)), # Resizing the image to be 224 by 224
                             #T.RandomRotation(degrees=(-20,+20)), #NO need for validation
                             T.ToTensor(), #converting the dimension from (height,weight,channel) to (channel,height,weight) convention of PyTorch
                             T.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225]) # Normalize by 3 means 3 StD's of the image net, 3 channels

])

from google.colab import drive
drive.mount('/content/drive')

trainset=datasets.ImageFolder(CFG.train_path,transform=train_transform)
print("Trainset Size:  {}".format(len(trainset)))

validateset=datasets.ImageFolder(CFG.validate_path,transform=validate_transform)
print("validateset Size:  {}".format(len(validateset)))

testset=datasets.ImageFolder(CFG.test_path,transform=test_transform)
print("testset Size:  {}".format(len(testset)))

img,label = trainset[20]
#print(trainset.class_to_idx)

class_name =["NORMAL","PNEUMONIA"]
show_image(img,class_name[label])

img,label = trainset[20]
#print(trainset.class_to_idx)

class_name =["NORMAL","PNEUMONIA"]
show_image(img,class_name[label]) 

# randomly rotated

from torch.utils.data import DataLoader
from torchvision.utils import make_grid

trainloader = DataLoader(trainset,batch_size=CFG.batch_size,shuffle=True)
print("No. of batches in trainloader:{}".format(len(trainloader))) #Trainset Size:  5216 / batch_size: 16 = 326(No. of batches in trainloader) 
print("No. of Total examples:{}".format(len(trainloader.dataset)))

validationloader = DataLoader(validateset,batch_size=CFG.batch_size,shuffle=True)
print("No. of batches in validationloader:{}".format(len(validationloader))) #validationset Size:  16 / batch_size: 16 = 1(No. of batches in validationloader) 
print("No. of Total examples:{}".format(len(validationloader.dataset)))

testloader = DataLoader(testset,batch_size=CFG.batch_size,shuffle=True)
print("No. of batches in testloader:{}".format(len(testloader))) #testset Size:  624 / batch_size: 16 = 39(No. of batches in testloader) 
print("No. of Total examples:{}".format(len(testloader.dataset)))

dataiter = iter(trainloader)
images, labels = dataiter.__next__()

out = make_grid(images, nrow=4)

show_grid(out, title=[class_name[x] for x in labels])

!pip install timm # install PyTorch Image Models

from torch import nn
import torch.nn.functional as F
import timm # PyTorch Image Models

model = timm.create_model(CFG.model_name,pretrained=True) #load pretrained model

model

#let's update the pretarined model:
for param in model.parameters():
  param.requires_grad=False

#orginally, it was:
#(classifier): Linear(in_features=1792, out_features=1000, bias=True)


#we are updating it as a 2-class classifier:
model.classifier = nn.Sequential(
    # nn.Flatten(),
    # nn.AdaptiveAvgPool2d((1, 1)), # GlobalAveragePooling2D equivalent
    nn.Linear(in_features=1408, out_features=128),
    nn.ReLU(),
    nn.Dropout(p=0.3),
    nn.Linear(in_features=128, out_features=64),
    nn.ReLU(),
    nn.Dropout(p=0.2),
    nn.Linear(in_features=64, out_features=2)
)


model

# after updatingnow it becomes:
#(classifier): Sequential(
#    (0): Linear(in_features=1792, out_features=625, bias=True)
#    (1): ReLU()
#    (2): Dropout(p=0.3, inplace=False)
#    (3): Linear(in_features=625, out_features=256, bias=True)
#    (4): ReLU()
#    (5): Linear(in_features=256, out_features=2, bias=True)
#  )

from torchsummary import  summary
model.to(device) # move the model to GPU
summary(model,input_size=(3,128,128))

class PneumoniaTrainer():
    
    def __init__(self, criterion=None, optimizer=None, scheduler=None):
        self.criterion = criterion
        self.optimizer = optimizer
        self.scheduler = scheduler
        
        self.train_losses = []
        self.train_accs = []
        self.val_losses = []
        self.val_accs = []
        
    def train_batch_loop(self, model, trainloader):
        train_loss = 0.0
        train_acc = 0.0

        for images, labels in tqdm(trainloader): 
            images = images.to(device)
            labels = labels.to(device)

            logits = model(images)
            loss = self.criterion(logits, labels)

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            train_loss += loss.item()
            train_acc += accuracy(logits, labels)

        return train_loss / len(trainloader), train_acc / len(trainloader) 

    
    def valid_batch_loop(self, model, validloader):
        valid_loss = 0.0
        valid_acc = 0.0

        with torch.no_grad():
            for images, labels in tqdm(validloader):
                images = images.to(device)
                labels = labels.to(device)

                logits = model(images)
                loss = self.criterion(logits, labels)

                valid_loss += loss.item()
                valid_acc += accuracy(logits, labels)

        return valid_loss / len(validloader), valid_acc / len(validloader)
            
        
    def fit(self, model, trainloader, validloader, epochs):
        valid_min_loss = np.Inf 
        
        for epoch in range(epochs):
            model.train() 
            avg_train_loss, avg_train_acc = self.train_batch_loop(model, trainloader)
            
            model.eval() 
            avg_valid_loss, avg_valid_acc = self.valid_batch_loop(model, validloader)
            
            self.train_losses.append(avg_train_loss)
            self.train_accs.append(avg_train_acc)
            self.val_losses.append(avg_valid_loss)
            self.val_accs.append(avg_valid_acc)
            
            if avg_valid_loss <= valid_min_loss:
                print("Valid_loss decreased {} --> {}".format(valid_min_loss,avg_valid_loss))
                torch.save(model.state_dict(), 'ColabPneumoniaModel.pt')
                valid_min_loss = avg_valid_loss

                
            print("Epoch : {} Train Loss : {:.6f} Train Acc : {:.6f}".format(epoch+1, avg_train_loss, avg_train_acc))
            print("Epoch : {} Valid Loss : {:.6f} Valid Acc : {:.6f}".format(epoch+1, avg_valid_loss, avg_valid_acc))


    def plot_pr_curve(self, model, testloader):
        with torch.no_grad():
            model.eval()
            y_true = []
            y_scores = []
            for images, labels in tqdm(testloader):
                images = images.to(device)
                labels = labels.to(device)

                logits = model(images)
                probs = torch.softmax(logits, dim=1)
                y_true.extend(labels.cpu().numpy())
                y_scores.extend(probs[:, 1].cpu().numpy())

            precision, recall, _ = precision_recall_curve(y_true, y_scores)
            plt.plot(recall, precision, color='b', alpha=0.8)
            plt.xlabel('Recall')
            plt.ylabel('Precision')
            plt.title('PR Curve')
            plt.show()
    
    def plot_roc_curve(self, model, testloader):
        with torch.no_grad():
            model.eval()
            y_true = []
            y_scores = []
            for images, labels in tqdm(testloader):
                images = images.to(device)
                labels = labels.to(device)

                logits = model(images)
                probs = torch.softmax(logits, dim=1)
                y_true.extend(labels.cpu().numpy())
                y_scores.extend(probs[:, 1].cpu().numpy())

            fpr, tpr, _ = roc_curve(y_true, y_scores)
            roc_auc = auc(fpr, tpr)
            plt.plot(fpr, tpr, color='b', alpha=0.8, label='AUC = {:.2f}'.format(roc_auc))
            plt.plot([0, 1], [0, 1], color='r', linestyle='--')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title('ROC Curve')
            plt.legend()
            plt.show()

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(),lr = CFG.lr)

trainer = PneumoniaTrainer(criterion,optimizer)
trainer.fit(model,trainloader,validationloader,epochs = CFG.epochs)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(),lr = CFG.lr)

trainer = PneumoniaTrainer(criterion,optimizer)
trainer.fit(model,trainloader,validationloader,epochs = CFG.epochs)

from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score
import matplotlib.pyplot as plt

train_losses = trainer.train_losses
val_losses = trainer.val_losses
train_accs = trainer.train_accs
val_accs = trainer.val_accs

# Plot losses
plt.plot(train_losses, label='train')
plt.plot(val_losses, label='val')
plt.title('Train/Val Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.savefig('11.pdf')
plt.show()

# Plot accuracies
plt.plot(train_accs, label='train')
plt.plot(val_accs, label='val')
plt.title('Train/Val Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.savefig('21.pdf')
plt.show()

# PR curve
model.load_state_dict(torch.load('/content/ColabPneumoniaModel.pt'))
model.eval()
y_true, y_scores = [], []
with torch.no_grad():
    for images, labels in testloader:
        images = images.to(device)
        labels = labels.to(device)
        logits = model(images)
        probas = torch.softmax(logits, dim=1)
        y_true.extend(labels.cpu().numpy())
        y_scores.extend(probas[:, 1].cpu().numpy())
precision, recall, _ = precision_recall_curve(y_true, y_scores)
pr_auc = average_precision_score(y_true, y_scores)
plt.plot(recall, precision, lw=2, label='PR Curve (area = %0.2f)' % pr_auc)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend(loc="lower right")
plt.savefig('31.pdf')
plt.show()

# ROC curve
fpr, tpr, thresholds = roc_curve(y_true, y_scores)
roc_auc = auc(fpr, tpr)
plt.plot(fpr, tpr, lw=2, label='ROC Curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], '--', color='gray', label='Random Guess')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.savefig('41.pdf')
plt.show()

from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score, precision_score, recall_score, f1_score
import seaborn as sns

# Load the saved model
model.load_state_dict(torch.load('/content/ColabPneumoniaModel.pt'))
model.eval()

# Evaluate the model on the test set
avg_test_loss, avg_test_acc = trainer.valid_batch_loop(model,testloader)
print("Test Loss : {:.6f}".format(avg_test_loss))
print("Test Acc : {:.6f}".format(avg_test_acc))

# Evaluate the model's performance using a confusion matrix
true_labels = []
pred_labels = []

for images, labels in testloader:
    images = images.to(device)
    labels = labels.to(device)
    
    with torch.no_grad():
        logits = model(images)
    
    preds = torch.argmax(logits, dim=1)
    
    true_labels += labels.tolist()
    pred_labels += preds.tolist()

cm = confusion_matrix(true_labels, pred_labels)
sns.heatmap(cm, annot=True, fmt='g')
plt.xlabel('Predicted labels')
plt.ylabel('True labels')

# Save the confusion matrix as a PDF
plt.savefig('confusion_matrix2.pdf', dpi=300, bbox_inches='tight')

# Calculate and print classification report, AUC, precision, recall, and F1 score
target_names = ['Normal', 'Pneumonia']
print(classification_report(true_labels, pred_labels, target_names=target_names))

roc_auc = roc_auc_score(true_labels, pred_labels)
print("AUC : {:.6f}".format(roc_auc))

precision = precision_score(true_labels, pred_labels)
print("Precision : {:.6f}".format(precision))

recall = recall_score(true_labels, pred_labels)
print("Recall : {:.6f}".format(recall))

f1 = f1_score(true_labels, pred_labels)
print("F1 Score : {:.6f}".format(f1))

import torch.nn.functional as F
import matplotlib.pyplot as plt

image, label = testset[300]

ps = model(image.to(device).unsqueeze(0))
ps = F.softmax(ps, dim=1)

view_classify(image, ps, label)

# Save the output as a PNG file
plt.savefig('output1.pdf')
plt.savefig('output1.png')

import torch.nn.functional as F
import matplotlib.pyplot as plt

image, label = testset[320]

ps = model(image.to(device).unsqueeze(0))
ps = F.softmax(ps, dim=1)

view_classify(image, ps, label)

# Save the output as a PNG file
plt.savefig('output2.pdf')
plt.savefig('output2.png')

import torch.nn.functional as F
import matplotlib.pyplot as plt

image, label = testset[5]

ps = model(image.to(device).unsqueeze(0))
ps = F.softmax(ps, dim=1)

view_classify(image, ps, label)

# Save the output as a PNG file
plt.savefig('output3.pdf')
plt.savefig('output3.png')

import torch.nn.functional as F
import matplotlib.pyplot as plt

image, label = testset[8]

ps = model(image.to(device).unsqueeze(0))
ps = F.softmax(ps, dim=1)

view_classify(image, ps, label)

# Save the output as a PNG file
plt.savefig('output4.pdf')
plt.savefig('output4.png')

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(),lr = CFG.lr)

trainer = PneumoniaTrainer(criterion,optimizer)
trainer.fit(model,trainloader,validationloader,epochs = CFG.epochs)

from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score
import matplotlib.pyplot as plt

train_losses = trainer.train_losses
val_losses = trainer.val_losses
train_accs = trainer.train_accs
val_accs = trainer.val_accs

# Plot losses
plt.plot(train_losses, label='train')
plt.plot(val_losses, label='val')
plt.title('Train/Val Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.savefig('11.pdf')
plt.show()

# Plot accuracies
plt.plot(train_accs, label='train')
plt.plot(val_accs, label='val')
plt.title('Train/Val Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.savefig('21.pdf')
plt.show()

# PR curve
model.load_state_dict(torch.load('/content/ColabPneumoniaModel.pt'))
model.eval()
y_true, y_scores = [], []
with torch.no_grad():
    for images, labels in testloader:
        images = images.to(device)
        labels = labels.to(device)
        logits = model(images)
        probas = torch.softmax(logits, dim=1)
        y_true.extend(labels.cpu().numpy())
        y_scores.extend(probas[:, 1].cpu().numpy())
precision, recall, _ = precision_recall_curve(y_true, y_scores)
pr_auc = average_precision_score(y_true, y_scores)
plt.plot(recall, precision, lw=2, label='PR Curve (area = %0.2f)' % pr_auc)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend(loc="lower right")
plt.savefig('31.pdf')
plt.show()

# ROC curve
fpr, tpr, thresholds = roc_curve(y_true, y_scores)
roc_auc = auc(fpr, tpr)
plt.plot(fpr, tpr, lw=2, label='ROC Curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], '--', color='gray', label='Random Guess')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.savefig('41.pdf')
plt.show()

from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score, precision_score, recall_score, f1_score
import seaborn as sns

# Load the saved model
model.load_state_dict(torch.load('/content/ColabPneumoniaModel.pt'))
model.eval()

# Evaluate the model on the test set
avg_test_loss, avg_test_acc = trainer.valid_batch_loop(model,testloader)
print("Test Loss : {:.6f}".format(avg_test_loss))
print("Test Acc : {:.6f}".format(avg_test_acc))

# Evaluate the model's performance using a confusion matrix
true_labels = []
pred_labels = []

for images, labels in testloader:
    images = images.to(device)
    labels = labels.to(device)
    
    with torch.no_grad():
        logits = model(images)
    
    preds = torch.argmax(logits, dim=1)
    
    true_labels += labels.tolist()
    pred_labels += preds.tolist()

cm = confusion_matrix(true_labels, pred_labels)
sns.heatmap(cm, annot=True, fmt='g')
plt.xlabel('Predicted labels')
plt.ylabel('True labels')

# Save the confusion matrix as a PDF
plt.savefig('confusion_matrix2.pdf', dpi=300, bbox_inches='tight')

# Calculate and print classification report, AUC, precision, recall, and F1 score
target_names = ['Normal', 'Pneumonia']
print(classification_report(true_labels, pred_labels, target_names=target_names))

roc_auc = roc_auc_score(true_labels, pred_labels)
print("AUC : {:.6f}".format(roc_auc))

precision = precision_score(true_labels, pred_labels)
print("Precision : {:.6f}".format(precision))

recall = recall_score(true_labels, pred_labels)
print("Recall : {:.6f}".format(recall))

f1 = f1_score(true_labels, pred_labels)
print("F1 Score : {:.6f}".format(f1))

import torch.nn.functional as F
import matplotlib.pyplot as plt

image, label = testset[300]

ps = model(image.to(device).unsqueeze(0))
ps = F.softmax(ps, dim=1)

view_classify(image, ps, label)

# Save the output as a PNG file
plt.savefig('output1.pdf')

import torch.nn.functional as F
import matplotlib.pyplot as plt

image, label = testset[320]

ps = model(image.to(device).unsqueeze(0))
ps = F.softmax(ps, dim=1)

view_classify(image, ps, label)

# Save the output as a PNG file
plt.savefig('output2.pdf')

import torch.nn.functional as F
import matplotlib.pyplot as plt

image, label = testset[5]

ps = model(image.to(device).unsqueeze(0))
ps = F.softmax(ps, dim=1)

view_classify(image, ps, label)

# Save the output as a PNG file
plt.savefig('output3.pdf')

import torch.nn.functional as F
import matplotlib.pyplot as plt

image, label = testset[8]

ps = model(image.to(device).unsqueeze(0))
ps = F.softmax(ps, dim=1)

view_classify(image, ps, label)

# Save the output as a PNG file
plt.savefig('output4.pdf')

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(),lr = CFG.lr)

trainer = PneumoniaTrainer(criterion,optimizer)
trainer.fit(model,trainloader,validationloader,epochs = CFG.epochs)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(),lr = CFG.lr)

trainer = PneumoniaTrainer(criterion,optimizer)
trainer.fit(model,trainloader,validationloader,epochs = CFG.epochs)

from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score
import matplotlib.pyplot as plt

train_losses = trainer.train_losses
val_losses = trainer.val_losses
train_accs = trainer.train_accs
val_accs = trainer.val_accs

# Plot losses
plt.plot(train_losses, label='train')
plt.plot(val_losses, label='val')
plt.title('Train/Val Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.savefig('1.pdf')
plt.show()

# Plot accuracies
plt.plot(train_accs, label='train')
plt.plot(val_accs, label='val')
plt.title('Train/Val Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.savefig('2.pdf')
plt.show()

# PR curve
model.load_state_dict(torch.load('/content/ColabPneumoniaModel.pt'))
model.eval()
y_true, y_scores = [], []
with torch.no_grad():
    for images, labels in testloader:
        images = images.to(device)
        labels = labels.to(device)
        logits = model(images)
        probas = torch.softmax(logits, dim=1)
        y_true.extend(labels.cpu().numpy())
        y_scores.extend(probas[:, 1].cpu().numpy())
precision, recall, _ = precision_recall_curve(y_true, y_scores)
pr_auc = average_precision_score(y_true, y_scores)
plt.plot(recall, precision, lw=2, label='PR Curve (area = %0.2f)' % pr_auc)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend(loc="lower right")
plt.savefig('3.pdf')
plt.show()

# ROC curve
fpr, tpr, thresholds = roc_curve(y_true, y_scores)
roc_auc = auc(fpr, tpr)
plt.plot(fpr, tpr, lw=2, label='ROC Curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], '--', color='gray', label='Random Guess')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.savefig('4.pdf')
plt.show()

model.load_state_dict(torch.load('/content/ColabPneumoniaModel.pt'))
model.eval()

avg_test_loss, avg_test_acc = trainer.valid_batch_loop(model,testloader)


print("Test Loss : {}".format(avg_test_loss))
print("Test Acc : {}".format(avg_test_acc))

from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score, precision_score, recall_score, f1_score
import seaborn as sns

# Load the saved model
model.load_state_dict(torch.load('/content/ColabPneumoniaModel.pt'))
model.eval()

# Evaluate the model on the test set
avg_test_loss, avg_test_acc = trainer.valid_batch_loop(model,testloader)
print("Test Loss : {:.6f}".format(avg_test_loss))
print("Test Acc : {:.6f}".format(avg_test_acc))

# Evaluate the model's performance using a confusion matrix
true_labels = []
pred_labels = []

for images, labels in testloader:
    images = images.to(device)
    labels = labels.to(device)
    
    with torch.no_grad():
        logits = model(images)
    
    preds = torch.argmax(logits, dim=1)
    
    true_labels += labels.tolist()
    pred_labels += preds.tolist()

cm = confusion_matrix(true_labels, pred_labels)
sns.heatmap(cm, annot=True, fmt='g')
plt.xlabel('Predicted labels')
plt.ylabel('True labels')

# Save the confusion matrix as a PDF
plt.savefig('confusion_matrix.pdf', dpi=300, bbox_inches='tight')

# Calculate and print classification report, AUC, precision, recall, and F1 score
target_names = ['Normal', 'Pneumonia']
print(classification_report(true_labels, pred_labels, target_names=target_names))

roc_auc = roc_auc_score(true_labels, pred_labels)
print("AUC : {:.6f}".format(roc_auc))

precision = precision_score(true_labels, pred_labels)
print("Precision : {:.6f}".format(precision))

recall = recall_score(true_labels, pred_labels)
print("Recall : {:.6f}".format(recall))

f1 = f1_score(true_labels, pred_labels)
print("F1 Score : {:.6f}".format(f1))

from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score, precision_score, recall_score, f1_score
import seaborn as sns

# Load the saved model
model.load_state_dict(torch.load('/content/ColabPneumoniaModel.pt'))
model.eval()

# Evaluate the model on the test set
avg_test_loss, avg_test_acc = trainer.valid_batch_loop(model,testloader)
print("Test Loss : {:.6f}".format(avg_test_loss))
print("Test Acc : {:.6f}".format(avg_test_acc))

# Evaluate the model's performance using a confusion matrix
true_labels = []
pred_labels = []

for images, labels in testloader:
    images = images.to(device)
    labels = labels.to(device)
    
    with torch.no_grad():
        logits = model(images)
    
    preds = torch.argmax(logits, dim=1)
    
    true_labels += labels.tolist()
    pred_labels += preds.tolist()

cm = confusion_matrix(true_labels, pred_labels)
sns.heatmap(cm, annot=True, fmt='g')
plt.xlabel('Predicted labels')
plt.ylabel('True labels')

# Save the confusion matrix as a PDF
plt.savefig('confusion_matrix.pdf', dpi=300, bbox_inches='tight')

# Calculate and print classification report, AUC, precision, recall, and F1 score
target_names = ['Normal', 'Pneumonia']
print(classification_report(true_labels, pred_labels, target_names=target_names))

roc_auc = roc_auc_score(true_labels, pred_labels)
print("AUC : {:.6f}".format(roc_auc))

precision = precision_score(true_labels, pred_labels)
print("Precision : {:.6f}".format(precision))

recall = recall_score(true_labels, pred_labels)
print("Recall : {:.6f}".format(recall))

f1 = f1_score(true_labels, pred_labels)
print("F1 Score : {:.6f}".format(f1))

import torch.nn.functional as F

image,label = testset[15]

ps = model(image.to(device).unsqueeze(0))
ps = F.softmax(ps,dim = 1)

view_classify(image,ps,label)

import torch.nn.functional as F

image,label = testset[5]

ps = model(image.to(device).unsqueeze(0))
ps = F.softmax(ps,dim = 1)

view_classify(image,ps,label)

import torch.nn.functional as F

image,label = testset[10]

ps = model(image.to(device).unsqueeze(0))
ps = F.softmax(ps,dim = 1)

view_classify(image,ps,label)

import torch.nn.functional as F

image,label = testset[324]

ps = model(image.to(device).unsqueeze(0))
ps = F.softmax(ps,dim = 1)

view_classify(image,ps,label)

import torch.nn.functional as F
import matplotlib.pyplot as plt

image, label = testset[15]

ps = model(image.to(device).unsqueeze(0))
ps = F.softmax(ps, dim=1)

view_classify(image, ps, label)

# Save the output as a PNG file
plt.savefig('output.png')

import torch.nn.functional as F
import matplotlib.pyplot as plt

image, label = testset[324]

ps = model(image.to(device).unsqueeze(0))
ps = F.softmax(ps, dim=1)

view_classify(image, ps, label)

# Save the output as a PNG file
plt.savefig('output.png')

import torch.nn.functional as F
import matplotlib.pyplot as plt

image, label = testset[15]

ps = model(image.to(device).unsqueeze(0))
ps = F.softmax(ps, dim=1)

view_classify(image, ps, label)

# Save the output as a PNG file
plt.savefig('output.pdf')

import torch.nn.functional as F
import matplotlib.pyplot as plt

image, label = testset[324]

ps = model(image.to(device).unsqueeze(0))
ps = F.softmax(ps, dim=1)

view_classify(image, ps, label)

# Save the output as a PNG file
plt.savefig('output.pdf')