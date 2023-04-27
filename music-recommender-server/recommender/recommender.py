import torch
import librosa
import numpy as np
from recommender.model import classify_model, recommend_model
import os


class Recommender:

    def __init__(self) -> None:
        self.classify_model = classify_model
        self.recommend_model = recommend_model
        self.id_to_label = {
            0: 'blues',
            1: 'classical',
            2: 'country',
            3: 'disco',
            4: 'hiphop',
            5: 'jazz',
            6: 'metal',
            7: 'pop',
            8: 'reggae',
            9: 'rock'
        }
        self.library = np.load('./recommender/music_features.npy',
                               allow_pickle=True)
        self.musics = []
        for root, dirs, files in os.walk('./recommender/genres'):
            for file in files:
                file_path = os.path.join(root, file)
                self.musics.append(file_path)

    def classify(self, path_to_audio) -> str:
        # Load an audio file and extract its Mel spectrogram
        signal, sr = librosa.load(path_to_audio, sr=22050)
        mel_spectrogram = librosa.feature.melspectrogram(y=signal,
                                                         sr=sr,
                                                         n_fft=2048,
                                                         hop_length=512,
                                                         n_mels=128)
        mel_spectrogram = librosa.util.fix_length(mel_spectrogram, size=1292)

        # Convert the Mel spectrogram to a PyTorch tensor
        mel_spectrogram = np.expand_dims(mel_spectrogram, axis=0)
        mel_spectrogram = torch.from_numpy(mel_spectrogram).float().unsqueeze(
            0)

        # Classify the audio file
        with torch.no_grad():
            prediction = self.classify_model(mel_spectrogram)
            genre = self.id_to_label[prediction.argmax().item()]

        # Convert the Mel spectrogram to a feature vector
        features = mel_spectrogram.reshape(1, -1)

        _, indices = self.recommend_model(features)
        recommend_list = [self.musics[i] for i in indices[0]]
        recommend_list = [name.split('\\')[-1] for name in recommend_list]

        return genre, recommend_list


if __name__ == '__main__':
    recommendation_engine = Recommender()
    genre, recommend_list = recommendation_engine.classify(
        './upload_audio_file')
    print(genre)
    print(recommend_list)
