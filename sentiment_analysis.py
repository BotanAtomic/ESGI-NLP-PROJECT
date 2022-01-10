from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax

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

task = 'sentiment'
MODEL = f"cardiffnlp/twitter-roberta-base-{task}"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = TFAutoModelForSequenceClassification.from_pretrained(MODEL)

# tokenizer.save_pretrained(MODEL)
# model.save_pretrained(MODEL)

scores_map = {}

i = 0
for _, tweet in tweets.iterrows():
    text = preprocess(tweet['content'])
    encoded_input = tokenizer(text, return_tensors='tf')
    output = model(encoded_input)
    scores = output[0][0].numpy()
    scores = softmax(scores)

    scores_map[tweet['id']] = normalize_score(*scores)

    if i % 1000 == 0:
        print(f'Progression: {i} / {len(tweets)}')

    i += 1


