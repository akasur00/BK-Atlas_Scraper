"""
Functions for the Bundesklinik Atlas API
https://klinikatlas.bmg.api.bund.dev/
No API Token is needed
"""

import logging
import urllib.request
import requests

base_url = "https://klinikatlas.api.proxy.bund.dev"
all_hospitals_url = "/fileadmin/json/locations.json"

logger = logging.getLogger()
logging.basicConfig(filename='./Logs/bundesklinik-atlas.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

def get_all_hospitals():
    """
    Get all hospitals from the Bundesklinik Atlas API
    :param: base_url: basic URL of the API
    :param: all_hospitals_url: part of the URL to get all hospitals
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
        logging.info(f"got {len(response.json())} hospitals from {base_url + all_hospitals_url}")
        return response.json()
    else:
        return None

def get_individual_hospital(link):
    """
    Get a hospital by its individual link
    :param: link: from the JSON of the hospital
    :return: html of the hospital page
    """
    try:
        html = urllib.request.urlopen(link).read().decode("utf-8")
        return html
    except Exception as e:
        logging.error(f"Failed to get HTML for {link}\n", exc_info=True)
        return None

