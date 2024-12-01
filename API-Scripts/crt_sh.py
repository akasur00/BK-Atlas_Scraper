"""
Functions for crt.sh
https://crt.sh
No API Token needed
"""

import logging
import requests

base_url = "https://crt.sh/json?identity="


def get_domains(domain):
    """
    Get all via certs related domains
    :return: JSON with all domains and info
    Structure:
        [
            {
                "issuer_ca_id": ID of Certificate Authority,
                "issuer_name": issuer of cert (example: "C=DE, O=Charite - Universitaetsmedizin Berlin, OU=IT-Zentrum, CN=Charite CA - G02, emailAddress=pki@charite.de"),
                "common_name": Domain Name,
                "name_value": (example: "hostmaster@charite.de\nwifiswitch-ent03-cevent.charite.de"),
                "id": cert id,
                "entry_timestamp": ,
                "not_before": start of certificate lifetime,
                "not_after": end of certificate lifetime,
                "serial_number": ,
                "result_count": 3
            }, {...}
        ]"""
    response = requests.get(base_url + domain)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def only_domains(domain):
    """
        Get all via certs related domains
        :return: JSON with all domains
    Structure:
        [
            {
                "common_name": Domain Name
            }
        ]
    """
    urls = []
    response = get_domains(domain)
    if response is not None:
        for entry in response:
            urls.append(entry["common_name"])
        return urls
    else:
        return None
