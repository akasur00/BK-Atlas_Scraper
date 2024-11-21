"""
Functions for the Bundesklinik Atlas API
https://klinikatlas.bmg.api.bund.dev/
No API Token needed
"""

import logging
import urllib.request
import requests

base_url = "https://klinikatlas.api.proxy.bund.dev"
all_hospitals_url = "/fileadmin/json/locations.json"

logger = logging.getLogger()
logging.basicConfig(filename='./logs/bundesklinik-atlas.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

def get_all_hospitals():
    """
    Get all hospitals from the Bundesklinik Atlas API
    :return: JSON with all hospitals
    Structure:
        [
            {
                "name": string,
                "street": string,
                "city": string,
                "zip": string,
                "phone": string,
                "mail": string,
                "beds_number": integer,
                "latitude": string,
                "longitude": string,
                "link": string
            }, {...}
    """
    response = requests.get(base_url + all_hospitals_url)
    if response.status_code == 200:
        logger.info(f"got {len(response.json())} hospitals from {base_url + all_hospitals_url}")
        return response.json()
    else:
        logger.error(f"Failed to get any hospitals from {base_url + all_hospitals_url}, statuscode {response.status_code}\n", exc_info=True)
        return None

def get_individual_hospital(link):
    """
    Get a hospital by its individual link
    :param: link: from the JSON of the hospital
    :return: html of the hospital page
    """
    try:
        html = urllib.request.urlopen(link).read().decode("utf-8")
        logger.info("got html for " + link)
        return html
    except Exception as e:
        logger.error(f"Failed to get HTML for {link}\n", exc_info=True)
        return None

