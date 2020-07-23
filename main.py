import logging
import os
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


def dynamic_dns():
    """fix dns record"""
    cmd = 'dns-list_records'
    dns_records = _call(cmd)
    dns_ip = _get_dns_ip(dns_records)
    logger.info('dns_ip = %s', dns_ip)


def main():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    dynamic_dns()

if __name__ == '__main__':
    main()
