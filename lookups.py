"""
Useful functions for looking up information
"""
import dns.resolver

def dns_lookup(dns_record):
    """
    Get the IP Address for a DNS Record
    :param dns_record: DNS Record to get the IP Address for
    :return: IP Address of the DNS Record
    """
    try:
        ip_address = dns.resolver.resolve(dns_record, 'A')
        return str(ip_address[0])
    except Exception as e:
        return None

def mx_lookup(dns_record):
    """
    Get the hostname from an mx-lookup of a dns-record
    :param dns_record: dns_record to get the hostname for
    :return: hostname
    """
    try:
        mx_hostname = dns.resolver.resolve(dns_record, 'MX')
        return str(mx_hostname[0].exchange)
    except Exception as e:
        return None