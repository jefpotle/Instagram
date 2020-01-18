from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import getpass

# logging in
browser = webdriver.Chrome("*/chromedriver") # locate path for chromedriver
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

RATE_LIMIT = 0
RATE_LIMIT_STOP = 10000
RATE_LIMIT_SLEEP = 1000
# opening up the followers
link = input("Enter website link of your instagram homepage: ")
browser.get(link)
time.sleep(2)
followers = browser.find_elements_by_class_name('-nal3 ')
followers[1].click()
time.sleep(2)

# scrolling infinitely and grabbing followers
scroll = browser.find_element_by_class_name("isgrP")
last_height = browser.execute_script("return arguments[0].scrollHeight", scroll)
while True:
    browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll)
    time.sleep(1)
    new_height = browser.execute_script("return arguments[0].scrollHeight", scroll)
    if new_height == last_height:
        break
    last_height = new_height
    RATE_LIMIT += 1
    if RATE_LIMIT == RATE_LIMIT_STOP:
        time.sleep(RATE_LIMIT_SLEEP)
        RATE_LIMIT = 0

# scraping data for followers
elems = browser.find_elements_by_xpath("//body//div[@class='PZuss']//a[@class='FPmhX notranslate  _0imsa ']")
followers = {}
for x in elems:
    followers[x.text] = 0
    RATE_LIMIT += 1
    if RATE_LIMIT == RATE_LIMIT_STOP:
        time.sleep(RATE_LIMIT_SLEEP)
        RATE_LIMIT = 0

# scraping data for posts
browser.get(link)
time.sleep(2)
posts = browser.find_elements_by_xpath("//body//div//div[@class=' _2z6nI']//div[@class='v1Nh3 kIKUG  _bz0w']")
for x in posts:
    x.click()
    time.sleep(1)
    browser.find_element_by_xpath("//div[@class = 'Nm9Fw']//button").click()
    time.sleep(1)
    usernames = []
    scroll = browser.find_element_by_xpath("//body//div[@class='RnEpo Yx5HN   ']//div//div[2]//div")
    last_height = browser.execute_script("return arguments[0].scrollHeight", scroll)
    while True:
        x = (browser.find_element_by_xpath("//body//div[@class='RnEpo Yx5HN   ']//div//div[2]//div").text).split("\n")
        for i in range(len(x) - 1):
            RATE_LIMIT += 1
            if RATE_LIMIT == RATE_LIMIT_STOP:
                time.sleep(RATE_LIMIT_SLEEP)
                RATE_LIMIT = 0
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
    for users in usernames:
        try:
            followers[users] += 1
        except:
            try:
                followers[users + 'unfollowed'] += 1
            except:
                followers[users + 'unfollowed'] = 0
    browser.find_element_by_class_name('wpO6b ').click()
    browser.find_element_by_class_name('ckWGn').click()
browser.close()
f = open("followersanalysis.csv", "a")
for x in followers:
    f.write(str(x) + "," + str(followers[x]))
f.close()
