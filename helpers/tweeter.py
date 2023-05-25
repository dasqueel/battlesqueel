import tweepy
import datetime
import pytz
from dateutil.parser import *
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN_KEY = os.getenv('ACCESS_TOKEN_KEY')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

def cleanTweetText(tweetTxt):
    words = tweetTxt.split(' ')
    words = list(filter(lambda a: a != '', words))

    cleanTweetList = []

    for word in words:
        try:
            if word[0] != '@' and 'https://t.co' not in word: cleanTweetList.append(word)
        except Exception as e: print(e)

    cleanTweet = ' '.join(cleanTweetList)

    return cleanTweet

def getTeamTweets(beatWriters):
    allTweets = []

    for user in beatWriters:
        try:
            userTweets = api.user_timeline(screen_name=user, include_rts=False, exclude_replies=False, count=10)
            for tweet in userTweets:
                tweetUrls = []
                for url in tweet.entities['urls']: tweetUrls.append(url['url'])
            
                allTweets.append({'tweet': cleanTweetText(tweet.text), 'created_at': tweet.created_at, 'author': tweet.user.name, 'urls': tweetUrls})


        except Exception as e:
            print(e)
            print('couldnt find tweets for: ', user)

    allTweets.sort(key=lambda tweet: tweet['created_at'], reverse=True)
    now = datetime.datetime.now()

    # get mins ago for tweets
    for tweet in allTweets:
        fmt = '%Y-%m-%d %H:%M:%S'
        tweetTime = tweet['created_at']
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        d1 = datetime.datetime.strptime(str(tweetTime)[:-6], fmt)
        d2 = datetime.datetime.strptime(str(now)[:-13], fmt)
        minsAgo = (d2-d1).total_seconds()/60
        tweet['minsAgo'] = int(round(minsAgo))

    return allTweets