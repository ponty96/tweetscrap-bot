
import tweepy
from .scrapper import splitText
from pubsub import pub
import json
import pprint
keywords = ['scrap','from', 'end']

pp = pprint.PrettyPrinter(indent=4)

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


    def buildMessageTemplate(self,tweet):
        print("----------- this is a new tweet ---------------")
        print("\n")
        pp.pprint(tweet)
        print("\n")
        print("----------- this is the end of a tweet ---------------")
        msg = tweet.text + "\n" + self.getHashtags(tweet.entities) 
        return tweet.text
        
    def getHashtags(self, hashtags):
         hashs = ""
         for hash in hashtags:
             hashs = hashs+hash.text
         
         return hashs


    def queryBuilder(self, channel):
        for tweet in tweepy.Cursor(self.twitterApi.search, q=self.keyParamArray[0]['action'], count=3).items(30):
            json_obj = self.buildMessageTemplate(tweet)
            payload = {}
            payload['channel'] = channel
            payload['text'] = json_obj
            self.dispatchMessage("tweet", payload) 
            

    def search_for_hash_tag(self, channel):
        # search from twitter
        payload = {}
        payload['channel'] = channel
        payload['text'] = self.queryBuilder()
        self.dispatchMessage("tweet", payload)

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

        self.queryBuilder(channel=channel)


    # register a callback to listen to changes
    def registerListener(self, callback, obj_type):
       self.pub.subscribe(callback, obj_type)

    # dispatches changes
    def dispatchMessage(self, obj_type, payload):
       self.pub.sendMessage(obj_type, payload=payload)
