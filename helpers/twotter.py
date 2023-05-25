import twitter
from pymongo import MongoClient
from dateutil.parser import *
import datetime
import pytz
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

# Accessing variables.
TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN_KEY = os.getenv('ACCESS_TOKEN_KEY')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

api = twitter.Api(consumer_key=TWITTER_CONSUMER_KEY,
                  consumer_secret=TWITTER_CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN_KEY,
                  access_token_secret=ACCESS_TOKEN_SECRET)


def getTeamTweets(beatWriters):
    tweets = []
    for user in beatWriters:
        try:
            statuses = api.GetUserTimeline(
                screen_name=user, include_rts=False, count=15)
            for s in statuses[::-1]:
                urls = []
                for url in s.urls:
                    urls.append(url.url)
                tweets.append({'tweet': s.text, 'created_at': parse(
                    s.created_at), 'author': s.user.name, 'urls': urls})

        except:
            print('couldnt find tweets for: ', user)

    tweets.sort(key=lambda item: item['created_at'], reverse=True)
    now = datetime.datetime.now()

    # get mins ago for tweets
    for tweet in tweets:
        fmt = '%Y-%m-%d %H:%M:%S'
        tweetTime = tweet['created_at']
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        d1 = datetime.datetime.strptime(str(tweetTime)[:-6], fmt)
        d2 = datetime.datetime.strptime(str(now)[:-13], fmt)
        minsAgo = (d2-d1).total_seconds()/60
        tweet['minsAgo'] = int(round(minsAgo))

    return tweets
