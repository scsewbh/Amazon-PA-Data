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
#mycursor.execute("CREATE TABLE products (id INT AUTO_INCREMENT PRIMARY KEY, PartialLink TEXT, Link TEXT)")

#mycursor.execute("SHOW TABLES")
#mycursor.execute("DROP TABLE products")

mycursor.execute("SELECT * FROM products")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)

amzn_base_url = 'https://www.amazon.com/'
amzn_bestElec_url = 'https://www.amazon.com/Best-Sellers/zgbs/electronics/'
amzn_bestVideoGame_url = 'https://www.amazon.com/Best-Sellers/zgbs/videogames/'
amzn_bestCellAccessories_url = 'https://www.amazon.com/Best-Sellers/zgbs/wireless/'
amzn_bestPC_url = 'https://www.amazon.com/Best-Sellers/zgbs/pc/'
amzn_bestHPC_url = 'https://www.amazon.com/Best-Sellers/zgbs/hpc/'
amzn_bestSkincare_url = 'https://www.amazon.com/Best-Sellers/zgbs/beauty/11060451/'
amzn_bestHI_url = 'https://www.amazon.com/Best-Sellers/zgbs/hi/'
amzn_bestOffice_url = 'https://www.amazon.com/Best-Sellers/zgbs/office-products'


class AMZN:
    def __init__(self):
        self.session = requests.Session()

    def results(self):
        sql = "INSERT INTO products (PartialLink, Link) VALUES (%s, %s)"
        test = self.session.get(amzn_bestElec_url)
        soup = bs(test.text, 'html.parser')
        a = soup.find_all('a', class_='a-link-normal a-text-normal')
        data = []
        for x in a:
            data.append((x['href'], amzn_base_url + x['href']))
        print(data)
        mycursor.executemany(sql, data)
        mydb.commit()

        print(mycursor.rowcount, "was inserted.")

