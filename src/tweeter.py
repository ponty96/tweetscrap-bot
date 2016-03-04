
import tweepy
from .scrapper import splitText
from pubsub import pub


class Twitter(object):

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.twitterApi = None
        self.pub = pub

    def auth(self):
        auth =  tweepy.OAuthHandler(self.consumer_key,self.consumer_secret)
        self.twitterApi = tweepy.API(auth)


    def search_for_hash_tag(self, msg_dict, channel):
        print('called search')
        hashtag = msg_dict['hashtag']
        start_date = msg_dict['from']
        end_date =  msg_dict['end_date']
        # search from twitter


        payload = {}
        payload['channel'] = channel
        payload['text'] = "i have not gone to twitter yet but will soon thou"
        self.dispatchMessage("tweet",payload)

    def listenForMsg(self, payload):

        channel = payload['channel']
        words = splitText(payload['text'])
        self.handleMessage(words=words, channel=channel)


    def handleMessage(self, words, channel):
        msg_dict = {}
        for word in words:
            # do something with each word here
            # match regex here to get the scrap, hashtag, from_date, last_date
            print(word)
            msg_dict['hashtag'] = "#dude";
            msg_dict['from'] = ""
            msg_dict['end_date'] = ""

        self.search_for_hash_tag(msg_dict=msg_dict, channel=channel)


    # register a callback to listen to changes
    def registerListener(self, callback, obj_type):
       self.pub.subscribe(callback, obj_type)

    # dispatches changes
    def dispatchMessage(self, obj_type, payload):
       self.pub.sendMessage(obj_type, payload=payload)
