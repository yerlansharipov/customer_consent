#!/anaconda3/bin/python
import tweepy as tw
from google.cloud import language_v1
from google.cloud.language_v1 import enums
from cred_twitter import param
import pandas as pd
import six
from preprocessor.api import clean, tokenize, parse

#Twitter API credentials
consumer_key = param()[0]
consumer_secret = param()[1]
access_token = param()[2]
access_token_secret = param()[3]

#parsing data from twitter
def parse_tweets(user, date):

    #twitter authentication
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    print("### Info: Succesfully authenticated in Twitter")

    #parse tweets
    tweets = tw.Cursor(api.search, q=user, lang="en", since=date, tweet_mode="extended").items()
    tweets_raw = pd.DataFrame(columns=["Date","Location", "Text", "Score", "Magnitude"])
    i = 0
    for tweet in tweets:
        tweets_raw = tweets_raw.append({'Date': tweet.created_at, 'Location':tweet.user.location, 'Text':tweet.full_text}, ignore_index=True)
        i += 1
        if i == 10:
            break
    print("### Info: Raw data is collected based on mention of ", user)

    return tweets_raw

#cleaning the data
def data_preprocessing (tweets_raw):
    tweets_clean = pd.DataFrame(columns=["Date","Location", "Text"])

    for i in range(tweets_raw.shape[0]):
        clean_text = clean(tweets_raw["Text"][i])
        tweets_raw["Text"][i] = clean_text
    
    return tweets_raw

#get sentiments from tweets
def analyze_sentiment(tweets_cleaned):

    #client = language_v1.LanguageServiceClient()
    client = language_v1.LanguageServiceClient.from_service_account_json("/Users/q/skunkw/google_application_credentials/google_cred.json")

    for i in range(tweets_raw.shape[0]):
        content = tweets_raw["Text"][i]
        if isinstance(content, six.binary_type):
            content = content.decode('utf-8')
        type_ = enums.Document.Type.PLAIN_TEXT
        document = {'type': type_, 'content': content}
        response = client.analyze_sentiment(document)
        sentiment = response.document_sentiment
        tweets_raw["Score"][i] = sentiment.score
        tweets_raw["Magnitude"][i] = sentiment.magnitude

if __name__ == '__main__':
    tweets_raw = parse_tweets("@SpaceX", "2019-09-23")
    tweets_cleaned = data_preprocessing (tweets_raw)
    sentiments = analyze_sentiment(tweets_cleaned)
    print(tweets_cleaned)

    
        
    



