import glob
import json
import time
import os
import sys
import logging
from slackclient import SlackClient
from slacker import Slacker
from pubsub import pub




class Bot(object):

    def __init__(self, token, bot_user):
        self.last_ping = 0
        self.token = token
        self.slack_client = None
        self.pub = pub
        self.slack = Slacker(token)
        self.bot_user = bot_user

    def connect(self):
        self.slack_client = SlackClient(self.token)
        return self.slack_client.rtm_connect()

    def run(self):
        # connect the slack_client and create a websocket connection
        isConnected = self.connect()
        if isConnected:
            while True:
                # while True we keep reading from slack every 0.3 secs for messages
                # for each payload in the array of payloads sent we dispatch a message
                # which is the type of the payload and the payload itself
                # any listener gets updated and can perform any action based on the payload
                for payload in self.slack_client.rtm_read():
                    print(payload)
                    self.dispatchMessage(payload['type'],payload)

                time.sleep(.3)
        else:
            # should throw an exception here
            print("Connection closed")

    # register a callback to listen to changes
    def registerListener(self, callback, obj_type):
        self.pub.subscribe(callback, obj_type)

    # dispatches changes
    def dispatchMessage(self, obj_type, payload):
        self.pub.sendMessage(obj_type, payload=payload)

    def sendChannelMsg(self, msg_dict):
        channel = msg_dict['channel']
        msg = msg_dict['message']
        self.slack.chat.post_message(channel=channel, text=msg, username=self.bot_user)


    def listenForMsg(self, payload):
        print(" i just got a message from tweeter")
