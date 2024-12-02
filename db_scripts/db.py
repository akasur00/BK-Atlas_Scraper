import sqlite3
import mysql.connector

# Connection to MySQL-database
conn = mysql.connector.connect(
    host="example.com",
    user="user",
    password="",
    database="mysql"
)

# # SQLite Connection
# conn = sqlite3.connect("VA-database.db")
c = conn.cursor()

schema_name = "GERMAN_HOSPITALS"

c.execute(f"""CREATE SCHEMA IF NOT EXISTS {schema_name} """)
c.execute(f"""CREATE TABLE IF NOT EXISTS {schema_name}.hospitals
                (hospital_ID INTEGER PRIMARY KEY, _name text, link text, hospital_location text)""")

c.execute(f"""CREATE TABLE IF NOT EXISTS {schema_name}.domains
                (domain_id integer primary key, dns_address text, mail bit Default false, 
                hospital integer references {schema_name}.hospitals)""")

c.execute(f"""CREATE TABLE IF NOT EXISTS {schema_name}.related_domains
                (origin_domain integer references {schema_name}.domains, 
                related_domain integer references {schema_name}.domains, 
                Primary Key (origin_domain, related_domain))""")

c.execute(f"""CREATE TABLE IF NOT EXISTS {schema_name}.mx_domains
                (mx_domain_id integer primary key, mx_address text, priority integer, 
                _domain integer references {schema_name}.domains)""")

c.execute(f"""CREATE TABLE IF NOT EXISTS {schema_name}.ASN
                (asn_id integer primary key, _name text)""")

c.execute(f"""CREATE TABLE IF NOT EXISTS {schema_name}.IP_ranges
                (range_id integer primary key, _range text, prefix integer, asn integer references {schema_name}.ASN)""", (schema_name, schema_name,))

c.execute(f"""CREATE TABLE IF NOT EXISTS {schema_name}.IPs
                (IP_ID integer primary key, address text, _domain integer references {schema_name}.domains, 
                mx_domain integer references {schema_name}.mx_domains, 
                ip_range integer references {schema_name}.IP_ranges)""")


# Save hospital information to database
def save_hospital_data(hospital):
    """
    Saves the hospital data to the database.
    :param hospital: Structure: {'name': '', 'link': '', 'location': ''}
    :return hospital_id: Returns id of hospital in database
    """
    c.execute(f"INSERT INTO {schema_name}.hospitals VALUES (?, ?, ?)",
              (hospital['name'], hospital['link'], hospital['city']))
    conn.commit()
    c.execute(f"SELECT hospital_id FROM {schema_name}.hospitals WHERE _name = ? AND link = ? AND hospital_location = ?",
              (hospital['name'], hospital['link'], hospital['city']))
    return c.fetchall()[0]["hospital_id"]


# Save domain information to database
def save_domain_data(domain):
    """
    Saves the domain data to the database. Related to hospital via hospital id
    :param domain: Structure: {'dns_address': '', 'mail': '', 'hospital': ''}
    :return domain_id: Returns id of domain in database
    """
    c.execute(f"INSERT INTO {schema_name}.domains VALUES (?, ?, ?)",
              (domain['dns_address'], domain['mail'], domain['hospital']))
    conn.commit()
    c.execute(f"SELECT domain_id FROM {schema_name}.domains WHERE dns_address = ? AND mail = ? AND hospital = ?",
              (domain['dns_address'], domain['mail'], domain['hospital']))
    return c.fetchall()[0]["domain_id"]


# Save mx domain information to database
def save_mx_domain_data(mx_domain):
    """
    Saves the domain data from the mx record. Related to domain via domain id.
    :param mx_domain: Structure: {'mx_address': '', 'priority': '', 'domain': ''}
    :return mx_domain_id: Returns id of mx domain in database
    """
    c.execute(f"INSERT INTO {schema_name}.mx_domains VALUES (?, ?, ?)",
              (mx_domain['mx_address'], mx_domain['priority'], mx_domain['domain']))
    conn.commit()
    c.execute(f"SELECT mx_domain_id FROM {schema_name}.mx_domains WHERE mx_address = ? AND priority = ? AND _domain = ?",
              (mx_domain['mx_address'], mx_domain['priority'], mx_domain['domain']))
    return c.fetchall()[0]["mx_domain_id"]


# Save asn information to database
def save_asn_data(asn):
    """
    Saves the asn data to the database.
    :param asn: Structure: {'asn_id': '', 'name': ''}
    :return asn_id: Returns id of asn in database
    """
    c.execute(f"INSERT INTO {schema_name}.asn VALUES (?, ?)",
              (asn['asn_id'], asn['name']))
    conn.commit()
    return asn["asn_id"]


# Save ip range information to database
def save_ip_range_data(ip_range):
    """
    Saves the ip_range data to the database.
    :param ip_range: Structure: {'range': '', 'prefix': '', 'asn': ''}
    :return range_id: Returns id of ip_range in database
    """
    c.execute(f"INSERT INTO {schema_name}.ip_ranges VALUES (?, ?, ?)",
              (ip_range['range'], ip_range['prefix'], ip_range['asn']))
    conn.commit()
    c.execute(f"SELECT range_id FROM {schema_name}.ip_ranges WHERE _range = ? AND prefix = ? AND asn = ?",
              (ip_range['range'], ip_range['prefix'], ip_range['asn']))
    return c.fetchall()[0]["range_id"]


# Save ip information to database
def save_ip_data(ip):
    c.execute(f"INSERT INTO {schema_name}.ips VALUES (?, ?, ?, ?)",
              (ip['address'], ip['_domain'], ip['mx_domain'], ip['ip_range']))
    conn.commit()
    c.execute(f"SELECT ip_id FROM {schema_name}.ips WHERE address = ? AND _domain = ? AND mx_domain = ? AND ip_range = ?",
              (ip['address'], ip['_domain'], ip['mx_domain'], ip['ip_range']))
    return c.fetchall()[0]["ip_id"]


# Save information of related domains to database (crt.sh)
def save_related_domains(domains):
    c.execute(f"INSERT INTO {schema_name}.related_domains VALUES (?, ?)",
              (domains['origin'], domains['related_domain']))
    conn.commit()


a = save_hospital_data({'name': 'test', 'link': 'test', 'location': 'test'})
print(a)

conn.close()
