
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
        mainMsg = []
        message = {'color':'#0084B4',
                    'author_name':"by: " + tweet.user.screen_name,
                    'author_icon':tweet.user.profile_image_url,
                    'pretext':tweet.text}
        message['fields'] = []
        text = ""
        for hash in tweet.entities['hashtags']:
             text = ''.join([text," #", hash['text']])
             
        message['fields'].append({'title':text})
        message['fields'].append({
                    "title": "Tweeted At",
                    "value": str(tweet.created_at.now().strftime("%A, %d. %B %Y %I:%M%p")),
                    "short": False
                })
        mainMsg.append(message)
        return json.dumps(mainMsg)

    def queryBuilder(self, channel):
        for tweet in tweepy.Cursor(self.twitterApi.search, q=self.keyParamArray[0]['action'], count=15).items(15):
            
            attach = self.buildMessageTemplate(tweet)
            
            payload = {}
            payload['channel'] = channel
            payload['text'] = ""
            payload['attachments'] = attach
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
