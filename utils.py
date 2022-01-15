import glob
import pickle

import pandas as pd
import os

PLAYERS = {
    "Chiellini": ["Chiellini"],
    "De Bruyne": ["De Bruyne"],
    "Ruben Dias": ["Ruben Dias"],
    "Donnarumma": ["Donnarumma"],
    "Fernandes": ["Fernandes"],
    "Foden": ["Foden"],
    "Haaland": ["Haaland"],
    "Jorginho": ["Jorginho"],
    "Kane": ["Harry Kane", "Kane"],
    "Kante": ["N'Golo Kante", "Kante", "Ngolo Kante"],
    "Kjaer": ["Kjaer"],
    "Lewandowski": ["Lewandowski"],
    "Lukaku": ["Lukaku"],
    "Mahrez": ["Mahrez"],
    "Martinez": ["Lautaro Martinez"],
    "Mbappe": ["Mbappe", "M'bappe"],
    "Messi": ["Messi"],
    "Modric": ["Modric"],
    "Moreno": ["Moreno"],
    "Mount": ["Mason Mount"],
    "Neymar": ["Neymar"],
    "Pedri": ["Pedri"],
    "Ronaldo": ["Ronaldo", "CR7"],
    "Salah": ["Mohammed Salah", "Salah", "Mohamed Salah"],
    "Sterling": ["Sterling"],
    "Suarez": ["Suarez"]
}


def load_tweets(base_path, columns=None):
    if columns is None:
        columns = ['id', 'time', 'retweet_count', 'content', 'player']

    tweets_batch = []
    for file in glob.glob(base_path):
        current_data = pd.read_csv(file, sep=";")
        current_data['player'] = file.split(os.path.sep)[-2].split(".csv")[0]
        tweets_batch.append(current_data)

    data = pd.concat(tweets_batch)
    data = data[columns]
    data.drop_duplicates(subset=['id'], inplace=True, keep=False)
    return data


def load_scores(path):
    with open(path, 'rb') as file:
        return pickle.load(file)


def load_irony_probabilities(path):
    with open(path, 'rb') as file:
        return pickle.load(file)
