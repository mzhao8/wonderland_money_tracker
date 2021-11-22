from selenium import webdriver
import os
import schedule
import time

from selenium.webdriver.chrome.options import Options
from coin_test_script import get_wonderland_price, get_snowbank_price
from parser import update_csv_wonderland, update_csv_snowbank
import datetime, requests, os, shutil, time, unicodedata, sys
from time import sleep


url_dict = {"wonderland":"https://www.wonderland.money/", "snowbank": "https://dapp.snowbank.finance/#/dashboard"}
api_key = os.environ['key']



def wonderland_job():
    try:
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(url_dict['wonderland'])
        driver.maximize_window()

        time.sleep(5)

        current_time = datetime.datetime.now()

        #page_source = driver.page_source

        with open("wonderland.html", "w") as f:
            f.write(driver.page_source)
            
        print(f"refreshed on {current_time}")

        get_wonderland_price(api_key)

        update_csv_wonderland("test.csv")
        driver.close()
    except:
        print(f'error at {current_time}')

def snowbank_job():
    try:
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(url_dict['snowbank'])
        driver.maximize_window()

        time.sleep(5)

        current_time = datetime.datetime.now()

        #page_source = driver.page_source

        with open("snowbank.html", "w") as f:
            f.write(driver.page_source)
            
        print(f"refreshed on {current_time}")

        #get_snowbank_price(api_key)

        update_csv_snowbank("test.csv")
        driver.close()
    except:
        print(f'error at {current_time}')


snowbank_job()
'''
# time is in utc, not eastern
schedule.every().day.at("14:00").do(wonderland_job)
schedule.every().day.at("22:00").do(wonderland_job)
schedule.every().day.at("06:00").do(wonderland_job)

while True:
    schedule.run_pending()
    time.sleep(1)

'''