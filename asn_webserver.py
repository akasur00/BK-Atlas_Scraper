'''
This script is used to get the informations about the ASN via the ipinfo.io API.
'''

import api_scripts.ipinfo
import sqlite3

#SQLite Connection
conn = sqlite3.connect("bk-a.db")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS ASN_WEBSERVER (dns text, asn text)""")

#Get all hospitals from the database
c.execute("SELECT name, dns_address FROM GERMAN_HOSPITALS")

for hospital in c.fetchall():
    #Get the ASN Information from the ipinfo.io API
    try:
        ip_info = api_scripts.ipinfo.get_ip_info(hospital[1])
        if ip_info is not None:
            asn = ip_info['org']
        else:
            asn = None
    except Exception as e:
        asn = None

    #Update the Database
    c.execute("INSERT INTO ASN_WEBSERVER VALUES (?, ?)", (hospital[0], asn))
    conn.commit()

#Write all Distinct ASNs into a new Table
c.execute("Create TABLE IF NOT EXISTS ASN (asn text, count integer)")
c.execute("SELECT DISTINCT asn FROM ASN_WEBSERVER")
for asn in c.fetchall():
    c.execute("SELECT COUNT(*) FROM ASN_WEBSERVER WHERE asn = ?", (asn[0],))
    count = c.fetchone()[0]
    c.execute("INSERT INTO ASN VALUES (?, ?)", (asn[0], count))
conn.commit()
conn.close()