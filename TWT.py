import mysql.connector
from passwords import HOST, USER, PASSWORD, CK, CSK, AT, ATS
import requests
import json
import time
import tweepy
import os
from random import seed
from random import randint

#------------Twitter - Use Test Account-------------------
# Twitter Bot
# -------------------------------------
# Limits:
# Follow Limit
# 400 - New following per day
# 300 - tweets or retweets every 3 hours <<<<IMPORTANT!!!!
# 1000 - likes per day
# 1000 - DMs sent per day
# -------------------------------------

mydb = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database="mydatabase"
)

# Destroyer Account

consumer_key = CK
consumer_secret_key = CSK
access_token = AT
access_token_secret = ATS


class TWT():
    def __init__(self):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit='True', wait_on_rate_limit_notify='True')
        self.my_id = self.api.me().id
        self.url = ''

    def tweet(self, message):
        filename = 'img.jpg'
        request = requests.get(self.url, stream=True)
        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
            self.api.update_with_media(filename, status=message)
            os.remove(filename)
        else:
            self.api.update_status(message)

    def test(self):
        message = 'name\nprice\nlink'
        self.api.update_status(message)

x = TWT()
x.test()

'''mycursor = mydb.cursor()
mycursor.execute("USE mydatabase")
mycursor.execute("SELECT * FROM item_data")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)'''