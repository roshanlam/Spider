from urllib.parse import urlparse
from Exceptions import domain

def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-2] + '.' + results[-1]
    except domain.DomainExceptions.DomainNameException as DNE:
        return DNE

def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except domain.DomainExceptions.SubDomainNameException as SDNE:
        return SDNE