import csv
import datetime
import logging
from itertools import zip_longest
import base64
import bson
import nltk
import pymongo
from daal import Base
from pymongo import MongoClient, UpdateOne
import tweepy
import json
from datetime import datetime
import config
from collections import OrderedDict
from nltk.sentiment import SentimentIntensityAnalyzer
import string
import numpy


nltk.download('vader_lexicon')
from bson.json_util import dumps
sid = SentimentIntensityAnalyzer()

def sentiment(text):
    score = (sid.polarity_scores(text))
    compund = score.get('compound')
    if compund >= 0.5:
        return 'pos'
    if compund <= -0.5:
        return 'neg'
    else:
        return 'neu'

client = MongoClient(config.connection)
collection = client.tweet[config.db_tweet_raw]

# Authentication details
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_token_secret = config.access_token_secret

# sourcedb = client.tweet.tweet_reduce
# targerdb = client.tweet.tweet_train

# count = 0
# for doc in sourcedb.find():
#     # if doc["lang"] == 'en':
#     #     count += 1
#     #     targerdb.save(doc)
#     #     print(len(doc))
#     # if count == 1000:
#     #     print(doc['_id'],doc['text'])
#     #     break
#     targerdb.save(doc)
#     count += 1
#     if count == 1000:
#         break

# requests = []
# fields = ['text', '_id']
# for document in targerdb.find():
#     unset_op = dict(zip_longest(set(document.keys()).difference(fields), ['']))
#     requests.append(UpdateOne({'_id': document['_id']}, {'$unset': unset_op}))
#     # Execute per 1000 operations and re-init.
#     if len(requests) == 1000:
#         targerdb.bulk_write(requests)
#         requests = []
#
# # clean up the queues
# if requests:
#     targerdb.bulk_write(requests)

#print(count)

# looking for tweets based on "created_at"
startTime = "Sun Aug 20 15:00:00 +0000 2017"
endTime = "Sun Aug 20 15:01:00 +0000 2017"
tweets = list(collection.find({'created_at': {'$gte':startTime, '$lt':endTime}}))
for tweet in tweets:
    print(tweet["_id"]+' '+tweet["text"])

client = MongoClient('mongodb://admin:88404@115.146.92.116:27017/')
coll = client.tweet.tweet_reduce


from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

# x = [0.045454545454545456, 0.0, 0.08333333333333333, 0.09090909090909091, 0.3076923076923077, 0.1276595744680851, 0.12280701754385964, 0.11764705882352941, 0.05555555555555555, 0.0, 0.09090909090909091, 0.375, 0.4, 1.0, 0.07142857142857142, 0.0, 0.09090909090909091, 0.0, 0.42857142857142855, 0.0, 0.0, 0.1111111111111111, 0.42857142857142855, 0.16666666666666666, 0.3484848484848485, 0.3151515151515151, 0.2677165354330709, 0.23636363636363636, 0.1956521739130435, 0.3333333333333333, 0.3333333333333333, 0.1875, 0.09375, 0.08, 0.0, 0.038461538461538464, 0.2, 0.05555555555555555, 0.09090909090909091, 0.04918032786885246, 0.02040816326530612, 0.038461538461538464, 0.029411764705882353, 0.0, 0.0, 0.1111111111111111, 0.1, 0.12, 0.25, 0.18604651162790697, 0.2727272727272727, 0.16326530612244897, 0.13333333333333333, 0.05, 0.15789473684210525, 0.0, 0.16666666666666666, 0.08333333333333333, 0.1111111111111111, 0.2, 0.0625, 0.07692307692307693, 0.3181818181818182, 0.08333333333333333, 0.0, 0.2857142857142857, 0.18181818181818182, 0.16666666666666666, 0.058823529411764705, 0.16666666666666666, 0.07692307692307693, 0.2727272727272727, 0.0, 0.16666666666666666, 0.3, 0.07692307692307693, 0.0, 0.0, 0.07142857142857142, 0.0, 0.0, 0.2222222222222222, 0.07692307692307693, 0.1, 0.0, 0.07142857142857142, 0.30434782608695654, 0.0, 0.07692307692307693, 0.1111111111111111, 0.125, 0.06451612903225806, 0.034482758620689655, 0.18181818181818182, 0.05263157894736842, 0.08333333333333333, 0.0, 0.15151515151515152, 0.07692307692307693, 0.0625, 0.15384615384615385, 0.1206896551724138, 0.20987654320987653, 0.15625, 0.07317073170731707, 0.10638297872340426, 0.08849557522123894, 0.18461538461538463, 0.09923664122137404, 0.19387755102040816, 0.15254237288135594, 0.14893617021276595, 0.18181818181818182, 0.23529411764705882, 0.2391304347826087, 0.25263157894736843, 0.265625, 0.30985915492957744, 0.17073170731707318, 0.32075471698113206]
# y = [22, 19, 12, 11, 13, 47, 57, 34, 18, 10, 11, 16, 5, 1, 14, 7, 11, 9, 7, 3, 3, 9, 7, 6, 66, 165, 127, 55, 46, 27, 21, 16, 32, 25, 10, 26, 20, 18, 11, 61, 49, 52, 34, 34, 27, 27, 20, 25, 16, 43, 44, 49, 45, 20, 19, 20, 24, 12, 18, 10, 16, 13, 22, 12, 8, 7, 11, 6, 17, 12, 13, 11, 10, 18, 10, 13, 9, 10, 14, 9, 16, 9, 13, 10, 16, 14, 23, 10, 13, 18, 8, 31, 29, 22, 19, 24, 19, 33, 26, 16, 39, 58, 81, 64, 41, 47, 113, 130, 131, 98, 59, 47, 33, 51, 92, 95, 64, 71, 41, 53]
#
# peak_time_goal = []
# x_q3 = numpy.percentile(x, 75)
# y_q3 = numpy.percentile(y, 75)
# print(x_q3)
# for i in range(len(x)):
#     if x[i] > x_q3 and x[i]>x[i-1] and y[i]>y_q3 and (i<=45 or (i>60 and i<110)):
#         peak_time_goal.append(i)
# print(peak_time_goal)
# print(len(peak_time_goal))
#


# for doc in coll.find():
#     if 'chelsea' in doc['processed_text']:
#         print(doc['processed_text'])


# with open ('.\\doc\\chelsea.csv', 'r') as f:
#     reader = csv.reader(f)
#     mylist = list(reader)
#     players = []
#     for row in mylist:
#         if row[1] != '':
#             players.append(row[1].split(',')[0].lower())
#

# count =0
# for doc in sourcedb.find():
#     try:
#         var = (doc['vader_tag'])
#         count +=1
#         print(count)
#     except KeyError:
#         pass
#         # count += 1
#         # print(count)

#vader_tag
# count=0
# for doc in coll.find():
#     try:
#         var = doc['vader_tag']
#     except KeyError:
#         count += 1
#         score = sentiment(doc['processed_text'])
#         coll.update_one({'_id': doc['_id']}, {'$set': {'vader_tag': score}})
#
# print(count)



#generate pos training txt for ML
# count = 0
# postweet = []
# negtweet = []
# neutweet = []
#
# for doc in coll.find():
#     if doc['tag'] == 'pos':
#         text = doc['processed_text']
#         postweet.append(text)
#         count += 1
#     if doc['tag'] == 'neg':
#         text = doc['processed_text']
#         negtweet.append(text)
#         count += 1
#     if doc['tag'] == 'neu':
#         text = doc['processed_text']
#         neutweet.append(text)
#         count += 1
#     if count == 100000:
#         break
# #
# data_pos = open("pos.txt", "w", encoding='utf-8')
# for text in postweet:
#     data_pos.write(str(text)+'\n')
#     data_pos.flush()
# data_pos.close()
# data_neg = open("neg.txt", "w", encoding='utf-8')
# for text in negtweet:
#     data_neg.write(str(text)+'\n')
#     data_neg.flush()
# data_neg.close()
# data_neu = open("neu.txt", "w", encoding='utf-8')
# for text in neutweet:
#     data_neu.write(str(text)+'\n')
#     data_neu.flush()
# data_neu.close()


