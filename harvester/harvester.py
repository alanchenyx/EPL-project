"""

Twitter streaming Harvester

"""

import json
import logging
import pymongo
import tweepy
from pymongo import MongoClient
import config

client = MongoClient(config.connection)
collection = client.tweet[config.db_tweet_raw]

# Authentication details
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_token_secret = config.access_token_secret

location = config.locations
track = config.track


# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        tweet = json.loads(data)
        skip = False
        try:
            tweet['_id'] = tweet['id_str']
        except KeyError:
            try:
                tweet['_id'] = tweet['id']
            except KeyError as e:
                msg = '[SKIP] Tweet without id_str or id.\n'
                msg += json.dumps(tweet)
                msg += '\n'
                logging.exception(msg)
                skip = True
        if skip:
            pass
        else:
            # Add sentiment analysis tag if a keyword present
            # match = re.findall(keyword, tweet['text'])
            # if match:
            #     result = sort_ordered_dict(sid.polarity_scores(tweet['text'])).keys()
            #     tweet.update({tag: list(result)[0]})

            try:
                collection.insert(tweet)
            except pymongo.errors.DuplicateKeyError:
                pass

            print('id: {}'.format(tweet['_id']))


            # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
            # print('@%s: %s' % (tweet['user']['screen_name'], tweet['text'].encode('ascii', 'ignore')))
            # print('')
            # return True

    def on_error(self, status):
        logging.error('on_error:  {}'.format(status))
        return False

    def on_exception(self, exception):
        logging.error('on_exception:  {}'.format(exception))
        return False


if __name__ == '__main__':
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = tweepy.Stream(auth, StdOutListener())
    print('auth passed')

    stream.filter(locations=location, track=track, languages='en')
    print('start harvesting')
