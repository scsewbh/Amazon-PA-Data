import mysql.connector
import requests
import time
import tweepy
import os

#------------Twitter - Use Test Account-------------------
# Twitter Bot
# -------------------------------------
# Limits:
# Follow Limit
# 400 - New following per day
# 300 - tweets or retweets every 3 hours <<<<IMPORTANT!!!!
# 10800 seconds in 3 hours / 300 tweets = 1 tweet every 36 secs ~= 40secs for safety
# 1000 - likes per day
# 1000 - DMs sent per day
# -------------------------------------

mydb = mysql.connector.connect(
    host=os.environ.get("HOST"),
    user=os.environ.get("USER"),
    password=os.environ.get("PASSWORD"),
    database="mydatabase"
)

# Destroyer Account

consumer_key = os.environ.get("CK")
consumer_secret_key = os.environ.get("CSK")
access_token = os.environ.get("AT")
access_token_secret = os.environ.get("ATS")


class TWT():
    def __init__(self):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit='True', wait_on_rate_limit_notify='True')
        self.my_id = self.api.me().id
        self.url = ''
        self.mycursor = mydb.cursor()

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

    def DB_grab(self):
        self.mycursor.execute("USE mydatabase")
        self.mycursor.execute("select p.ProductName, p.Link, i.Name, i.Price as I_Price, s.Price as S_Price, "
                              "i.Img_URL, i.Price-s.Price as P_Value from sync_data s, item_data i, products p where "
                              "p.ProductName = i.ProductName and p.ProductName = s.ProductName and (("
                              "i.Price-s.Price)/i.Price*100)>=10 and i.Price-s.Price>0 and i.Price>0 and s.Price>0 "
                              "and Img_URL!='' order by i.Price-s.Price desc")

        myresult = self.mycursor.fetchall()

        for row in myresult:
            time.sleep(40) # TO FOLLOW TWITTER RATE LIMIT 36 sec min.
            name = row[2]
            price = str(row[4])
            d_price = str(row[3])
            self.url = row[5]
            link = row[1]
            msg = name + '\n\nPrice: $' + d_price + '\nDeal Price: $' + price + '\n\n' + link
            self.tweet(msg)


instance = TWT()
while True:
    instance.DB_grab()



