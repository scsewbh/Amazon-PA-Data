from selenium import webdriver
import time

chromedriver = 'C:\\Users\\scsew\\Desktop\\chromedriver.exe'

options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('window-size=1200x600')  # optional

browser = webdriver.Chrome(executable_path=chromedriver, options=options)

#browser.get('https://www.amazon.com/All-New-Echo-Dot-4th-Gen/dp/B07XJ8C8F5/ref=zg_bs_electronics_home_1?_encoding=UTF8&psc=1&')
browser.get('https://www.amazon.com/All-New-Echo-Dot-4th-Gen/dp/B08GTWC9ZB/ref=zg_bs_electronics_home_1?_encoding=UTF8&th=1')

elem = browser.find_element_by_css_selector('#ppd')

image = elem.find_element_by_id('leftCol')
content = image.find_element_by_class_name('imgTagWrapper')
con = content.find_element_by_tag_name('img')
img_src = con.get_attribute('src')

main = elem.find_element_by_id('centerCol').text
splitted = main.splitlines()
product_name = splitted[0]
print(product_name)
for line in splitted:
    if 'Price: $' in line:
        print(line)
    if 'You Save: $' in line:
        print(line)

browser.quit()


print(img_src)