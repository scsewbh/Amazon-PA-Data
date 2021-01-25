from bs4 import BeautifulSoup as bs
import mysql.connector
from selenium import webdriver
import selenium.common.exceptions
import os

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
'''
mycursor = mydb.cursor() #mycursor.execute("CREATE DATABASE mydatabase") 
mycursor.execute("CREATE TABLE products (ProductName VARCHAR(200) PRIMARY KEY, Link TEXT)") 
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
amzn_1 = 'https://www.amazon.com/Best-Sellers-Beauty-Skin-Care-Products/zgbs/beauty/11060451/'
amzn_2 = 'https://www.amazon.com/gp/new-releases/electronics/'
amzn_3 = 'https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/'


amzn_wishedFor = [amzn_Elec_url, amzn_VideoGame_url, amzn_CellAccessories_url, amzn_PC_url, amzn_HPC_url, amzn_Skincare_url, amzn_HI_url, amzn_Office_url, amzn_1, amzn_2, amzn_3]

#-----------------------AMZN Class ----------------------------

class AMZN:
    def __init__(self):
        self.browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        self.data = []
        self.page_data = {}
        self.item_dataHolder = ()
        self.sync_dataHolder = ()
        self.item_data_names = ['name', 'price', 'img_url', 'product_id']
        self.sync_data_names = ['product_id', 'discounted_price']

    #--------------------------------ADDING TO DB---------------------------------
    def passToDatabase(self):
        mycursor = mydb.cursor()
        sql = "INSERT IGNORE INTO products (ProductName, Link) VALUES (%s, %s)"
        #Insert Ignore allows me to insert products and skip over the duplicates and the error it gives.
        mycursor.executemany(sql, self.data)
        mydb.commit()
        print(mycursor.rowcount, "was inserted to table.")

    def results(self, listUrl):
        self.data = []
        self.browser.get(listUrl)
        listData = self.browser.page_source
        soup = bs(listData, 'html.parser')
        a = soup.find_all('a', class_='a-link-normal a-text-normal')

        for parLink in a:
            pHref = parLink['href'].split('?_encoding=')[0]
            if '/ref=' in pHref:
                pHref = pHref.split('/ref=')[0]
            self.data.append((pHref, amzn_base_url + pHref))
        self.passToDatabase()

    def page_with_list(self, page_urls):
        #Takes the array of pages that are list eg: bestsellers, new releases
        for url in page_urls:
            self.results(url)
        self.browser.quit()

    #------------------------------PARSING----------------------------------------
    def passToParser(self):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT Link FROM products") #LIMIT AT 3 FOR TESTING - PARTITION OUT FOR HEROKU SOMEHOW
        myresult = mycursor.fetchall()
        for url in myresult:
            print(url[0])
            self.page_parser(url[0])
        self.browser.quit()

    def page_parser(self, url):
        self.browser.get(url)
        self.page_data = {}
        try:
            elem = self.browser.find_element_by_css_selector('#ppd')
        except selenium.common.exceptions.NoSuchElementException:
            try:
                elem = self.browser.find_element_by_css_selector('#dp-container')
            except selenium.common.exceptions.NoSuchElementException:
                return

        try:
            image = elem.find_element_by_id('leftCol')
            content = image.find_element_by_class_name('imgTagWrapper')
            con = content.find_element_by_tag_name('img')
            img_src = con.get_attribute('src')
        except selenium.common.exceptions.NoSuchElementException:
            img_src = 'No Image'

        main = elem.find_element_by_id('centerCol').text
        splitted = main.splitlines()
        product_name = splitted[0]
        self.page_data['name'] = product_name
        temp = 0
        for line in splitted:
            if 'Price: $' in line:
                temp += 1
                if temp == 1:
                    self.page_data['price'] = (line.split('$')[-1]).split(' ')[0]
                if temp == 2:
                    self.page_data['discounted_price'] = (line.split('$')[-1]).split(' ')[0]
            if 'Was: $' in line:
                temp += 1
                self.page_data['price'] = (line.split('$')[-1]).split(' ')[0]
            if 'With Deal: $' in line:
                self.page_data['discounted_price'] = (line.split('$')[-1]).split(' ')[0]
            if 'price' not in self.page_data:
                self.page_data['price'] = 'Not Listed'
        self.page_data['img_url'] = img_src
        self.page_data['product_id'] = url.replace(amzn_base_url, '')
        self.dataOrganizer()
        self.passProductsToDBs()
        '''
        for elem in self.page_data:
            print(elem, self.page_data[elem])
        '''

    #INITIAL PASS SETUP
    def dataOrganizer(self):
        self.item_dataHolder = ()
        self.sync_dataHolder = ()
        for value in self.item_data_names:
            if value in self.page_data:
                self.item_dataHolder += (self.page_data[value],)
            else:
                self.item_dataHolder += (None,)

        for value in self.sync_data_names:
            if value in self.page_data:
                self.sync_dataHolder += (self.page_data[value],)
            elif value == 'discounted_price':
                self.sync_dataHolder += (self.page_data['price'],)
            else:
                self.sync_dataHolder += (None,)

    def passProductsToDBs(self):
        # item_data (Name TEXT, Price DECIMAL(5,2), Img_URL TEXT, ProductName VARCHAR(255), PRIMARY KEY (ProductName), FOREIGN KEY (ProductName) REFERENCES products(ProductName))")
        # sync_data (ProductName VARCHAR(255), Price DECIMAL(5,2), Savings TINYINT, PRIMARY KEY (ProductName), FOREIGN KEY (ProductName) REFERENCES products(ProductName))")

        mycursor = mydb.cursor()
        sql = "INSERT IGNORE INTO item_data (Name, Price, Img_URL, ProductName) VALUES (%s, %s, %s, %s)"  # Insert Ignore allows me to insert products and skip over the duplicates and the error it gives.
        mycursor.execute(sql, self.item_dataHolder)
        mydb.commit()

        #---------------------------------------------------------

        mycursor = mydb.cursor()
        sql = "INSERT IGNORE INTO sync_data (ProductName, Price) VALUES (%s, %s)"  # Insert Ignore allows me to insert products and skip over the duplicates and the error it gives.
        mycursor.execute(sql, self.sync_dataHolder)
        mydb.commit()




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

pages = ['https://www.amazon.com/Best-Sellers-Amazon-Launchpad/zgbs/boost/', 'https://www.amazon.com/Best-Sellers-Beauty-Skin-Care-Products/zgbs/beauty/11060451/']

instance.page_with_list(pages)
'''
#ONLY ONE SESSION OF SELENIUM AT A TIME

instance = AMZN()
instance.page_with_list(amzn_wishedFor)

instance2 = AMZN()
instance2.passToParser()
