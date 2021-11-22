from selenium import webdriver
import os
import schedule
import time

from selenium.webdriver.chrome.options import Options
from coin_test_script import get_price
from parser import update_csv
import datetime, requests, os, shutil, time, unicodedata, sys
from time import sleep


url = "https://www.wonderland.money/"
api_key = os.environ['key']



def job():
    try:
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(url)
        driver.maximize_window()

        time.sleep(5)

        current_time = datetime.datetime.now()

        page_source = driver.page_source

        with open("test.html", "w") as f:
            f.write(driver.page_source)
            
        print(f"refreshed on {current_time}")

        get_price(api_key)

        update_csv("test.csv")
        driver.close()
    except:
        print(f'error at {current_time}')

# time is in utc, not eastern
schedule.every().day.at("14:00").do(job)
schedule.every().day.at("22:00").do(job)
schedule.every().day.at("06:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)