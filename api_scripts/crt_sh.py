"""
Functions for crt.sh
https://crt.sh
No API Token needed
"""

import logging
import requests

base_url = "https://crt.sh/json?identity="

logger = logging.getLogger()
logging.basicConfig(filename='./logs/crt-sh.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


def get_domains(domain):
    """
    Get all via certs related domains
    :return: JSON with all domains
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
        logger.info(f"got {len(response.json())} returns from {base_url + domain}")
        return response.json()
    else:
        logger.error(f"Failed to get any returns from {base_url + domain}, statuscode {response.status_code}\n",
                     exc_info=True)
        return None
