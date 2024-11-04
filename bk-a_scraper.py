import logging
import sqlite3
import requests

#Add dnslookups from dns records
#Add ip location of the webserver

url = "https://bundes-klinik-atlas.de/searchresults/"
params = {
    "tx_solr[start]": 0,
    "tx_solr[rows]": 20,
    "searchtype": "free-search",
    "tx_solr[sort]": "header,desc"
}
headers = {
    "Accept": "application/json"
}

#SQLite Connection
conn = sqlite3.connect("bk-a.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS GERMAN_HOSPITALS
                (dns_name text, ip_address text, name text, mail_domain text, location text, cases integer, public boolean)""")

logger = logging.getLogger()
logging.basicConfig(filename='./Logs/bk-a.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

logger.info("<-- Script started -->")

def get_all_hospitals():
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Request failed with status code {response.status_code}")