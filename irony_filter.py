
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax
import pickle

from utils import load_tweets


def normalize_score(negative, neutral, positive):
    return ((positive + neutral / 2) * 2) - 1 if positive > negative else -((negative + neutral / 2) * 2) + 1


def preprocess(text):
    new_text = []

    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)


tweets = load_tweets("tweets/*.csv")

task = 'irony'
MODEL = f"cardiffnlp/twitter-roberta-base-{task}"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = TFAutoModelForSequenceClassification.from_pretrained(MODEL)

# tokenizer.save_pretrained(MODEL)
# model.save_pretrained(MODEL)

irony_map = {}

batch_size = 32
batches = np.array_split(tweets, len(tweets) // batch_size)

i = 0
for batch in batches:
    ids = batch['id'].values
    texts = batch['content'].map(lambda x: preprocess(x)).values

    encoded_input = tokenizer(list(texts), padding=True, truncation=True, return_tensors='tf')

    output = model(encoded_input)
    scores = output[0].numpy()
    scores = softmax(scores)

    for idx, score in enumerate(scores):
        irony = score[1]
        irony_map[ids[idx]] = irony

    i += 1

    if i % 1000 == 0:
        print(f'Progression: {i} / {len(tweets)}')

with open('irony.pkl', 'wb') as file:
    pickle.dump(irony_map, file, pickle.HIGHEST_PROTOCOL)
