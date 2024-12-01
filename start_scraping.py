'''
Starting Script to get a Database with the following Infos:
    Structure:
        name:               name of the Hospital
        link:               link to the individual hospital web site
        dns_record:         dns record, scraped from the individual site
        dns_address:        ip address after dns lookup of the dns record
        mx_hostname:        hostname of the mx lookup of the dns record
        mx_address:         ip address after dns lookup of the hostname
        mail_domain:        domain of the mail address
        mail_domain_address:ip address after dns lookup of the mail domain
        hospital_location:  location of the hospital from the API
'''

import sqlite3
import urllib.request
import bs4
import api_scripts.bundesklinikatlas
import lookups

#SQLite Connection
conn = sqlite3.connect("bk-a.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS GERMAN_HOSPITALS
                (name text, link text, dns_record text, dns_address text, mx_hostname text, mx_address text, mail_domain text, mail_domain_address text, hospital_location text)""")

#Get all hospitals as JSON from the Bundesklinik Atlas API
hospitals_json = api_scripts.bundesklinikatlas.get_all_hospitals()

#Main Loop to get further information and save it to the database
#hospitals_json = hospitals_json[:10] #Limit to 10 for testing
for hospital in hospitals_json:

    #Scrape information from individual Website
    try:
        html = urllib.request.urlopen(hospital['link']).read().decode("utf-8")
        soup = bs4.BeautifulSoup(html, 'html.parser')
        dns_element = soup.find('a', {'class': 'u-icon--icon-link-extern'})

        #If Dns Element is found, resolve to AAAA Record and MX Record
        if dns_element is not None:
            dns_record = dns_element.text
            #get IP for dns record
            try:
                dns_address = lookups.dns_lookup(dns_record)
            except Exception as e:
                dns_address = None

            #get MX record and IP from MX
            try:
                mx_hostname = lookups.mx_lookup(dns_record)
                mx_address = lookups.dns_lookup(mx_hostname)
            except Exception as e:
                mx_hostname = None
                mx_address = None
        else:
            dns_record, dns_address, mx_hostname, mx_address = None, None, None, None

        #get the Mail Domain from the Website
        mail_domain = hospital['mail'].split('@')[-1] if '@' in hospital['mail'] else None

        if mail_domain is not None:
            mail_domain_address = lookups.dns_lookup(mail_domain)
        else:
            mail_domain_address = None

        #Save information to database
        c.execute("INSERT INTO GERMAN_HOSPITALS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (hospital['name'], hospital['link'], dns_record, dns_address, mx_hostname, mx_address, mail_domain, mail_domain_address, hospital['city']))
        conn.commit()

    except Exception as e:
        print(f"Failed to get information for {hospital['name']}")
        print(e)
conn.close()