import snscrape.modules.twitter as sntwitter
from datetime import datetime, date, timedelta
import os
import csv

from utils import PLAYERS


def scrap(query, file, replace=True):
    items = sntwitter.TwitterSearchScraper(query).get_items()

    if not replace and os.path.exists(file):
        print('Skip', query)
        return

    try:
        os.remove(file)
    except Exception:
        pass

    with open(file, mode='w', newline='') as file:
        csv_writer = csv.writer(file, delimiter=';')

        header = ['id', 'time', 'username', 'follower_count', 'friend_count', 'user_verified',
                  'retweet_count', 'quote_count', 'like_count', 'reply_count', 'content']

        csv_writer.writerow(header)
        i = 0
        for tweet in items:
            user = tweet.user

            features = [
                tweet.id,
                int(datetime.timestamp(tweet.date) * 1000),
                user.username,
                user.followersCount, user.friendsCount, user.verified,
                tweet.retweetCount, tweet.quoteCount, tweet.likeCount, tweet.replyCount,
                tweet.content.encode('utf-8')
            ]
            csv_writer.writerow(features)
            i += 1

            if i >= 1000 - 1:
                break

    print(query, ": done with", i, "tweets")


start_date = date(2021, 9, 28)
end_date = date(2021, 11, 28)
delta = end_date - start_date

RETRY = ["Kante"]

for query_key in PLAYERS:

    if not os.path.exists(f"tweets/{query_key}"):
        os.mkdir(f"tweets/{query_key}")

    if query_key not in RETRY:
        continue

    keywords = " OR ".join(map(lambda x: f"\"{x}\"", PLAYERS[query_key]))
    for i in range(delta.days):
        query = f"{keywords} lang:en since:{start_date + timedelta(days=i)} until:{start_date + timedelta(days=i + 1)}"
        scrap(query, f"tweets/{query_key}/{i}.csv", False)
