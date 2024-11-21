"""
Functions for the Ipinfo API
https://ipinfo.io/
API Token is needed (free version available with 50.000 requests per month)
"""

import logging
import os
import requests


logger = logging.getLogger()
logging.basicConfig(filename='./logs/ipinfo.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

ip_info_url = "https://ipinfo.io/"
#Your API-Token for ipinfo.io
ip_info_token = "?token=" + os.getenv('IPINFO_TOKEN')
"""
On Linux/Mac:
export IPINFO_TOKEN="your_token"
On Windows:
set IPINFO_TOKEN="your_token"
"""


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
        logger.info(f"got IP information for {ip_address}")
        return response.json()
    else:
        logger.error(f"Failed to get IP information for {ip_address}, statuscode {response.status_code}\n", exc_info=True)
        return None
