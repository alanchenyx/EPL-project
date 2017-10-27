"""

This file is for generating collections for each match

"""

import datetime
from pymongo import MongoClient
import config

client = MongoClient(config.connection)
sourcedb = client.tweet[config.db_tweet_reduce]

# targetdb = client.match.Spurs_Chelsea_20082017
# targetdb = client.match.Everton_Chelsea_27082017
# targetdb = client.match.Chelsea_Arsenal_17092017
# targetdb = client.match.ManCity_Everton_21082017
# targetdb = client.match.Bournemouth_ManCity_26082017
targetdb = client.match.Watford_ManCity_16092017




# looking for tweets based on "created_at"
# startTime = "Sun Aug 20 15:00:00 +0000 2017"
# startTime = "Sun Aug 27 12:30:00 +0000 2017"
# startTime = "Sun Sep 17 12:30:00 +0000 2017"
# startTime = "Mon Aug 21 19:00:00 +0000 2017"
# startTime = "Sat Aug 26 11:30:00 +0000 2017"
startTime = "Sat Sep 16 14:00:00 +0000 2017"



dt = datetime.datetime.strptime(startTime, '%a %b %d %H:%M:%S +0000 %Y')
dfshift = dt + datetime.timedelta(0, 60 * 120)
endTime = dfshift.strftime('%a %b %d %H:%M:%S +0000 %Y')

tweets = list(sourcedb.find({'created_at': {'$gte': startTime, '$lt': endTime}}))
for tweet in tweets:
    # if 'chelsea' in tweet['processed_text']:
    targetdb.save(tweet)


    # file = open('match.txt', 'r')
    # lines = file.readlines()
    # for line in lines:
    #     elelist = line.split(',')
    #     targetdb = client((elelist[0]+'_'+elelist[1]+'_'+elelist[2]))
    #     startTime = elelist[3]
