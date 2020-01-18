from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import getpass

browser = webdriver.Chrome("*/chromedriver") # locate path of chromedriver

# logging in
browser.get('https://www.instagram.com/')
time.sleep(2)
fb = browser.find_element_by_tag_name('button')
fb.click()
username = browser.find_element_by_id('email')
user = input("Enter username: ")
username.send_keys(user)
password = browser.find_element_by_id('pass')
pw = getpass()
password.send_keys(pw)
enter = browser.find_element_by_id('loginbutton')
enter.click()
time.sleep(2)

# opening up the followers
link = input("Enter website link of your instagram homepage: ")
browser.get(link)
time.sleep(2)

elems = browser.find_elements_by_xpath("//body//div//div[@class=' _2z6nI']//div[@class='v1Nh3 kIKUG  _bz0w']")
for x in elems:
    x.click()
    time.sleep(1)
    browser.find_element_by_xpath("//div[@class = 'Nm9Fw']//button").click()
    time.sleep(1)

    # for scrolling
    usernames = []
    scroll = browser.find_element_by_xpath("//body//div[@class='RnEpo Yx5HN   ']//div//div[2]//div")
    last_height = browser.execute_script("return arguments[0].scrollHeight", scroll)
    while True:
        x = (browser.find_element_by_xpath("//body//div[@class='RnEpo Yx5HN   ']//div//div[2]//div").text).split("\n")
        for i in range(len(x) - 1):
            if i == 0 and x[i] not in usernames:
                usernames.append(x[i])
            elif x[i] in ('Following', 'Follow'):
                if x[i + 1] not in usernames:
                    usernames.append(x[i + 1])
        browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll)
        time.sleep(1)
        new_height = browser.execute_script("return arguments[0].scrollHeight", scroll)
        if new_height == last_height:
            break
        last_height = new_height
    print(usernames)
    browser.find_element_by_class_name('wpO6b ').click()
    browser.find_element_by_class_name('ckWGn').click()
