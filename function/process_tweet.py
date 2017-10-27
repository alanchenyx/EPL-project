"""

functions for preprocessing

"""

import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer

nltk.download('punkt')
nltk.download('stopwords')

punctuation = list(string.punctuation)
stopwords = stopwords.words('english')
http_link = 'https://'

# remove negation words from stopwords
neg_words = ['no', 'nor', 'not', 'wasn', 'weren']
for word in neg_words:
    stopwords.remove(word)


def process(tweet):
    tweet = reduce_lengthening(tweet)
    token_list = tokenize(tweet)
    processed_token_list = process_token(token_list)
    stem_token_list = stemming(processed_token_list)
    return stem_token_list

def tokenize(tweet):
    tokenizer = TweetTokenizer(preserve_case=False, reduce_len=True)
    token_list = tokenizer.tokenize(tweet)
    return token_list


def reduce_lengthening(text):
    pattern = nltk.re.compile(r"(.)\1{2,}")
    return pattern.sub(r"\1\1", text)

def stemming(token_list):
    ps = PorterStemmer()
    for i in range((len(token_list))):
        token_list[i] = ps.stem(token_list[i])
    return token_list


# remove punctuation/stopwords/http/@
def process_token(token_list):
    result_list = [token for token in token_list if not (
        (http_link in token) or (token in stopwords) or (token in punctuation) or (token.startswith('@')) or (
            token == 'rt') or is_number(token))]
    return result_list


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False
