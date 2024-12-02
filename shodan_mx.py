'''
script for getting shodan information of mx records
'''

import os
import sqlite3

import requests

shodan_base_url = "https://api.shodan.io/shodan/host/"
shodan_api_token = "?key=" + "2qnS9XmgmmGTNiOP39l5k3fzxPaLHwwy"

#SQLite Connection
conn = sqlite3.connect("bk-a.db")
c = conn.cursor()

c.execute("SELECT mx_address FROM GERMAN_HOSPITALS WHERE mx_address IS NOT NULL")

mx_addresses = c.fetchall()
for address in mx_addresses:
    try:
        print (shodan_base_url + address[0] + shodan_api_token)
        response = requests.get(shodan_base_url + address[0] + shodan_api_token)
        if response.status_code == 200:
            print(response.json()['tags'])
    except Exception as e:
        print(e)

