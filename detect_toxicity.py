# -*- coding: utf-8 -*-
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import pandas as pd 
import pickle
import numpy as np

def det_tox(text):
    """
        det_tox takes an array of text input and predicts whether it contains
        toxic/insulting content.
        Returns a list containing tags that state the type of offensive content
        predicted. Null if none were found.
        
        inp: list or list-like of text. 
        out: list of tags associated with type of abusive language if found. 
    """
    my_model = load_model('detect_toxicity.h5')    
        
    #tokenized_test = format_inp(list_sentences_test)
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    
    handle.close()
    tokenized_inp = tokenizer.texts_to_sequences(text)
    X = pad_sequences(tokenized_inp, maxlen=200)
    
    preds = my_model.predict(X)
    class_label = pd.read_csv('class_label.csv')
    class_label = class_label.values.tolist()
    pred_f = np.where(preds > 0.5, 1, 0)
    p_n = []
    for p in pred_f:
        indx = [i for i,x in enumerate(p) if x == 1]
        p_n.append([class_label[i] for i in indx])

    return p_n

from get_tweets import get_tweets

search_words = '#Trump'
date_since = '2019-05-01'

tweets = get_tweets(search_words, date_since, 15)   
pred = det_tox(tweets)     

