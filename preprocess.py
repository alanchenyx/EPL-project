"""

spark application for preprocessing

"""
import pickle
import string
from nltk.corpus import stopwords
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import *
from pyspark.sql.utils import AnalysisException
from function import process_tweet
import config

# -- CONFIGURATION --
input_url = config.connection
authentication = config.auth_type
input_db = 'test.coll'
output_db = 'test.coll'
part_size = 32
vader_tag_col = 'vader_tag'
train_tag = 'tag'
processed_text_col = 'processed_text'
punctuation = list(string.punctuation)
stopwords = stopwords.words('english')
http_link = 'https://'


# remove negation words from stopwords
neg_words = ['no', 'nor', 'not', 'wasn', 'weren']
for word in neg_words:
    stopwords.remove(word)


# dataframe function
# def sentiment(text):
#     return sort_ordered_dict(sid.polarity_scores(text))
#
# def sort_ordered_dict(order_dict):
#     return OrderedDict(sorted(order_dict.items(), key=lambda x: x[1], reverse=True)).keys()[0]

def sentiment(text):
    with open('logistic.pkl', 'rb') as model:
        lr_clf = pickle.load(model)
        tag = lr_clf.predict(text)
        return tag

def has_column(df, col):
    try:
        var = df[col]
        return True
    except AnalysisException:
        return False


# dataframe user define functions
# use function.process_tweet.process to preprocess the text
def udfValueToTest(text):
    token_list = process_tweet.process(text)
    if token_list is None:
        return None
    if len(token_list) == 1:
        return token_list[0]
    else:
        processed_text = ' '.join(token_list)
        return processed_text


def udfPosTagValue():
    return 'pos'


def udfNegTagValue():
    return 'neg'


def udfNeuTagValue():
    return 'neu'


if __name__ == "__main__":

    db_input_url = input_url + input_db + authentication
    db_output_url = input_url + output_db + authentication

    my_spark = SparkSession \
        .builder \
        .appName("vader_tag") \
        .config("spark.mongodb.input.uri", db_input_url) \
        .config("spark.mongodb.output.uri", db_input_url) \
        .config('jsonstore.rdd.partitions', part_size) \
        .getOrCreate()

    # read from db and convert to spark dataframe
    tweet = my_spark.read.format("com.mongodb.spark.sql.DefaultSource").load()

    # get all english tweets
    eng_tweet = tweet.filter(tweet.lang.rlike('en'))

    # preprocess text
    if not has_column(eng_tweet, processed_text_col):
        processed_text_udf = udf(udfValueToTest, StringType())
        processed_text = eng_tweet.withColumn(processed_text_col, processed_text_udf(eng_tweet['text']))
        processed_text.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").save()

    # generate training dataset
    # pos_tweet = eng_tweet.filter(eng_tweet.text.rlike(':\)'))
    # pos_train_udf = udf(udfPosTagValue, StringType())
    # pos_tagged_tweet = pos_tweet.withColumn(train_tag, pos_train_udf())
    # pos_tagged_tweet.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").save()
    #
    # neg_tweet = eng_tweet.filter(eng_tweet.text.rlike(':\('))
    # neg_train_udf = udf(udfNegTagValue, StringType())
    # neg_tagged_tweet = neg_tweet.withColumn(train_tag,neg_train_udf())
    # neg_tagged_tweet.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").save()
    #
    # neu_tweet = eng_tweet.filter(eng_tweet.text.rlike(':\|'))
    # neu_train_udf = udf(udfNeuTagValue, StringType())
    # neu_tagged_tweet = neu_tweet.withColumn(train_tag, neu_train_udf())
    # neu_tagged_tweet.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").save()


    # if not has_column(eng_tweet, vader_tag_col):
    #     sentiment_udf = udf(sentiment, StringType())
    #     vader_tagged_tweet = eng_tweet.withColumn(vader_tag_col, sentiment_udf(eng_tweet['processed_text']))
    #     vader_tagged_tweet.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").save()
