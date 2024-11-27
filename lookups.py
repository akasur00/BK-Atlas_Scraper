"""
Useful functions for looking up information
"""
import dns.resolver

#TODO implement the lookup-functions



def dns_lookup(dns_record):
    """
    Get the IP Address for a DNS Record
    :param dns_record: DNS Record to get the IP Address for
    :return: IP Address of the DNS Record
    """
    try:
        for mx in dns.resolver.resolve(dns_record, 'MX'):
            print (mx.to_text())
    except Exception as e:
        return None
    return mx

dns_lookup('hotmail.com')