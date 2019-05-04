# -*- coding: utf-8 -*-
import tweepy as tw
from twitter_API_auth import api

def get_tweets(search_words, date_since, cnt):
    tweets = tw.Cursor(api.search,
                   q=search_words,
                   lang="en",
                   since=date_since).items(cnt)
    
    tweets_list = [tweet.text for tweet in tweets]

    return tweets_list

# example:
# define search term and date_since and count as variables.
search_words = '#Trump'
date_since = '2019-05-01'
cnt = 15
tweets = get_tweets(search_words, date_since, cnt)
