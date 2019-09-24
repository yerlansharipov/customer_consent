#!/anaconda3/bin/python
import tweepy as tw
from google.cloud import language_v1
from google.cloud.language_v1 import enums
from cred_twitter import param
import pandas as pd
import six
from preprocessor.api import clean, tokenize, parse

import numpy as np 
import gmaps 
import gmaps.datasets 
from geopy.geocoders import Nominatim

#Twitter API credentials
consumer_key = param()[0]
consumer_secret = param()[1]
access_token = param()[2]
access_token_secret = param()[3]

#parsing data from twitter
def parse_tweets(user, date):

    pd.set_option('mode.chained_assignment', None)

    #twitter authentication
    print("### Info: Authentication in Twitter...", end='')
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    print("DONE!")

    #parse tweets
    print("### Info: Raw data collection based on mention of ", user,"...", end='')    
    tweets = tw.Cursor(api.search, q=user, lang="en", since=date, tweet_mode="extended").items()
    tweets_raw = pd.DataFrame(columns=["Date","Location", "Lat", "Lon", "Text", "Score", "Magnitude"])
    i = 0
    for tweet in tweets:
        tweets_raw = tweets_raw.append({'Date': tweet.created_at, 'Location':tweet.user.location, 'Text':tweet.full_text}, ignore_index=True)
        i += 1
        if i == 10:
            break
    print("DONE!")

    return tweets_raw

#cleaning the data
def data_preprocessing (tweets_raw):

    print("### Info: Cleaning the data...", end='')
    tweets_clean = pd.DataFrame(columns=["Date","Location", "Text"])

    for i in range(tweets_raw.shape[0]):
        clean_text = clean(tweets_raw["Text"][i])
        tweets_raw["Text"][i] = clean_text
    print("DONE!")

    return tweets_raw

#get sentiments from tweets
def analyze_sentiment(tweets_cleaned):

    print("### Info: Sentiment analyze...", end='')
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
    print("DONE!")

    return tweets_raw

#convert address in coordinates
def geolocation(tweets_sentiment):

    print("### Info: Converting address into coordinates...", end='')
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    for i in range(tweets_raw.shape[0]):
        try:
            location = geolocator.geocode(tweets_raw["Location"][i])
            tweets_raw["Lat"][i] = location.latitude
            tweets_raw["Lon"][i] = location.longitude
        except:
            tweets_raw["Lat"][i] = None
            tweets_raw["Lon"][i] = None
    print("DONE!")

    return tweets_raw

#make a heatmap based on location of tweets
def heatmap(tweets_location):

    print("Info: Building heatmap...", end='')

    #Seattle 47.60° N, 122.33° W
    #Miami   25.76° N, 80.19° W

    Lon = np.arange(-71.21, -71, 0.0021) 
    Lat = np.arange(42.189, 42.427, 0.00238) 
    Crime_counts = np.zeros((100,100))

    longitude_values = [Lon,]*100 
    latitude_values = np.repeat(Lat,100) 
    Crime_counts.resize((10000,)) 
    heatmap_data = {'Counts': Crime_counts, 'latitude': latitude_values, 'longitude' : np.concatenate(longitude_values)} 
    df = pd.DataFrame(data=heatmap_data)
    locations = df[['latitude', 'longitude']] 
    weights = df['Counts'] 
    fig = gmaps.figure() 
    heatmap_layer = gmaps.heatmap_layer(locations, weights=weights) 
    fig.add_layer(gmaps.heatmap_layer(locations, weights=weights))
    print(fig) 


    print("DONE!")

    return 0

if __name__ == '__main__':

    #tweets_raw = parse_tweets("@SpaceX", "2019-09-23")
    #tweets_cleaned = data_preprocessing (tweets_raw)
    #tweets_sentiment = analyze_sentiment(tweets_cleaned)
    #tweets_location = geolocation(tweets_sentiment)
    heatmap(4)
    pass

    
        
    



