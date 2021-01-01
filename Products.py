import requests
from bs4 import BeautifulSoup as bs
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="mydatabase"
)

mycursor = mydb.cursor()
#mycursor.execute("CREATE DATABASE mydatabase")
#mycursor.execute("CREATE TABLE Products (Links TEXT(255))")

mycursor.execute("SHOW TABLES")
#mycursor.execute("DROP TABLE customers")

#for x in mycursor:
#  print(x)

amzn_base_url = 'https://www.amazon.com'
amzn_bestElec_url = 'https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/'


class AMZN:
    def __init__(self):
        self.session = requests.Session()

    def showResult(self):
        test = self.session.get(amzn_bestElec_url)
        soup = bs(test.text, 'html.parser')
        a = soup.find_all('a', class_='a-link-normal a-text-normal')
        for x in a:
            print("Found the URL:", x['href'])


x = AMZN()
x.showResult()