"""
Functions for the Ipinfo API
https://ipinfo.io/
API Token is needed (free version available with 50.000 requests per month)
!!!Ask the German participants for a Token with ASN-Information!!!
"""

import os
import requests


ip_info_url = "https://ipinfo.io/"
#Your API-Token for ipinfo.io
try:
    ip_info_token = "?token=" + os.getenv('IPINFO_TOKEN')
except Exception as e:
    ip_info_token = ""
    print("No Token found. Please set the IPINFO_TOKEN Environment Variable")
    print("On Linux/Mac:")
    print("export IPINFO_TOKEN=\"your_token\"")
    print("On Windows:")
    print("set IPINFO_TOKEN=\"your_token\"")
    print("")

def get_ip_info(ip_address):
    """
    Get information about an IP Address
    :param: ip_address: IP Address to get information about
    :return: JSON with information about the IP Address
    Structure:
        {
        Geolocation-Information:
            "hostname": string,
            "city": string,
            "region": string,
            "country": string,
            "loc": string,
            "org": string,
            "postal": string,
            "timezone": string,
        ASN-Information:            --works only with paid version--
            "asn":"string",
            "name":"string",
            "domain":"string",
            "route":"string",
            "type":"string"
        }
    """
    response = requests.get(ip_info_url + ip_address + ip_info_token)
    if response.status_code == 200:
        return response.json()
    else:
        return None