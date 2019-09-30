#!/anaconda3/bin/python
import tweepy as tw
from google.cloud import language_v1
from google.cloud.language_v1 import enums
from cred_twitter import param
from cred_alpha_vantage import av_cred
import pandas as pd
import six
from preprocessor.api import clean, tokenize, parse

import numpy as np 
import gmaps 
import gmaps.datasets 
from geopy.geocoders import Nominatim
from matplotlib import pyplot as plt
import datetime

import pandas as pd
import matplotlib.pyplot as plt
import csv
from datetime import datetime 
from alpha_vantage.timeseries import TimeSeries

from datetime import datetime, date, time, timedelta

#Twitter API credentials
consumer_key = param()[0]
consumer_secret = param()[1]
access_token = param()[2]
access_token_secret = param()[3]

#Alpha Vantage key
av_key = av_cred()

#parsing data from twitter
def parse_tweets(user, date_range):

    pd.set_option('mode.chained_assignment', None)

    #twitter authentication
    #print("### Info: Authentication in Twitter...", end='')
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    #print("DONE!")
    sentiments = list()
    #parse tweets
    #print("### Info: Raw data collection based on mention of ", user,"...", end='')
    for d_id in range(len(date_range)-1):
        tweets = tw.Cursor(api.search, q=user, lang="en", since=date_range[d_id], until=date_range[d_id+1],tweet_mode="extended").items(10)
        #tweets_raw = pd.DataFrame(columns=["Date","Location", "Lat", "Lon", "Text", "Score", "Magnitude"])
        i = 0
        tweets_cleaned = []
        for tweet in tweets:
            tweets_cleaned.append(data_preprocessing(tweet.full_text))
            #tweets_raw = tweets_raw.append({'Date': tweet.created_at, 'Location':tweet.user.location, 'Text':tweet.full_text}, ignore_index=True)
            
            #i += 1
            #if i == 10:
            #    break
        #print(tweets_cleaned)
        ave_sent_per_day = analyze_sentiment(tweets_cleaned)
        #print("ave_sent_per_day:", ave_sent_per_day)
        sentiments.append(ave_sent_per_day)
    #print("DONE!")

    return sentiments

"""
#forgotten piece
tweets = tw.Cursor(api.search, q=user, lang="en", since=cur_date[d_id], until=cur_date[d_id+1],tweet_mode="extended").items(10)
        tweets_raw = pd.DataFrame(columns=["Date","Location", "Lat", "Lon", "Text", "Score", "Magnitude"])
        i = 0
        for tweet in tweets:
            tweets_raw = tweets_raw.append({'Date': tweet.created_at, 'Location':tweet.user.location, 'Text':tweet.full_text}, ignore_index=True)
            i += 1
            if i == 10:
                break
"""

#cleaning the data
def data_preprocessing (tweets_raw):

    clean_text = clean(tweets_raw)

    #print("### Info: Cleaning the data...", end='')
    #tweets_clean = pd.DataFrame(columns=["Date","Location", "Text"])
    """
    for i in range(tweets_raw.shape[0]):
        clean_text = clean(tweets_raw["Text"][i])
        tweets_raw["Text"][i] = clean_text
    """
    #print("DONE!")

    return tweets_raw

#get sentiments from tweets
def analyze_sentiment(tweets_cleaned):

    #print("### Info: Sentiment analyze...", end='')
    #client = language_v1.LanguageServiceClient()
    client = language_v1.LanguageServiceClient.from_service_account_json("/Users/q/skunkw/google_application_credentials/google_cred.json")
    content = tweets_cleaned

    sum_of_sent = 0
    for i in tweets_cleaned:
        content = i
        if isinstance(content, six.binary_type):
            content = content.decode('utf-8')
        type_ = enums.Document.Type.PLAIN_TEXT
        document = {'type': type_, 'content': content}
        response = client.analyze_sentiment(document)
        sentiment = response.document_sentiment
        sum_of_sent += sentiment.score

    ave_sent_per_day = sum_of_sent/(len(tweets_cleaned)+1)

    #tweets_raw["Score"][i] = sentiment.score
    #tweets_raw["Magnitude"][i] = sentiment.magnitude

    """
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
    """

    #return tweets_raw
    return ave_sent_per_day

#convert address in coordinates
def geolocation(tweets_sentiment):

    #print("### Info: Converting address into coordinates...", end='')
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    for i in range(tweets_raw.shape[0]):
        try:
            location = geolocator.geocode(tweets_raw["Location"][i])
            tweets_raw["Lat"][i] = location.latitude
            tweets_raw["Lon"][i] = location.longitude
        except:
            tweets_raw["Lat"][i] = None
            tweets_raw["Lon"][i] = None
    #print("DONE!")

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

# parse stock information
def get_stock_close(comp, s1, s2):

    ALPHA_VANTAGE_API_KEY = av_key 
    
    ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas', indexing_type='integer')
    symb = 'NYSE:%(name)s' % dict(name=comp)
    #print(symb)
    
    interday_data, meta_data = ts.get_daily_adjusted(symbol=symb, outputsize='full')
    
    # Print the information of the data
    alldatesstr = interday_data['index']
    alldates = []

    for idem in range(0,len(alldatesstr)):
        alldates.append(datetime.strptime(alldatesstr[idem], '%Y-%m-%d'))
    
    allclose = interday_data['4. close']
    #print(alldates)
    
    #print(alldates[1])
    #print(alldates[2])
    #print(alldates[3])

    date1 = datetime.strptime(s1, '%Y-%m-%d') 
    date2 = datetime.strptime(s2, '%Y-%m-%d')

    date = []
    close = []
  

    for idam in range(0,len(alldates)):
        if ((alldates[idam]>=date1) and (alldates[idam]<=date2)):
            date.append(alldates[idam])
            close.append(allclose[idam])

    #print('The date of interest are ',date)
    """
    with open('tesla_stock_try.csv', 'w') as f:
        writer = csv.writer(f, delimiter='\t')
    writer.writerows(zip(date,close))
    """

    return close



def date_list_gen(start, end):
    start = datetime.strptime(start, '%Y-%m-%d')
    end = datetime.strptime(end, '%Y-%m-%d')
    step = timedelta(days=1)
    date_range = []
    while start <= end:
        date_range.append(str(start.date()))
        #print(start.date())
        start += step
    date_range.append(str(start.date()))

    return date_range

# plot the graph
def plotting (date_range, sentiments, stocks):

    fig, ax1 = plt.subplots()
    
    color = 'tab:red'
    ax1.set_xlabel('date')
    ax1.set_ylabel('stock_price', color=color)
    ax1.plot(date_range, stocks, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    
    color = 'tab:blue'
    ax2.set_ylabel('sentiment', color=color)  # we already handled the x-label with ax1
    ax2.plot(date_range, sentiments, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

    return 0

# converting time string to datetime format for comparison reasons
#def convert(s):
#  return datetime.strptime(s, '%Y-%m-%d')

if __name__ == '__main__':
    
    start_date = '2019-09-16'
    end_date = '2019-09-27'
    comp_stock_mark_name = 'TSLA'
    comp_twitter_name = '@SpaceX'

    date_range = date_list_gen (start_date, end_date)
    stocks = get_stock_close(comp_stock_mark_name,start_date,end_date)

    sentiments = parse_tweets(comp_twitter_name, date_range)
    plotting(date_range[:-1], sentiments, stocks)


    #tweets_raw = parse_tweets(comp_twitter_name, date_range)
    #print("date_range: ", date_range[:-1])
    #print("stocks: ", stocks)
    #print("sentiments: ", sentiments)
   
    
    #date_range = ['2019-09-23', '2019-09-24', '2019-09-25', '2019-09-26', '2019-09-27']
    #stocks = [241.23, 223.21, 228.7, 242.56, 242.13]
    #sentiments = [0.0940594069733478, 0.06534653496329147, 0.08415841672680166, 0.04059405971576672, -0.05841584186447729]


    #tweets_cleaned = data_preprocessing (tweets_raw)
    #tweets_sentiment = analyze_sentiment(tweets_cleaned)
    
    #print(tweets_raw)
    #plotting(tweets_raw)
    #tweets_location = geolocation(tweets_sentiment)
    #heatmap(4)
    pass


















