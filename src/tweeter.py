
import tweepy
from .scrapper import splitText
from pubsub import pub
import json

keywords = ['scrap','from', 'end']

class Twitter(object):

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.twitterApi = None
        self.pub = pub
        self.keyParamArray = []

    def auth(self):
        auth =  tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.twitterApi = tweepy.API(auth)


    def queryBuilder(self):
        response = []
        for tweet in tweepy.Cursor(self.twitterApi.search, q=self.keyParamArray[0]['action']).items(10):
            json_obj = json.dumps(tweet._json)
            response.append(json_obj)

        print(response)
        return response

    def search_for_hash_tag(self, channel):
        # search from twitter
        payload = {}
        payload['channel'] = channel
        payload['text'] = self.queryBuilder()
        self.dispatchMessage("tweet", andpayload)

    def listenForMsg(self, payload):

        channel = payload['channel']
        words = splitText(payload['text'])
        self.handleMessage(words=words, channel=channel)


    def handleMessage(self, words, channel):
        msg_dict = {}
        self.keyParamArray[:] = [] # empty the array so as to have only latest messasge sent
        for i, word in enumerate(words):
            # do something with each word here
            # match regex here to get the scrap, hashtag, from_date, last_date
            if word in keywords:
                keyParamMap = {}
                keyParamMap['keyword'] = word
                keyParamMap['action'] = words[int(i+1)]
                self.keyParamArray.append(keyParamMap)

        self.search_for_hash_tag(channel=channel)


    # register a callback to listen to changes
    def registerListener(self, callback, obj_type):
       self.pub.subscribe(callback, obj_type)

    # dispatches changes
    def dispatchMessage(self, obj_type, payload):
       self.pub.sendMessage(obj_type, payload=payload)
