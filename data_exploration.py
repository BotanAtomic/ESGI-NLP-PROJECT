import utils

tweets = utils.load_tweets("tweets/*.csv")

scores = utils.load_scores("scores.pkl")

irony_map = utils.load_scores("irony.pkl")

tweets.drop_duplicates(subset=['id'], inplace=True)

print(len(tweets))

print(len(scores))

print(len(irony_map))

