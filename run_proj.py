# -*- coding: utf-8 -*-
from get_tweets import get_tweets
from detect_toxicity import det_tox

search_words = 'idiot'
date_since = '2019-05-01'
count = 15
tweets = get_tweets(search_words, date_since, count)   
pred = det_tox(tweets)     

# print out toxic tweets and labels.
for p in range(len(pred)):
    if pred[p]:
        print('\n Tweet number: ', p)
        print('Tweet Content: ', tweets[p])
        print('Toxic labels: ', pred[p])
        
