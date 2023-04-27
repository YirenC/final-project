import torch.nn as nn
import torch
from sklearn.neighbors import NearestNeighbors
import numpy as np


class MelSpectrogramClassifier(nn.Module):

    def __init__(self):
        super(MelSpectrogramClassifier, self).__init__()
        self.conv1 = nn.Conv2d(1,
                               32,
                               kernel_size=(3, 3),
                               stride=(1, 1),
                               padding=(1, 1))
        self.max_pool1 = nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))
        self.conv2 = nn.Conv2d(32,
                               64,
                               kernel_size=(3, 3),
                               stride=(1, 1),
                               padding=(1, 1))
        self.max_pool2 = nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))
        self.flatten = nn.Flatten()
        self.dense1 = nn.Linear(661504, 128)
        self.dropout = nn.Dropout(0.5)
        self.dense2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = nn.functional.relu(x)
        x = self.max_pool1(x)
        x = self.conv2(x)
        x = nn.functional.relu(x)
        x = self.max_pool2(x)
        x = self.flatten(x)
        x = self.dense1(x)
        x = nn.functional.relu(x)
        x = self.dropout(x)
        x = self.dense2(x)
        return x


# Create an instance of the model
classify_model = MelSpectrogramClassifier()

# Load the trained model parameters
classify_model.load_state_dict(
    torch.load('./recommender/classify_model.pth',
               map_location=torch.device('cpu')))
classify_model.eval()

music_features = np.load('./recommender/music_features.npy', allow_pickle=True)
recommend_model = NearestNeighbors(
    n_neighbors=5, algorithm='ball_tree').fit(music_features).kneighbors
