import logging
import os
import sys

from flask import Flask, request
from dreamhost import dynamic_dns

logger = logging.getLogger()


DREAMHOST_API_KEY = os.environ["DREAMHOST_API_KEY"]


app = Flask(__name__)

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


@app.route("/")
def index():
    api_key = request.args.get("key")
    hostname = request.args.get("hostname")
    ip = request.args.get("ip")

    if api_key != DREAMHOST_API_KEY:
        return "invalid api key"

    if not hostname:
        logger.error("no hostname entered")
        return "please add a hostname"

    if not ip:
        logger.error("no ip entered")
        return "please add an ip"

    logger.info("ip = %s", ip)
    resp = dynamic_dns(ip, hostname)
    return resp

