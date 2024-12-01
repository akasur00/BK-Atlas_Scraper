import os
import sqlite3
import urllib.request

import bs4
import requests
import socket

import api_scripts.Ipinfo, api_scripts.bundesklinikatlas

#SQLite Connection
conn = sqlite3.connect("bk-a.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS GERMAN_HOSPITALS
                (name text, dns_name text, ip_address text, ip_location text, ip_region text, ip_org text, mail_domain text, hospital_location text, cases integer)""")

#Get all hospitals as JSON from the Bundesklinik Atlas API
hospitals_json = api_scripts.bundesklinikatlas.get_all_hospitals()

#Main Loop to get further information and save it to the database
hospitals_json = hospitals_json[:10] #Limit to 10 for testing
for hospital in hospitals_json:

    #Scrape information from individual Website
    try:
        html = urllib.request.urlopen(hospital['link']).read().decode("utf-8")
        soup = bs4.BeautifulSoup(html, 'html.parser')
        dns_element = soup.find('a', {'class': 'u-icon--icon-link-extern'})

        #If Dns Element is found, resolve to AAAA Record and MX Record
        if dns_element is not None:
            dns_name = dns_element.text
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