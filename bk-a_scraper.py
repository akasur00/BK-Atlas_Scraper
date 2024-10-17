import logging
import sqlite3
import urllib
from selenium import webdriver
from selenium.webdriver.common.by import By

import bs4

#Add dnslookups from dns records
#Add ip location of the webserver

url = "https://bundes-klinik-atlas.de/krankenhaussuche/?searchtype=free-search"

#SQLite Connection
conn = sqlite3.connect("bk-a.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS GERMAN_HOSPITALS
                (dns_name text, ip_address text, name text, location text, cases integer, public boolean)""")

logger = logging.getLogger()
logging.basicConfig(filename='./Logs/bk-a.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

logger.info("<-- Script started -->")

def has_next_page(soup):
    return soup.find('a', string='next') is not None

def get_all_hospitals(url):
    try:
        logger.info(f"Requesting {url}")
        driver = webdriver.Chrome()
        driver.get(url)
        driver.find_element("id", "free-search").click()
        driver.implicitly_wait(1)
        driver.find_element(By.CLASS_NAME, "ce-search-result-list-item")
        html = driver.page_source
        soup = bs4.BeautifulSoup(html, 'html.parser')
        hospitals = soup.find_all('a', {'class': 'c-link'})
        print(hospitals)


        response = urllib.request.urlopen(url)
        html = response.read().decode("utf-8")
        soup = bs4.BeautifulSoup(html, 'html.parser')
    except Exception as e:
        logger.error(f"Script failed for {url}\n", exc_info=True)

get_all_hospitals(url)