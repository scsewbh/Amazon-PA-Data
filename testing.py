from selenium import webdriver
import time

chromedriver = 'C:\\Users\\scsew\\Desktop\\chromedriver.exe'

options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('window-size=1200x600')  # optional

browser = webdriver.Chrome(executable_path=chromedriver, options=options)

browser.get('https://www.amazon.com/All-New-Echo-Dot-4th-Gen/dp/B07XJ8C8F5/ref=zg_bs_electronics_home_1?_encoding=UTF8&psc=1&')
html = browser.page_source
#html = browser.execute_script("return document.documentElement.innerHTML;")
browser.quit()

print(html)