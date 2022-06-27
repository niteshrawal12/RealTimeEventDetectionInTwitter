import tweepy as tp
from tweepy.streaming import StreamListener

consumer_key='GIVEYOURCUNSUMERKEYOFDEVELOPERACCOUNT'
consumer_key_secret = 'GIVEYOURCONSUMERKEYSECRETOFDEVELOPERACCOUNT'
access_token = 'GIVEYOURACCESSTOKENOFDEVELOPERACCOUNT'
access_token_secret = 'GIVEYOURACCESSTOKENSECRETOFDEVELOPERACCOUNT'

auth = tp.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tp.API(auth)
class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('/home/Desktop/project/code/RishabhPant.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status_code):
        print(status_code)
 
twitter_stream = tp.Stream(auth, MyListener())
twitter_stream.filter(track=['#RishabhPant'], languages=['en'])
print('Data Extract Successfulyy..........')