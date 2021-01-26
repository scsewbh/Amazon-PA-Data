import mysql.connector
from selenium import webdriver
import os
import selenium.common.exceptions
import time

#CONSTANTLY CHANGING VARIABLE - UPDATING
#-----------------------Settings--------------------------

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

mydb = mysql.connector.connect(
    host=os.environ.get("HOST"),
    user=os.environ.get("USER"),
    password=os.environ.get("PASSWORD"),
    database="mydatabase"
)

amzn_base_url = 'https://www.amazon.com/'

#-----------------------AMZN Class ----------------------------

class AMZN:
    def __init__(self):
        self.browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        self.data = ()

    def passToParser(self):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT p.Link FROM products p, item_data i where p.ProductName=i.ProductName") #LIMIT AT 3 FOR TESTING - PARTITION OUT FOR HEROKU SOMEHOW ----> #NOT NEEDED FOR NOW
        myresult = mycursor.fetchall()
        print(myresult)
        for url in myresult:
            print(url[0])
            self.page_parser(url[0])
        self.browser.quit()

    def page_parser(self, url):
        self.browser.get(url)
        self.data = ()

        try:
            elem = self.browser.find_element_by_css_selector('#ppd')
        except selenium.common.exceptions.NoSuchElementException:
            try:
                elem = self.browser.find_element_by_css_selector('#dp-container')
            except selenium.common.exceptions.NoSuchElementException:
                return

        main = elem.find_element_by_id('centerCol').text
        splitted = main.splitlines()
        temp = 0
        for line in splitted:
            if 'Price: $' in line:
                temp += 1
                if temp == 1:
                    self.data += ((line.split('$')[1]).split(' ')[0],)
                if temp == 2:
                    self.data = ()
                    self.data += ((line.split('$')[1]).split(' ')[0],)
            if 'With Deal: $' in line:
                self.data = ()
                self.data += ((line.split('$')[1]).split(' ')[0],)
        self.data += (url.replace(amzn_base_url, ''),)
        self.updateDatabase()

    def updateDatabase(self):
        #------Passing--------
        mycursor = mydb.cursor()
        if len(self.data) != 2:
            self.data = ('0.00', self.data[0])
        sql = "UPDATE sync_data SET Price = %s WHERE ProductName = %s"  # Insert Ignore allows me to insert products and skip over the duplicates and the error it gives.
        mycursor.execute(sql, self.data)  # data is reversed price first then product name
        mydb.commit()
        print(mycursor.rowcount, "updated in table.")

while True:
    instance = AMZN()
    instance.passToParser()
    time.sleep(900)