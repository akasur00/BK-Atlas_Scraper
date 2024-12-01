"""
Functions for the Bundesklinik Atlas API
https://klinikatlas.bmg.api.bund.dev/
No API Token needed
"""

import urllib.request
import requests

base_url = "https://klinikatlas.api.proxy.bund.dev"
all_hospitals_url = "/fileadmin/json/locations.json"

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
        return None

