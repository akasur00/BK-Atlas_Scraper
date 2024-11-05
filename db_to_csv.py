import sqlite3

#SQLite Connection
conn = sqlite3.connect("bk-a.db")
c = conn.cursor()

#Get all data from the database
c.execute("SELECT * FROM GERMAN_HOSPITALS")
rows = c.fetchall()

#Write data to CSV
with open("bk-a.csv", "w") as f:
    f.write("name,dns_name,ip_address,ip_location,ip_region,ip_org,mail_domain,hospital_location,cases\n")
    for row in rows:
        f.write(",".join([str(x) for x in row]) + "\n")