import glob
import json
import time
import os
import sys
import logging
from slackclient import SlackClient




class Bot(object):
    def __init__(self,token):
        self.last_ping = 0
        self.token = token
        self.slack_client = None
        self.replies = {}

    def connect(self):
        self.slack_client = SlackClient(self.token)
        return self.slack_client.rtm_connect()

    def run(self):
        isConnected = self.connect()
        print(isConnected)
        if isConnected:
            while True:
                for reply in self.slack_client.rtm_read():
                    
                time.sleep(.1)
        else:
            # should throw an exception here
            print("Connection closed")
