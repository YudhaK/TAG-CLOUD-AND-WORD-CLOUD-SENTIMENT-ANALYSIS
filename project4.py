# -*- coding: utf-8 -*-
"""Project4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JmtNyeiau3yZ8HiD2BOIYtHjqTr_hWEl
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from prettytable import PrettyTable
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

base = 'drive/My Drive/'

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv(base + "DATA.csv", encoding='utf-8')
df = df.reindex(np.random.permutation(df.index))
df['content'] = df['content'].astype(str)

vocabulary_size = 200000
tokenizer = Tokenizer(num_words= 1000)
tokenizer.fit_on_texts(df['content'])

word2index = tokenizer.word_index
index2word = {i:j for i, j in enumerate(word2index)}

df.head()

emotions = df.sentiment.unique()
sum_categorical_emotions = [df[df.sentiment == i].size for i in emotions]
plt.bar(emotions, sum_categorical_emotions)
plt.show()

df.loc[df.sentiment == 'anger', 'sentiment'] = 'anger'
df.loc[df.sentiment == 'happiness', 'sentiment'] = 'happiness'
df.loc[df.sentiment == 'sad', 'sentiment'] = 'sadness'
df.loc[df.sentiment == 'boredom', 'sentiment'] = 'sadness'
df.loc[df.sentiment == 'empty', 'sentiment'] = 'surprise'
df.loc[df.sentiment == 'fun', 'sentiment'] = 'happiness'
df.loc[df.sentiment == 'enthusiasm', 'sentiment'] = 'happiness'
df.loc[df.sentiment == 'hate', 'sentiment'] = 'disgust'
df.loc[df.sentiment == 'love', 'sentiment'] = 'happiness'
df.loc[df.sentiment == 'neutral', 'sentiment'] = 'surprise'
df.loc[df.sentiment == 'relief', 'sentiment'] = 'happiness'
df.loc[df.sentiment == 'surprise', 'sentiment'] = 'surprise'
df.loc[df.sentiment == 'worry', 'sentiment'] = 'fear'
df.sentiment.unique()

# Happiness Sadness Fear Disgust Anger Surprise

emotions = df.sentiment.unique()
sum_categorical_emotions = [df[df.sentiment == i].size for i in emotions]
print(sum_categorical_emotions)
plt.bar(emotions, sum_categorical_emotions)
plt.show()

from keras.models import Model
from keras.layers import LSTM, Activation, Dense, Dropout, Input, Embedding
from keras.optimizers import RMSprop
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from keras.utils import to_categorical

sequences = tokenizer.texts_to_sequences(df['content'])
data = pad_sequences(sequences, maxlen=50)
X = data.reshape(len(data), 50)
X[100]

flag = pd.Series(list(df['sentiment']))
Y = pd.get_dummies(flag)
Y = np.array(Y)
Y[100]

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42)

inputs = Input(shape=[50])
layer = Embedding(100000, 500, input_length=50)(inputs)
layer = LSTM(512)(layer)
layer = Dense(256)(layer)
layer = Activation('relu')(layer)
layer = Dropout(0.5)(layer)
layer = Dense(6)(layer)
layer = Activation('softmax')(layer)
model = Model(inputs=inputs,outputs=layer)
model.summary()
model.compile(loss='categorical_crossentropy',optimizer="adam",metrics=['accuracy'])

model.fit(X_train, y_train, batch_size=256, epochs=10, validation_data=(X_test, y_test), shuffle=True)

model.save('master_model.h5')

# Prediction and Evaluation
from keras.models import load_model
model = load_model('master_model.h5')

statement = "The mother gave birth to a baby."
sequences = tokenizer.texts_to_sequences([statement])
data = pad_sequences(sequences, maxlen=50)
sentiments = df.sentiment.unique()
y = model.predict(data)
y = np.argmax(y)
print(sentiments[y])

y_predict = model.predict(X_test)

from sklearn.metrics import confusion_matrix
predict = np.argmax(y_predict, axis = 1)
y_test_class = np.argmax(y_test, axis = 1)
cm = confusion_matrix(predict, y_test_class)

ax = plt.subplot()
sns.heatmap(cm, annot = True, ax = ax)
sns.set(rc={'figure.figsize':(15, 11)})
ax.set_xlabel('Predicted labels')
ax.set_ylabel('True labels')
ax.set_title('Confusion Matrix')
ax.xaxis.set_ticklabels(emotions)
ax.yaxis.set_ticklabels(emotions)

from sklearn.metrics import precision_recall_fscore_support as score
precision, recall, fscore, support = score(y_test_class, predict)
print('precision: {}'.format(precision))
print('recall: {}'.format(recall))
print('fscore: {}'.format(fscore))
print('support: {}'.format(support))
print('emotion: {}'.format(emotions))

score_table = PrettyTable(['Emotion', 'Precision', 'Recall', 'F-score', 'Support'])
for i in range(0, len(emotions)):
    score_table.add_row([emotions[i], precision[i], recall[i], fscore[i], support[i]])
print(score_table)

