import os



# lets get all our details like the bot token
# the token
from config import *

from src.bot import Bot
from src.tweeter import Twitter



myBot = Bot(SLACK_TOKEN_ID, bot_user="@tweetscrap")

twitter = Twitter(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
                  access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)
twitter.auth()

myBot.registerListener(twitter.listenForMsg,'message')

twitter.registerListener(myBot.listenForMsg, 'tweet')

if __name__ == "__main__":
    myBot.run()
