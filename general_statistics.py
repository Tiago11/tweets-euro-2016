################################################################################
#                                                                              #
# Here we have an example of how the ipython notebooks code looks like.        #
# This file has the code to get the generals statistics of the match PORvsFRA. #
#                                                                              #
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
import folium

################################################################################
# Match: Portugal vs France.

# Get all the tweets from the .csv files into pandas DataFrame.
t_por = pd.read_csv('/home/tiago/Desktop/Tiago/Proyectos/Twitter_data/euro_copa/7_por_fra/por_fra_por.csv', encoding='utf-8')
t_fra = pd.read_csv('/home/tiago/Desktop/Tiago/Proyectos/Twitter_data/euro_copa/7_por_fra/por_fra_fra.csv', encoding='utf-8')

# Make all the text lowercase.
t_por['text'] = t_por['text'].str.lower()
t_fra['text'] = t_fra['text'].str.lower()

# Concatenate both dataframes and remove duplicate tweets.
t_por_fra = pd.concat([t_por, t_fra])
t_por_fra.drop_duplicates(inplace=True)

# Transforme the 'created_at' field into a datetime.
t_por_fra['created_at'] = pd.to_datetime(t_por_fra['created_at'])
t_por_fra.head()

################################################################################
# Remove the tweets made before and after the match.

mask1 = (t_por_fra['created_at'] > '2016-07-10 10:30:00') & (t_por_fra['created_at'] <= '2016-07-10 18:55:00')
t_por_fra.loc[mask1]
t_por_fra.drop(t_por_fra.loc[mask1].index, inplace=True)

mask2 = (t_por_fra['created_at'] > '2016-07-10 23:50:00') & (t_por_fra['created_at'] <= '2016-07-10 23:59:59')
t_por_fra.loc[mask2]
t_por_fra.drop(t_por_fra.loc[mask2].index, inplace=True)

################################################################################
# Print some information.

print "Total tweets: " + str(len(t_por_fra.index))

t_rt = t_por_fra[t_por_fra['text'].str.contains('rt')]
print "Count of retweets: " + str(len(t_rt))

from __future__ import division

porc = len(t_rt)*100/len(t_por_fra.index)
print "Percentage of retweets in dataset: " + str(porc)

################################################################################
# Plot tweets vs retweets in dataset.

pre_data = []
for x in range(0,167164):
    pre_data.append('tweet')
for x in range(0,622538):
    pre_data.append('re-tweet')

s = pd.Series(pre_data)
s.value_counts(normalize=True)

df_s = pd.DataFrame(s.value_counts(normalize=True))
vincent.core.initialize_notebook()

donut = vincent.Pie(df_s, inner_radius=80, outer_radius=100)
donut.colors(brew="Set2")
donut.legend('Categories')
donut.display()

################################################################################

print "Languages percentage"
print t_por_fra['lang'].value_counts(normalize=True)[0:9]

################################################################################
# Plot languages:
df_lang = pd.DataFrame(t_por_fra['lang'].value_counts(normalize=True)[0:8])

vincent.core.initialize_notebook()

donut = vincent.Pie(df_lang, inner_radius=80, outer_radius=100)
donut.colors(brew="Set2")
donut.legend('Languages')
donut.display()

################################################################################
print "Sources percentage"
print t_por_fra['source'].value_counts(normalize=True)[0:9]

################################################################################
# Plot the sources:
df_source = pd.DataFrame(t_por_fra['source'].value_counts(normalize=True)[0:5])

vincent.core.initialize_notebook()

donut = vincent.Pie(df_source, inner_radius=80, outer_radius=100)
donut.colors(brew="Set2")
donut.legend('Sources')
donut.display()

################################################################################
# Group the tweets in 1 minute intervals.

tweets2 = t_por_fra.set_index(t_por_fra['created_at'])
tweets2.index.name = None
tweets3 = tweets2.resample('1min', how='count')

# Plot the amount of tweets per minute during the match.

vincent.core.initialize_notebook()

area = vincent.Area(tweets3['created_at'])
area.colors(brew='Spectral')
area.display()

################################################################################
# Print the mean of tweets per minute made during the match.

print tweets3['created_at'].mean()

################################################################################
# Analyze the most frecuent words made during the match.

local_stopwords = ['#porfra', 'portugal', 'france', 'rt', "c'est", u'\xe9', 'va']
stop_words = stopwords.words('english') + stopwords.words('french') + stopwords.words('portuguese') + stopwords.words('spanish') + local_stopwords
text = t_por_fra['text']

tokens = []
for txt in text.values:
    tokens.extend([t.lower().strip(":,.-!") for t in txt.split()])


filtered_tokens = [w for w in tokens if not w in stop_words]

freq_dist = nltk.FreqDist(filtered_tokens)
freq_dist.pop('')
lmc = freq_dist.most_common(20)
print lmc

################################################################################
# Analyze the most used bi-grams.
bgs = nltk.bigrams(filtered_tokens)

fdist = nltk.FreqDist(bgs)
print fdist.most_common(10)

################################################################################
# Analyze the most used tri-grams.
tgs = nltk.trigrams(filtered_tokens)

fdist = nltk.FreqDist(tgs)
print fdist.most_common(10)

################################################################################
# Find the most retweeted tweets
mrt = pd.DataFrame(data=t_por_fra['text'].value_counts())
print mrt[:10]

################################################################################
# Plot the most named players of the match (and when where they named).

t1 = t_por_fra[t_por_fra['text'].str.contains('ronaldo')]
t1 = t1.set_index(t1['created_at'])
t1.index.name = None
t1 = t1.resample('1min').count()

t2 = t_por_fra[t_por_fra['text'].str.contains('payet')]
t2 = t2.set_index(t2['created_at'])
t2.index.name = None
t2 = t2.resample('1min').count()

t3 = t_por_fra[t_por_fra['text'].str.contains('sissoko')]
t3 = t3.set_index(t3['created_at'])
t3.index.name = None
t3 = t3.resample('1min').count()

t4 = t_por_fra[t_por_fra['text'].str.contains('eder')]
t4 = t4.set_index(t4['created_at'])
t4.index.name = None
t4 = t4.resample('1min').count()

t5 = t_por_fra[t_por_fra['text'].str.contains('quaresma')]
t5 = t5.set_index(t5['created_at'])
t5.index.name = None
t5 = t5.resample('1min').count()

vincent.core.initialize_notebook()

t1.drop(['created_at', 'geo', 'source', 'retweet_count', 'tweet_id', 'coordinates', 'favorite_count', 'in_reply_to_status_id', 'in_reply_to_user_id', 'lang'],axis=1, inplace=True)
t1.columns = ['Ronaldo']
t2.drop(['created_at', 'geo', 'source', 'retweet_count', 'tweet_id', 'coordinates', 'favorite_count', 'in_reply_to_status_id', 'in_reply_to_user_id', 'lang'],axis=1, inplace=True)
t2.columns = ['Payet']
t3.drop(['created_at', 'geo', 'source', 'retweet_count', 'tweet_id', 'coordinates', 'favorite_count', 'in_reply_to_status_id', 'in_reply_to_user_id', 'lang'],axis=1, inplace=True)
t3.columns = ['Sissoko']
t4.drop(['created_at', 'geo', 'source', 'retweet_count', 'tweet_id', 'coordinates', 'favorite_count', 'in_reply_to_status_id', 'in_reply_to_user_id', 'lang'],axis=1, inplace=True)
t4.columns = ['Eder']
t5.drop(['created_at', 'geo', 'source', 'retweet_count', 'tweet_id', 'coordinates', 'favorite_count', 'in_reply_to_status_id', 'in_reply_to_user_id', 'lang'],axis=1, inplace=True)
t5.columns = ['Quaresma']

t_fin = t1.join(t2)
t_fin = t_fin.join(t3)
t_fin = t_fin.join(t4)
t_fin = t_fin.join(t5)

lines = vincent.Line(t_fin)
lines.legend(title='Players')
lines.display()

################################################################################
# Analyze Quaresma's spike.

t_ram = t_por_fra[t_por_fra['text'].str.contains('quaresma')]

tweets2 = t_ram.set_index(t_ram['created_at'])
tweets2.index.name = None
tweets3 = tweets2.resample('1min').count()

# Find the spike.
print tweets3['created_at'].idxmax()

# Isolate the spike.
mask3 = (t_ram['created_at'] < '2016-07-10 19:25:00') | (t_ram['created_at'] > '2016-07-10 19:27:00')
tweets4 = t_ram.copy()
tweets4.loc[mask3]
tweets4.drop(tweets4.loc[mask3].index, inplace=True)
tweets4.count()


# Analyze the most frequent words during the spike.
local_stopwords = ['rt', 'vs']
stop_words = stopwords.words('english') + stopwords.words('french') + stopwords.words('portuguese') + local_stopwords
text = tweets4['text']


tokens = []
for txt in text.values:
    tokens.extend([t.lower().strip(":,.-") for t in txt.split()])


filtered_tokens = [w for w in tokens if not w in stop_words]

# Print the most common words during the spike.
freq_dist = nltk.FreqDist(filtered_tokens)
freq_dist.pop('')
lmc = freq_dist.most_common(20)
print lmc

# Print the most retweeted tweets during the spike
mrt = pd.DataFrame(data=tweets4['text'].value_counts())
print mrt[:10]

################################################################################
# Popular hashtags.
hashtags = [x for x in filtered_tokens if x.startswith('#')]

hashtag_fd = nltk.FreqDist(hashtags)
hmc = hashtag_fd.most_common(20)
print hmc[0:10]

################################################################################
# Popular mentions ('@username')
mentions = [x for x in filtered_tokens if x.startswith('@')]

mentions_fd = nltk.FreqDist(mentions)
mmc = mentions_fd.most_common(20)
print mmc[0:10]

################################################################################
# Amount of geographical data.
print len(t_por_fra['coordinates'].dropna())

################################################################################
# Map the geographical data.

# Get the geographical data.
res = t_por_fra['coordinates'].dropna()
res2 = res.value_counts()
aux = res2.to_dict()

import json

l = []
for k,v in aux.iteritems():
    kj = json.loads(k)
    l.append((kj['coordinates'],v))


map_por_fra = folium.Map()

for elem in l:
    if elem[1] < 5:
        folium.CircleMarker(location=[elem[0][1], elem[0][0]], radius=500, color='#3186cc',fill_color='#3186cc').add_to(map_por_fra)
    elif elem[1] < 10:
        folium.CircleMarker(location=[elem[0][1], elem[0][0]], radius=500, color='yellow',fill_color='yellow').add_to(map_por_fra)
    elif elem[1] < 15:
        folium.CircleMarker(location=[elem[0][1], elem[0][0]], radius=500, color='orange',fill_color='orange').add_to(map_por_fra)
    else:
        folium.CircleMarker(location=[elem[0][1], elem[0][0]], radius=500, color='red',fill_color='red').add_to(map_por_fra)

map_por_fra
