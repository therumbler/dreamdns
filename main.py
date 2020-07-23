import logging
import os
from urllib.request import urlopen
import sys

from dreamhost import _call

DREAMHOST_DNS_DOMAIN = os.environ["DREAMHOST_DNS_DOMAIN"]

logger = logging.getLogger(__name__)


def _get_dns_ip(dns_records):
    rec_type = 'A'
    for record in dns_records['data']:
        if record['type'] != rec_type:
            continue
        if record['record'] == DREAMHOST_DNS_DOMAIN:
            return record['value']

    logger.error('cannot find %s record for %s', rec_type, DREAMHOST_DNS_DOMAIN)

def get_current_ip():
    """fetch the current public IP address"""
    url = "https://api.ipify.org/"
    public_ip = urlopen(url).read().decode()
    logger.debug('public_ip = %s', public_ip)
    return public_ip

def dns_add_record(current_ip):
    cmd = 'dns-add_record'
    logger.info('creating record for %s', current_ip)
    resp = _call(cmd, record=DREAMHOST_DNS_DOMAIN, type='A', value=current_ip)
    logger.info('attempted to create dns %r', resp)
    

def dynamic_dns():
    """fix dns record"""
    cmd = 'dns-list_records'
    dns_records = _call(cmd)
    dns_ip = _get_dns_ip(dns_records)
    logger.info('dns_ip = %s', dns_ip)
    current_ip = get_current_ip()
    if dns_ip == current_ip:
        logger.info('dns_ip and current_ip are both %s', dns_ip)
        return
    logger.error('ip mismatch. dns: %s. current %s', dns_ip, current_ip)
    if not dns_ip:
        dns_add_record(current_ip)


def main():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    dynamic_dns()

if __name__ == '__main__':
    main()
