"""Dreamhost python module"""

import json
import logging
import os
from urllib.request import urlopen
from urllib.parse import urlencode


logger = logging.getLogger(__name__)

DREAMHOST_API_KEY = os.environ["DREAMHOST_API_KEY"]

def _call(cmd, **params):
    params['cmd'] = cmd
    params['key'] = DREAMHOST_API_KEY
    params['format'] = 'json'
    qs = urlencode(params)
    url = f"https://api.dreamhost.com?{qs}"
    logger.info('loading %s', url)
    resp = urlopen(url)
    
    resp_text = resp.read().decode()
    try:
        resp_data = json.loads(resp_text)
    except json.decoder.JSONDecodeError:
        logger.error('Non-JSON response from %s', url)
        logger.error(resp_text)
        resp_data = None

    if resp_data.get('result') =='error':
        logger.error(resp_data)
    return resp_data

def dns_list_records():
    cmd = 'dns-list_records'
    resp = _call(cmd)
    return resp

def dns_add_record(current_ip, record):
    cmd = 'dns-add_record'
    logger.info('creating record for %s', current_ip)
    resp = _call(cmd, record=record, type='A', value=current_ip)
    logger.info('attempted to create dns %r', resp)
 

def dns_remove_record(ip, hostname):
    cmd = 'dns-remove_record'
    resp = _call(cmd, value=ip, type='A', record='hostname')
    logger.info('attempted to remove dns record %r', resp)


def _get_dns_ip(records, hostname):
    rec_type = 'A'
    for record in records['data']:
        if record['type'] != rec_type:
            continue
        if record['record'] == hostname:
            return record['value']

    logger.error('cannot find %s record for %s', rec_type, DREAMHOST_DNS_DOMAIN)


 
def dynamic_dns(new_ip, hostname):
    records = dns_list_records()
    dns_ip = _get_dns_ip(records, hostname)
    if dns_ip == new_ip:
        message = f'dns_ip and new_ip match {new_ip}. No need to update'
    elif not dns_ip:
        dns_add_record(new_ip, hostname)
        message = f'dns record added {new_ip}'
    else:
        dns_remove_record(dns_ip, hostname)
        dns_add_record(new_ip, hostname)
        message =  f'dns record updated {new_ip}'

    logger.info(message)
    return message
