import snscrape.modules.twitter as sntwitter
from datetime import datetime
import os
import csv


def scrap(query, file):
    print(query)
    items = sntwitter.TwitterSearchScraper(query).get_items()

    try:
        os.remove(file)
    except Exception:
        print("No file to remove")

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

            if i % 500 == 0:
                print(i, "tweets downloaded")

            if i >= 10_000:
                break


QUERIES = {
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

for query_key in QUERIES:
    keywords = " ".join(QUERIES[query_key])
    query = f"{keywords} lang:en since:2021-09-28 until:2021-11-28"
    scrap(query, f"tweets/{query_key}.csv")
