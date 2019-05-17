"""

This file is for reducing the exsiting database
Use mongoDB mapreduce to exclude all fields except ['text', '_id', 'created_at', 'lang']

"""

from itertools import zip_longest
from pymongo import MongoClient, UpdateOne
import config

client = MongoClient(config.connection)
collection = client.tweet.tweet_reduce
# collection = client.test.testcollection


requests = []
fields = ['text', '_id', 'created_at', 'lang']
count = 0
for document in collection.find():
    try:
        lan = document['lang']
        if lan != 'en':
            collection.remove(document)
        else:
            unset_op = dict(zip_longest(set(document.keys()).difference(fields), ['']))
            requests.append(UpdateOne({'_id': document['_id']}, {'$unset': unset_op}))
            # Execute per 1000 operations and re-init.
            if len(requests) == 1000:
                count = count + 1000
                print(count)
                collection.bulk_write(requests)
                requests = []
                # try:
                #     collection.bulk_write(requests)
                #     requests = []
                # except:
                #     bson.errors.InvalidDocument
                #     requests = []
    except KeyError:
        collection.remove(document)

# clean up the queues
if requests:
    collection.bulk_write(requests)
    print(count)
