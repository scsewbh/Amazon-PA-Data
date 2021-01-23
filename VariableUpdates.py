from bs4 import BeautifulSoup as bs
import mysql.connector
from selenium import webdriver

#CONSTANTLY CHANGING VARIABLE - UPDATING
#-----------------------Settings--------------------------

chromedriver = 'C:\\Users\\scsew\\Desktop\\chromedriver.exe'

options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('window-size=1200x600')  # optional

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="mydatabase"
)
'''
mycursor = mydb.cursor() #mycursor.execute("CREATE DATABASE mydatabase") 
mycursor.execute("CREATE TABLE products (ProductName VARCHAR(255) PRIMARY KEY, Link TEXT)") 
#mycursor.execute("CREATE TABLE item_data (Name TEXT, Price DECIMAL(5,2), Img_URL TEXT, ProductName VARCHAR(255), PRIMARY KEY (ProductName), FOREIGN KEY (ProductName) REFERENCES products(ProductName))") 
#mycursor.execute("CREATE TABLE sync_data (ProductName VARCHAR(255), Price DECIMAL(5,2), PRIMARY KEY (ProductName), FOREIGN KEY (ProductName) REFERENCES products(ProductName))") 
mycursor.execute("SHOW TABLES") 
mycursor.execute("DROP TABLE products") 

mycursor.execute("SELECT * FROM products")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)
'''

#------------------------Initial Variables--------------------------------

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

#-----------------------AMZN Class ----------------------------

class AMZN:
    def __init__(self):
        self.trigger = 0
        self.browser = webdriver.Chrome(executable_path=chromedriver, options=options)
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

        image = elem.find_element_by_id('leftCol')
        content = image.find_element_by_class_name('imgTagWrapper')
        con = content.find_element_by_tag_name('img')
        img_src = con.get_attribute('src')
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
        print(self.data)
        mycursor.execute(sql, self.data)  # data is reversed price first then product name
        mydb.commit()
        self.trigger += mycursor.rowcount
        print(mycursor.rowcount, "updated in table.")
        if self.trigger > 0:
            self.trigger = 0
            self.SELECTFUNCTION




AMZN()