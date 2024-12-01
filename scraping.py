import logging
import os
import sqlite3
import urllib

import bs4
import requests
import socket

base_url = "https://klinikatlas.api.proxy.bund.dev"
all_hospitals_url = "/fileadmin/json/locations.json"
ip_info_url = "https://ipinfo.io/"
#Your API-Token for ipinfo.io
ip_info_token = "?token=" + os.getenv('IPINFO_TOKEN')

#SQLite Connection
conn = sqlite3.connect("bk-a.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS GERMAN_HOSPITALS
                (name text, dns_name text, ip_address text, ip_location text, ip_region text, ip_org text, mail_domain text, hospital_location text, cases integer)""")

#Get all hospitals as JSON
response = requests.get(base_url + all_hospitals_url)
hospitals_data = response.json()

#Main Loop to get all information
#hospitals_data = hospitals_data[:10] #Limit to 10 for testing
for hospitals_data in hospitals_data:
    try:
        #Request HTML Page for DNS Name and number of cases
        html = urllib.request.urlopen(hospitals_data['link']).read().decode("utf-8")
        soup = bs4.BeautifulSoup(html, 'html.parser')
        dns_element = soup.find('a', {'class': 'u-icon--icon-link-extern'})

        if dns_element is not None:
            dnsname = dns_element.text
            # Get IP Address for DNS
            try:
                ip_address = socket.gethostbyname(dnsname) #TODO: get MX record for mail server
            except Exception as e:
                ip_address = "NULL"
            # Get IP Location
            try:
                ip_info = requests.get(ip_info_url + ip_address + ip_info_token).json()
                ip_location = ip_info['city']
                ip_region = ip_info['region']
                ip_org = ip_info['org']
            except Exception as e:
                ip_location, ip_region, ip_org = "NULL", "NULL", "NULL"

        else:
            dnsname, ip_address, ip_region, ip_org = "NULL", "NULL", "NULL", "NULL"

        cases = soup.find('div', {'class': 'c-tacho-text__text'}).text.split(' ')[0] #TODO: save without point as integer
        maildomain = hospitals_data['mail'].split('@')[-1] if '@' in hospitals_data['mail'] else "NULL"


        #Save information to database
        c.execute("INSERT INTO GERMAN_HOSPITALS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (hospitals_data['name'], dnsname, ip_address, ip_location, ip_region, ip_org, maildomain, hospitals_data['city'], cases))
        conn.commit()

    except Exception as e:
        print(f"Failed to get information for {hospitals_data['name']}")
        print(e)
conn.close()