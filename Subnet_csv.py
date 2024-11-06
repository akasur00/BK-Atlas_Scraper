import sqlite3
import requests

#Trying out the hackertarget API to get the subnet of an IP
#Only 50 requests per day for free users

base_url = "https://api.hackertarget.com/aslookup/"

#SQLite Connection
conn = sqlite3.connect("bk-a.db")
c = conn.cursor()

#Get all data from the database
c.execute("SELECT ip_address FROM GERMAN_HOSPITALS")
rows = c.fetchall()

#Write data to CSV
with open("bk-a_subnets.csv", "w") as f:
    for row in rows:
        if row[0] != "NULL":
            response = requests.get(base_url + f"?q={row[0]}&output=json")
            if response.status_code == 200:
                data = response.json()
                f.write(data['asn_range'] + "\n")
            else:
                print (f"Failed to get subnet for {row[0]} with status code {response.status_code}")