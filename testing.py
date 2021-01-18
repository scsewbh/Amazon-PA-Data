from selenium import webdriver
import time

chromedriver = 'C:\\Users\\scsew\\Desktop\\chromedriver.exe'

options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('window-size=1200x600')  # optional

browser = webdriver.Chrome(executable_path=chromedriver, options=options)

#browser.get('https://www.amazon.com/All-New-Echo-Dot-4th-Gen/dp/B07XJ8C8F5/ref=zg_bs_electronics_home_1?_encoding=UTF8&psc=1&')
browser.get('https://www.amazon.com/TeeTurtle-Reversible-Octopus-Mini-Plush/dp/B07H4YQF3Q/')

elem = browser.find_element_by_css_selector('#ppd')

image = elem.find_element_by_id('leftCol')
content = image.find_element_by_class_name('imgTagWrapper')
con = content.find_element_by_tag_name('img')
img_src = con.get_attribute('src')
product_list = {}
main = elem.find_element_by_id('centerCol').text
splitted = main.splitlines()
product_name = splitted[0]
product_list['name'] = product_name
#ANALYZE IF PRODUCT Had More than one price
temp = 0
for line in splitted:
    if 'Price: $' in line:
        temp += 1
        if temp == 1:
            product_list['price'] = line
        if temp == 2:
            product_list['discounted_price'] = line
    if 'You Save: $' in line:
        product_list['savings'] = line
product_list['img_url'] = img_src
browser.quit()


