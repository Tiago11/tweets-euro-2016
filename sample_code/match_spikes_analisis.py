################################################################################
#                                                                              #
# Here we have an example of how the ipython notebooks code looks like.        #
# This code analyses the spikes on the amount of tweets per minute to get an   #
# idea of what happened during the match.                                      #
#                                                                              #
#                                                                              #
#  On this example we have the analysis of the match PORvsFRA using only the   #
#  tweets that contain the word 'portugal'.                                    #
################################################################################

################################################################################
# Imports.

import pandas as pd
import numpy as np
import scipy as sp
import vincent
import nltk
from nltk.corpus import stopwords
from nltk import FreqDist
import unicodedata
import pickle

################################################################################
# Create the DataFrame from the .csv file.

tweets = pd.read_csv('/home/tiago/Desktop/Tiago/Proyectos/Twitter_data/euro_copa/7_por_fra/por_fra_por.csv', encoding='utf-8')

tweets['text'] = tweets['text'].str.lower()
tweets.head()

################################################################################
# Transform the 'created_at' field into a datetime.

tweets['created_at'] = pd.to_datetime(tweets['created_at'])
tweets.head()

################################################################################
# Remove the tweets made before and after the match.

mask1 = (tweets['created_at'] > '2016-07-10 10:30:00') & (tweets['created_at'] <= '2016-07-10 18:55:00')
tweets.loc[mask1]
tweets.drop(tweets.loc[mask1].index, inplace=True)

mask2 = (tweets['created_at'] > '2016-07-10 22:00:00') & (tweets['created_at'] <= '2016-07-10 23:59:59')
tweets.loc[mask2]
tweets.drop(tweets.loc[mask2].index, inplace=True)

################################################################################
# Create a new DateFrame which contains the words 'portugal', 'portugal!' or '#portugal' (removing duplicates).
t_por1 = tweets[tweets['text'].str.contains('portugal')]
t_por2 = tweets[tweets['text'].str.contains('portugal!')]
t_por3 = tweets[tweets['text'].str.contains('#portugal')]

t_por = pd.concat([t_por1, t_por2, t_por3])
t_por.drop_duplicates(inplace=True)

t_por.head()

################################################################################
# Group the tweets on 1 minute intervals.

tweets2 = t_por.set_index(t_por['created_at'])
tweets2.index.name = None
tweets3 = tweets2.resample('1min', how='count')
tweets3.head()

################################################################################
# Get the mean of tweets per minute.

print tweets3['created_at'].mean()

################################################################################
# Get the minute with most amount of tweets.

print tweets3['created_at'].idxmax()

################################################################################
# Plot the amount of tweets per minute during the match.

vincent.core.initialize_notebook()

area = vincent.Area(tweets3['created_at'])
area.colors(brew='Set1')
area.axis_titles(x='', y='tweets/minute')
area.display()

################################################################################
# Get the tweets during the spike (+/- 2 minutes).

mask3 = (tweets['created_at'] < '2016-07-10 21:32:00') | (tweets['created_at'] > '2016-07-10 21:36:00')
tweets4 = tweets.copy()
tweets4.loc[mask3]
tweets4.drop(tweets4.loc[mask3].index, inplace=True)
tweets4.count()

################################################################################
# Analyze the most frecuent words during the spike.

local_stopwords = ['rt', 'vs', 'portugal', 'france', '#porfra']
stop_words = stopwords.words('english') + stopwords.words('french') + stopwords.words('portuguese') + local_stopwords
text = tweets4['text']


tokens = []
for txt in text.values:
    tokens.extend([t.lower().strip(":,.-") for t in txt.split()])


filtered_tokens = [w for w in tokens if not w in stop_words]

freq_dist = nltk.FreqDist(filtered_tokens2)
freq_dist.pop('')
lmc = freq_dist.most_common(10)
print lmc

################################################################################
# Analyze the bi-grams.
bgs = nltk.bigrams(filtered_tokens)

fdist = nltk.FreqDist(bgs)
print fdist.most_common(10)

################################################################################
# Analyze the tri-grams.
tgs = nltk.trigrams(filtered_tokens)

fdist = nltk.FreqDist(tgs)
fdist.most_common(10)

################################################################################
# Most retweeted tweets during the spike.
mrt = pd.DataFrame(data=tweets4['text'].value_counts())
print mrt[:10]

################################################################################
# Truncate the spike, to be able to search for the next spike.

tweets3['created_at']['2016-07-10 21:32:00'] = 0
tweets3['created_at']['2016-07-10 21:33:00'] = 0
tweets3['created_at']['2016-07-10 21:34:00'] = 0
tweets3['created_at']['2016-07-10 21:35:00'] = 0
tweets3['created_at']['2016-07-10 21:36:00'] = 0
tweets3['created_at']['2016-07-10 21:39:00'] = 0
tweets3['created_at']['2016-07-10 21:38:00'] = 0
tweets3['created_at']['2016-07-10 21:37:00'] = 0

# Get the new tallest spike.
tweets3['created_at'].idxmax()

################################################################################
# Get the tweets during the spike.

mask3 = (tweets['created_at'] < '2016-07-10 21:18:00') | (tweets['created_at'] > '2016-07-10 21:22:00')
tweets4 = tweets.copy()
tweets4.loc[mask3]
tweets4.drop(tweets4.loc[mask3].index, inplace=True)
tweets4.count()

################################################################################
# Analyze the most frecuent words during the spike.

local_stopwords = ['rt', 'vs', 'portugal', 'france', '#porfra']
stop_words = stopwords.words('english') + stopwords.words('french') + stopwords.words('portuguese') + local_stopwords
text = tweets4['text']


tokens = []
for txt in text.values:
    tokens.extend([t.lower().strip(":,.-") for t in txt.split()])


filtered_tokens = [w for w in tokens if not w in stop_words]

freq_dist = nltk.FreqDist(filtered_tokens2)
freq_dist.pop('')
lmc = freq_dist.most_common(10)
print lmc

################################################################################
# Analyze the bi-grams.
bgs = nltk.bigrams(filtered_tokens)

fdist = nltk.FreqDist(bgs)
print fdist.most_common(10)

################################################################################
# Analyze the tri-grams.
tgs = nltk.trigrams(filtered_tokens)

fdist = nltk.FreqDist(tgs)
print fdist.most_common(10)

################################################################################
# Most retweeted tweets during the spike.
mrt = pd.DataFrame(data=tweets4['text'].value_counts())
print mrt[:10]
