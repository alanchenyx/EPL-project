"""

configuration

"""

import configparser
import json

parser = configparser.ConfigParser()
parser.read(r'config.ini')

consumer_key = parser['twitter']['consumer_key']
consumer_secret = parser['twitter']['consumer_secret']
access_token = parser['twitter']['access_token']
access_token_secret = parser['twitter']['access_token_secret']

locations = json.loads(parser['filter']['locations'])
track = json.loads(parser['filter']['track'])

connection = parser['mongodb']['connection']
db_tweet_raw = parser['mongodb']['db_tweet_raw']
db_tweet_reduce = parser['mongodb']['db_tweet_reduce']
spu_che_20082017 = parser['mongodb']['spu_che_20082017']
auth_type = parser['mongodb']['auth_type']
db_target = parser['mongodb']['db_tweet_raw']







# logging.basicConfig(
#     filename='log_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.log',
#     filemode='w',
#     level=logging.INFO,
#     format='%(asctime)s [%(levelname)s] %(message)s',
#     datefmt='%m/%d/%Y %I:%M:%S %p')
#
# logging.info('Logging started...')
