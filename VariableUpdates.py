from bs4 import BeautifulSoup as bs
import mysql.connector
from selenium import webdriver
import os

#CONSTANTLY CHANGING VARIABLE - UPDATING
#-----------------------Settings--------------------------

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

mydb = mysql.connector.connect(
    host="35.231.149.95",
    user="root",
    password="Heroku3031",
    database="mydatabase"
)

amzn_base_url = 'https://www.amazon.com/'

#-----------------------AMZN Class ----------------------------

class AMZN:
    def __init__(self):
        self.browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        self.data = ()
        self.passToParser()

    def passToParser(self):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT Link FROM products") #LIMIT AT 3 FOR TESTING - PARTITION OUT FOR HEROKU SOMEHOW ----> #NOT NEEDED FOR NOW
        myresult = mycursor.fetchall()
        print(myresult)
        for url in myresult:
            print(url[0])
            self.page_parser(url[0])
        self.browser.quit()

    def page_parser(self, url):
        self.browser.get(url)
        self.data = ()
        elem = self.browser.find_element_by_css_selector('#ppd')
        main = elem.find_element_by_id('centerCol').text

        splitted = main.splitlines()
        temp = 0
        for line in splitted:
            if 'Price: $' in line:
                temp += 1
                if temp == 1:
                    self.data += ((line.split('$')[-1]).split(' ')[0],)
                if temp == 2:
                    self.data = ()
                    self.data += ((line.split('$')[-1]).split(' ')[0],)
        self.data += (url.replace(amzn_base_url, ''),)
        self.updateDatabase()

    def updateDatabase(self):
        #------Passing--------
        mycursor = mydb.cursor()
        sql = "UPDATE sync_data SET Price = %s WHERE ProductName = %s"  # Insert Ignore allows me to insert products and skip over the duplicates and the error it gives.
        mycursor.execute(sql, self.data)  # data is reversed price first then product name
        mydb.commit()
        print(mycursor.rowcount, "updated in table.")

AMZN()