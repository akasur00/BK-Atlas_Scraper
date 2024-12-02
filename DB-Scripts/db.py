import sqlite3

# SQLite Connection
conn = sqlite3.connect("VA-database.db")
c = conn.cursor()

schema_name = "GERMAN _HOSPITALS"

c.execute("""CREATE SCHEMA IF NOT EXISTS ?""", (schema_name,))
c.execute("""CREATE TABLE IF NOT EXISTS ?.hospitals
                (hospital_ID INTEGER PRIMARY KEY, _name text, link text, hospital_location text)""", (schema_name,))

c.execute("""CREATE TABLE IF NOT EXISTS ?.domains
                (domain_id integer primary key, dns_address text, mail bit Default false, 
                hospital integer references hospitals)""", (schema_name,))

c.execute("""CREATE TABLE IF NOT EXISTS ?.mx_domains
                (mx_domain_id integer primary key, mx_address text, priority integer, 
                _domain integer references domains)""", (schema_name,))

c.execute("""CREATE TABLE IF NOT EXISTS ?.ASN
                (asn_id integer primary key, _name text)""", (schema_name,))

c.execute("""CREATE TABLE IF NOT EXISTS ?.IP_ranges
                (range_id integer primary key, _range text, prefix integer, asn integer references ASN)""", (schema_name,))

c.execute("""CREATE TABLE IF NOT EXISTS ?.IPs
                (IP_ID integer primary key, address text, _domain integer references domains, 
                mx_domain integer references mx_domains, ip_range integer references IP_ranges)""",
          (schema_name,))


# Save hospital information to database
def save_hospital_data(hospital):
    c.execute("INSERT INTO ?.hospitals VALUES (?, ?, ?)",
              (schema_name, hospital['name'], hospital['link'], hospital['city']))
    conn.commit()
    c.execute("SELECT hospital_id FROM ?.hospitals WHERE _name = ? AND link = ? AND city = ?",
              (schema_name, hospital['name'], hospital['link'], hospital['city']))
    return c.fetchall()[0]["hospital_id"]


# Save domain information to database
def save_domain_data(domain):
    c.execute("INSERT INTO ?.domains VALUES (?, ?, ?)",
              (schema_name, domain['dns_address'], domain['mail'], domain['hospital']))
    conn.commit()
    c.execute("SELECT domain_id FROM ?.domains WHERE dns_address = ? AND mail = ? AND hospital = ?",
              (schema_name, domain['dns_address'], domain['mail'], domain['hospital']))
    return c.fetchall()[0]["mx_domain_id"]


# Save mx domain information to database
def save_mx_domain_data(mx_domain):
    c.execute("INSERT INTO ?.mx_domains VALUES (?, ?, ?)",
              (schema_name, mx_domain['mx_address'], mx_domain['priority'], mx_domain['domain']))
    conn.commit()
    c.execute("SELECT mx_domain_id FROM ?.mx_domains WHERE mx_address = ? AND priority = ? AND _domain = ?",
              (schema_name, mx_domain['mx_address'], mx_domain['priority'], mx_domain['domain']))
    return c.fetchall()[0]["mx_domain_id"]


# Save asn information to database
def save_asn_data(asn):
    c.execute("INSERT INTO ?.asn VALUES (?, ?)",
              (schema_name, asn['asn_id'], asn['name']))
    conn.commit()
    return asn["asn_id"]


# Save ip range information to database
def save_ip_range_data(ip_range):
    c.execute("INSERT INTO ?.ip_ranges VALUES (?, ?, ?)",
              (schema_name, ip_range['range'], ip_range['prefix'], ip_range['asn']))
    conn.commit()
    c.execute("SELECT range_id FROM ?.ip_ranges WHERE _range = ? AND prefix = ? AND asn = ?",
              (schema_name, ip_range['range'], ip_range['prefix'], ip_range['asn']))
    return c.fetchall()[0]["range_id"]


# Save ip information to database
def save_ip_data(ip):
    c.execute("INSERT INTO ?.ips VALUES (?, ?, ?, ?)",
              (schema_name, ip['address'], ip['_domain'], ip['mx_domain'], ip['ip_range']))
    conn.commit()
    c.execute("SELECT ip_id FROM ?.ips WHERE address = ? AND _domain = ? AND mx_domain = ? AND ip_range = ?",
              (schema_name, ip['address'], ip['_domain'], ip['mx_domain'], ip['ip_range']))
    return c.fetchall()[0]["ip_id"]


conn.close()
