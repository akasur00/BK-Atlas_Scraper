"""
Functions for the Hackertarget ASN API
https://hackertarget.com/as-ip-lookup/
No API Token needed (50 Requests per day)
"""

import requests

base_url = "https://api.hackertarget.com/aslookup/"

def get_asn(ip_address):
    """
    Get the ASN for an IP Address
    :param: ip_address: IP Address to get the ASN for
    :return: JSON with information about the ASN
    Structure:
        {
            "asn": string,
            "asn_org": string,
            "asn_range": string,
            "ip": string
    """
    response = requests.get(base_url + f"?q={ip_address}&output=json")
    if response.status_code == 200:
        return response.json()
    else:
        return None