import os



# lets get all our details like the bot token
# the token

token = os.environ.get('TOKEN_ID');

from src.bot import Bot

myBot = Bot(token)


def testListener(payload):
    print("Listening")
    print(payload)

myBot.registerListener(testListener,'message')

if __name__ == "__main__":
    myBot.run()
