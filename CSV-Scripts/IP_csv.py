import sqlite3

#SQLite Connection
conn = sqlite3.connect("../bk-a.db")
c = conn.cursor()

#Get all data from the database
c.execute("SELECT ip_address FROM GERMAN_HOSPITALS")
rows = c.fetchall()

#Write data to CSV
with open("csv/bk-a_ip-addresses.csv", "w") as f:
    for row in rows:
        if row[0] != "NULL":
            f.write(row[0] + "\n")