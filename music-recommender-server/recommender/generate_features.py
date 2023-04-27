import librosa
import numpy as np
from pathlib import Path
import os

# Set paths
data_dir = Path('./genres')
music_features_path = Path('./music_features.npy')


# Create a function to extract the features of a song
def extract_features(song_path):
    signal, sr = librosa.load(song_path, sr=22050)
    mel_spectrogram = librosa.feature.melspectrogram(y=signal,
                                                     sr=sr,
                                                     n_fft=2048,
                                                     hop_length=512,
                                                     n_mels=128)
    mel_spectrogram = librosa.util.fix_length(mel_spectrogram, size=1292)
    return mel_spectrogram.flatten()


# Load the dataset and extract the features
all_features = []
for root, dirs, files in os.walk(data_dir):
    for file in files:
        file_path = os.path.join(root, file)
        features = extract_features(file_path)
        label = os.path.basename(root)
        all_features.append(features.squeeze().flatten())

# Save the features to a numpy array
all_features = np.array(all_features)
all_features = all_features.reshape(len(all_features), -1)  # 添加这一行
np.save(music_features_path, all_features)
