#!/anaconda3/bin/python
import tweepy #https://github.com/tweepy/tweepy
import json
from google.cloud import language_v1
from google.cloud.language_v1 import enums
import six
from cred_twitter import param


#Twitter API credentials
consumer_key = param()[0]
consumer_secret = param()[1]
access_key = param()[2]
access_secret = param()[3]

import json2table
import json
import json2html


def get_all_tweets(screen_name):
    
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=10)

    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=10,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        if(len(alltweets) > 15):
            break
        print (len(alltweets),"... tweets downloaded so far")
       
    #write tweet objects to JSON
    file = open('tweet.json', 'w') 
    print ("Writing tweet objects to JSON please wait...")
    for status in alltweets:
        json.dump(status._json,file,sort_keys = True,indent = 4)

    #close the file
    print ("Done")
    file.close()

    return 'tweet.json'

def sample_analyze_sentiment(content):

    #client = language_v1.LanguageServiceClient()
    client = language_v1.LanguageServiceClient.from_service_account_json("/Users/q/skunkw/google_application_credentials/google_cred.json")

    if isinstance(content, six.binary_type):
        
        content = content.decode('utf-8')

    type_ = enums.Document.Type.PLAIN_TEXT

    document = {'type': type_, 'content': content}

    response = client.analyze_sentiment(document)

    sentiment = response.document_sentiment

    print('Score: {}'.format(sentiment.score))

    print('Magnitude: {}'.format(sentiment.magnitude))

if __name__ == '__main__':
    #pass in the username of the account you want to download
    #tweet = get_all_tweets("@Ibra_official")
    tweet = get_all_tweets("@Tesla")
    
    sample_analyze_sentiment(tweet)    
    



