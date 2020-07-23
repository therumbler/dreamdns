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

