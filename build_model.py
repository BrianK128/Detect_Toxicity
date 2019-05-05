# -*- coding: utf-8 -*-
import pandas as pd

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Input, LSTM, Embedding, Dropout
from keras.layers import GlobalMaxPool1D
from keras.models import Model

# load train and test files.
train = pd.read_csv('../Data/input/train.csv')
test = pd.read_csv('../Data/input/test.csv')

# look at training set.
train.head()

class_label = list(train)[2:]
train['none'] = 1-train[class_label].max(axis=1)
train.describe()

# fill blank labels with 'unknown'
COMMENT = 'comment_text'
train[COMMENT].fillna("unknown", inplace=True)
test[COMMENT].fillna("unknown", inplace=True)

# split training set into data and tag
y = train[class_label].values
list_sentences_train = train[COMMENT]
list_sentences_test = test[COMMENT]

# tokenize comments.
max_features = 20000
tokenizer = Tokenizer(num_words=max_features)
tokenizer.fit_on_texts(list(list_sentences_train))
list_tokenized_train = tokenizer.texts_to_sequences(list_sentences_train)
list_tokenized_test = tokenizer.texts_to_sequences(list_sentences_test)

# pad sentences to be uniform length for input
maxlen = 200
X_t = pad_sequences(list_tokenized_train, maxlen=maxlen)
X_te = pad_sequences(list_tokenized_test, maxlen=maxlen)

# construct model
# input should be of length maxlen. 
inp = Input(shape=(maxlen, ))
# tuneable parameter. embedding layer.
embed_size = 128
x = Embedding(max_features, embed_size)(inp)
# feed this tensor into the LSTM layer. set LSTM to produce output with dim 60
# and return whole unrolled sequence of results.
x = LSTM(60, return_sequences=True, name='lstm_layer')(x)
# use global max pooling layer to reduce dimensionality of data. reshape 
x = GlobalMaxPool1D()(x)
# set dropout layer to drop out 10% of the nodes. This is indiscriminately disabled
# to force next layer to handle representation of missing data. could result in better generalization.
x = Dropout(0.1)(x)
# connect output of drop out layer to densely connected layer and pass through a ReLU function.
x = Dense(50, activation="relu")(x)
# feed output into dropout again..
x = Dropout(0.1)(x)
# finally, feed output into a sigmoid layer. (binary classification for each label.)
x = Dense(6, activation="sigmoid")(x)
# define inputs outputs and configure learning process.
model = Model(inputs=inp, outputs=x)
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
# 32 sentences per batch. 90/10 for validation set. 
batch_size = 32
epochs = 2
model.fit(X_t, y, batch_size=batch_size, epochs=epochs, validation_split=0.1)
