import requests
from bs4 import BeautifulSoup as bs
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="mydatabase"
)
'''
mycursor = mydb.cursor()
#mycursor.execute("CREATE DATABASE mydatabase")
#mycursor.execute("CREATE TABLE products (ProductName VARCHAR(200) PRIMARY KEY, Link TEXT)")

#mycursor.execute("SHOW TABLES")
#mycursor.execute("DROP TABLE products")

mycursor.execute("SELECT * FROM products")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)
'''
amzn_base_url = 'https://www.amazon.com/'
amzn_Elec_url = 'https://www.amazon.com/most-wished-for/zgbs/electronics/'
amzn_VideoGame_url = 'https://www.amazon.com/most-wished-for/zgbs/videogames/'
amzn_CellAccessories_url = 'https://www.amazon.com/most-wished-for/zgbs/wireless/'
amzn_PC_url = 'https://www.amazon.com/most-wished-for/zgbs/pc/'
amzn_HPC_url = 'https://www.amazon.com/most-wished-for/zgbs/hpc/'
amzn_Skincare_url = 'https://www.amazon.com/most-wished-for/zgbs/beauty/11060451/'
amzn_HI_url = 'https://www.amazon.com/most-wished-for/zgbs/hi/'
amzn_Office_url = 'https://www.amazon.com/most-wished-for/zgbs/office-products'

amzn_wishedFor = [amzn_Elec_url, amzn_VideoGame_url, amzn_CellAccessories_url, amzn_PC_url, amzn_HPC_url, amzn_Skincare_url, amzn_HI_url, amzn_Office_url]

class AMZN:
    def __init__(self):
        self.session = requests.Session()

    def results(self, url):
        data = []
        test = self.session.get(url)
        soup = bs(test.text, 'html.parser')
        a = soup.find_all('a', class_='a-link-normal a-text-normal')

        print(a)
        for x in a:
            p = soup
            data.append((x['href'], amzn_base_url + x['href']))
        return data


'''
<span class="p13n-sc-price">$29.99</span>
bestSellers = AMZN()
for x in amzn_bestSellers:
    data = bestSellers.results(x)
    sql = "INSERT INTO products (PartialLink, Link) VALUES (%s, %s)"
    mycursor.executemany(sql, data)
    mydb.commit()
    print(mycursor.rowcount, "was inserted.")
g = 'https://www.amazon.com//Canon-PG-243-Cartridge-Compatible-iP2820/dp/B01LXJNPZV?_encoding=UTF8&psc=1'
bestSellers = AMZN()
'''


