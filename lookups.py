"""
Useful functions for looking up information
"""
import socket

import dns.resolver

#TODO implement the lookup-functions



def dns_lookup(dns_record):
    """
    Get the IP Address for a DNS Record
    :param dns_record: DNS Record to get the IP Address for
    :return: IP Address of the DNS Record
    """
    try:
        ip_address = socket.gethostbyname(dns_record)
        return ip_address
    except Exception as e:
        return None

def mx_lookup(mx_record):
    """
    Get the hostname for a mx record
    :param mx_record: mx record to get the hostname for
    :return: hostname of the mx record
    """
    try:
        mx_hostname = dns.resolver.resolve(mx_record, 'MX')
        return str(mx_hostname[0].exchange)
    except Exception as e:
        return None