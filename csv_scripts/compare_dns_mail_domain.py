'''
Testing-Script to compare to columns and write differences to a CSV
'''


import sqlite3

conn = sqlite3.connect("../bk-a.db")
c = conn.cursor()

#Get all data from the database
c.execute("SELECT name, dns_address, mail_domain_address FROM GERMAN_HOSPITALS")
rows = c.fetchall()

#Write data to CSV
with open("csv/compare.csv", "w") as f:
    for row in rows:
        if row[1] != row[2]:
            f.write(row[0] + "\n")